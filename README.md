# CS 5433 Blockchain

Coursework for CS 5433 (Spring 2024): the Java programming assignments and the
written/coding homework. The solutions here are my own (netid ks2365).

## Layout

```
cryptocurrency_assignments/        Java assignments
  Assignment_1/   TxHandler      validate transactions against a UTXO pool
  Assignment_2/   CompliantNode  reach consensus over a random trust graph
  Assignment_3/   BlockChain     maintain a forking chain with cut-off pruning
  Assignment_4/   handout only

Homework/
  Homework1/   Python    p1 coin watermark, p2 Merkle proofs, p3 Merkle signatures
  Homework2/   Python    p1 PoW/PoA block validation, p3 gossip network
  Homework3/   Solidity  p1 wrapped-ether ERC-20 token, p2 EthermonLite battle
  Homework4/   handout only
```

The support classes in each Java assignment (`Transaction`, `UTXO`, `Crypto`,
and so on) are course-provided. The files I wrote are `TxHandler`,
`CompliantNode` and `BlockChain`, plus a do-nothing adversary that the
Assignment 2 simulation expects.

## Building and running

Java (needs a JDK):

    cd cryptocurrency_assignments/Assignment_1
    javac *.java

Assignment 2 includes a simulation you can run directly:

    cd cryptocurrency_assignments/Assignment_2
    javac *.java
    java Simulation 0.2 0.3 0.05 10      # p_graph p_malicious p_tx numRounds

Homework 1 has self-contained tests:

    cd "Homework/Homework1/hw1-ks2365 copy/p2" && python3 test.py
    cd "Homework/Homework1/hw1-ks2365 copy/p3" && python3 test.py

The Homework 2 Python files belong to a larger course framework that is not
checked in, so they are here for reading rather than running on their own.

Solidity (needs solc 0.8.x):

    solc Homework/Homework3/hw3_code/p1/ERC20.sol
    solc Homework/Homework3/hw3_code/p2/WinBattle.sol
