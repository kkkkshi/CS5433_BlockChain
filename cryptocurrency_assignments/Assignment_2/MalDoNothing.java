import java.util.Set;
import java.util.HashSet;

/* malicious node that does nothing: never forwards, ignores all input */
public class MalDoNothing implements Node {

    public MalDoNothing(double p_graph, double p_malicious, double p_txDistribution, int numRounds) {
    }

    public void setFollowees(boolean[] followees) {
    }

    public void setPendingTransaction(Set<Transaction> pendingTransactions) {
    }

    public Set<Transaction> sendToFollowers() {
        return new HashSet<Transaction>();
    }

    public void receiveFromFollowees(Set<Candidate> candidates) {
    }
}
