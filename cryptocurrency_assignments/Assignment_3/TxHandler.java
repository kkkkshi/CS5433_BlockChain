import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class TxHandler {

    /** Current view of unspent transaction outputs. */
    private UTXOPool utxoPool;

    /** Creates a public ledger whose current UTXOPool is a copy of {@code utxoPool}. */
    public TxHandler(UTXOPool utxoPool) {
        this.utxoPool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if all claimed outputs are in the pool, every input signature is valid, no UTXO
     *         is double-claimed, every output value is non-negative, and inputs cover outputs.
     */
    public boolean isValidTx(Transaction tx) {
        Set<UTXO> claimed = new HashSet<UTXO>();
        double inputSum = 0;

        ArrayList<Transaction.Input> inputs = tx.getInputs();
        for (int i = 0; i < inputs.size(); i++) {
            Transaction.Input in = inputs.get(i);
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);

            if (!utxoPool.contains(utxo))
                return false;

            Transaction.Output prevOut = utxoPool.getTxOutput(utxo);

            if (!Crypto.verifySignature(prevOut.address, tx.getRawDataToSign(i), in.signature))
                return false;

            if (!claimed.add(utxo))
                return false;

            inputSum += prevOut.value;
        }

        double outputSum = 0;
        for (Transaction.Output out : tx.getOutputs()) {
            if (out.value < 0)
                return false;
            outputSum += out.value;
        }

        return inputSum >= outputSum;
    }

    /**
     * Returns a mutually valid subset of {@code possibleTxs}, updating the UTXO pool as each
     * transaction is accepted.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        ArrayList<Transaction> accepted = new ArrayList<Transaction>();

        boolean progress = true;
        while (progress) {
            progress = false;
            for (Transaction tx : possibleTxs) {
                if (tx == null || !isValidTx(tx))
                    continue;

                accepted.add(tx);

                for (Transaction.Input in : tx.getInputs())
                    utxoPool.removeUTXO(new UTXO(in.prevTxHash, in.outputIndex));

                byte[] txHash = tx.getHash();
                ArrayList<Transaction.Output> outs = tx.getOutputs();
                for (int i = 0; i < outs.size(); i++)
                    utxoPool.addUTXO(new UTXO(txHash, i), outs.get(i));

                progress = true;
            }
        }

        return accepted.toArray(new Transaction[0]);
    }
}
