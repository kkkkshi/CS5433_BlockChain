import java.util.HashSet;
import java.util.Set;

/* CompliantNode refers to a node that follows the rules (not malicious)*/
public class CompliantNode implements Node {

    private boolean[] followees;
    private Set<Transaction> pending;

    public CompliantNode(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
        this.pending = new HashSet<Transaction>();
    }

    public void setFollowees(boolean[] followees) {
        this.followees = followees;
    }

    public void setPendingTransaction(Set<Transaction> pendingTransactions) {
        this.pending = new HashSet<Transaction>(pendingTransactions);
    }

    public Set<Transaction> sendToFollowers() {
        // send everything we've heard; the union across rounds is the consensus set
        return new HashSet<Transaction>(pending);
    }

    public void receiveFromFollowees(Set<Candidate> candidates) {
        // only trust txs from nodes we actually follow
        for (Candidate c : candidates) {
            if (followees != null && c.sender >= 0 && c.sender < followees.length && followees[c.sender])
                pending.add(c.tx);
        }
    }
}
