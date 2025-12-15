import string
import random
import hashlib


# return the hash of a string
def SHA(s: string) -> string:
    return hashlib.sha256(s.encode()).hexdigest()


# transfer a hex string to integer
def toDigit(s: string) -> int:
    return int(s, 16)


# generate 2^d (si^{-1}, si) pairs based on seed r
def KeyPairGen(d: int, r: int) -> dict:
    pairs = {}
    random.seed(r)
    for i in range(1 << d):
        cur = random.randbytes(32).hex()
        while cur in pairs:
            cur = random.randbytes(32).hex()
        pairs[cur] = SHA(cur)
    return pairs


class MTSignature:
    def __init__(self, d, k):
        self.d = d
        self.k = k
        self.treenodes = [None] * (d + 1)  # optional data structure
        for i in range(d + 1):
            self.treenodes[i] = [None] * (1 << i)
        self.sk = [None] * (1 << d)
        self.pk = None  # same as self.treenodes[0][0], if you are using self.treenodes

    # Populate the merkle tree, self.sk and self.pk. Returns self.pk.
    def KeyGen(self, seed: int) -> str:
        # create key pairs for each level
        pairs = KeyPairGen(self.d, seed)
        # store the key pairs for the highest level in the Merkle tree
        self.treenodes[self.d] = list(pairs.values())
        # build the Merkle tree from the bottom up
        for i in range(self.d, 0, -1):
            next_level = []
            curr_level = self.treenodes[i]
            i_val = 0
            # generate parent nodes by hashing pairs of child nodes
            for j in range(0, len(curr_level), 2):
                node_value = SHA(
                    format(i_val, "b").zfill(256) + curr_level[j] + curr_level[j + 1]
                )
                next_level.append(node_value)
                i_val += 1
            self.treenodes[i - 1] = next_level
        self.sk = list(pairs.keys())
        self.pk = self.treenodes[0][0]
        return self.pk

    # Returns the path SPj for the index j
    # The order in SPj follows from the leaf to the root.
    def Path(self, j: int) -> str:
        path = []
        curr_node = j
        for depth in range(self.d, 0, -1):
            # flip the last bit of the node index
            sibling_index = curr_node ^ 1
            # get the sibling node
            sibling_value = self.treenodes[depth][sibling_index]
            # append path
            path.append(sibling_value)
            # move to the next level
            curr_node = curr_node // 2
        return "".join(path)

    # Returns the signature. The format of the signature is as follows: ([sigma], [SP]).
    # The first is a sequence of sigma values and the second is a list of sibling paths.
    # Each sibling path is in turn a d-length list of tree node values.
    # All values are 64 bytes. Final signature is a single string obtained by concatentating all values.
    def Sign(self, msg: string) -> string:
        sigma = []
        sibling_paths = []
        for j in range(1, self.k + 1):
            # compute zj to find index with message and j
            zj = toDigit(SHA(format(j, "b").zfill(256) + msg)) % (2**self.d)
            # find pk at index zj
            sigma_j = self.sk[zj]
            sigma.append(sigma_j)
            # find path for leaf zj
            path = self.Path(zj)
            sibling_paths.append(path)
        sigma_str = "".join(sigma)
        sibling_paths_str = "".join(sibling_paths)
        return sigma_str+sibling_paths_str
