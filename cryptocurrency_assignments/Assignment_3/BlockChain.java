// Block Chain should maintain only limited block nodes to satisfy the functions
// You should not have all the blocks added to the block chain in memory
// as it would cause a memory overflow.

import java.util.HashMap;

public class BlockChain {
    public static final int CUT_OFF_AGE = 10;

    /** a block plus its height and the UTXO pool it leaves behind */
    private class BlockNode {
        Block block;
        int height;
        UTXOPool uPool;

        BlockNode(Block block, int height, UTXOPool uPool) {
            this.block = block;
            this.height = height;
            this.uPool = uPool;
        }
    }

    private HashMap<ByteArrayWrapper, BlockNode> nodes;
    private BlockNode maxHeightNode;
    private TransactionPool txPool;

    /**
     * create an empty block chain with just a genesis block. Assume {@code genesisBlock} is a valid
     * block
     */
    public BlockChain(Block genesisBlock) {
        nodes = new HashMap<ByteArrayWrapper, BlockNode>();
        UTXOPool uPool = new UTXOPool();
        addCoinbase(genesisBlock, uPool);
        BlockNode genesis = new BlockNode(genesisBlock, 1, uPool);
        nodes.put(wrap(genesisBlock.getHash()), genesis);
        maxHeightNode = genesis;
        txPool = new TransactionPool();
    }

    /** Get the maximum height block */
    public Block getMaxHeightBlock() {
        return maxHeightNode.block;
    }

    /** Get the UTXOPool for mining a new block on top of max height block */
    public UTXOPool getMaxHeightUTXOPool() {
        return new UTXOPool(maxHeightNode.uPool);
    }

    /** Get the transaction pool to mine a new block */
    public TransactionPool getTransactionPool() {
        return new TransactionPool(txPool);
    }

    /**
     * Add {@code block} to the block chain if it is valid. For validity, all transactions should be
     * valid and block should be at {@code height > (maxHeight - CUT_OFF_AGE)}.
     *
     * <p>
     * For example, you can try creating a new block over the genesis block (block height 2) if the
     * block chain height is {@code <=
     * CUT_OFF_AGE + 1}. As soon as {@code height > CUT_OFF_AGE + 1}, you cannot create a new block
     * at height 2.
     *
     * @return true if block is successfully added
     */
    public boolean addBlock(Block block) {
        if (block == null)
            return false;

        // must point to a known parent (also rejects genesis blocks)
        byte[] prevHash = block.getPrevBlockHash();
        if (prevHash == null)
            return false;
        BlockNode parent = nodes.get(wrap(prevHash));
        if (parent == null)
            return false;

        int height = parent.height + 1;
        if (height <= maxHeightNode.height - CUT_OFF_AGE)
            return false;

        // all txs must be valid against the parent's UTXO pool
        UTXOPool pool = new UTXOPool(parent.uPool);
        TxHandler handler = new TxHandler(pool);
        Transaction[] txs = block.getTransactions().toArray(new Transaction[0]);
        Transaction[] valid = handler.handleTxs(txs);
        if (valid.length != txs.length)
            return false;

        // build this block's UTXO pool from the accepted txs
        for (Transaction tx : valid) {
            for (Transaction.Input in : tx.getInputs())
                pool.removeUTXO(new UTXO(in.prevTxHash, in.outputIndex));
            byte[] txHash = tx.getHash();
            for (int i = 0; i < tx.numOutputs(); i++)
                pool.addUTXO(new UTXO(txHash, i), tx.getOutput(i));
        }
        addCoinbase(block, pool);

        BlockNode node = new BlockNode(block, height, pool);
        nodes.put(wrap(block.getHash()), node);

        // included txs are no longer pending
        for (Transaction tx : block.getTransactions())
            txPool.removeTransaction(tx.getHash());

        if (height > maxHeightNode.height)
            maxHeightNode = node;

        return true;
    }

    /** Add a transaction to the transaction pool */
    public void addTransaction(Transaction tx) {
        txPool.addTransaction(tx);
    }

    /** add the block's coinbase outputs to the pool */
    private void addCoinbase(Block block, UTXOPool pool) {
        Transaction coinbase = block.getCoinbase();
        byte[] hash = coinbase.getHash();
        for (int i = 0; i < coinbase.numOutputs(); i++)
            pool.addUTXO(new UTXO(hash, i), coinbase.getOutput(i));
    }

    private static ByteArrayWrapper wrap(byte[] b) {
        return new ByteArrayWrapper(b);
    }
}
