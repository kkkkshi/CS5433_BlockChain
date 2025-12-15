import hashlib
from typing import Optional, List

def verify(obj: str, proof: str, commitment: str) -> bool:
    # if there is only one element
    if proof == "":
        return obj == commitment

    # corresponding to the generate_proof
    proof_list = proof.split(',')
    temp_obj = obj
    for pair in proof_list:
        pos_str = pair[0]
        proof_hash = pair[1:]
        # based on the intermediate sign, decode the proof
        if pos_str == "a":
            temp_obj = hashlib.sha256((proof_hash + temp_obj).encode()).hexdigest()
        else:
            temp_obj = hashlib.sha256((temp_obj + proof_hash).encode()).hexdigest()
    # check if the commitment is corresponded
    return temp_obj == commitment


class Prover:
    def __init__(self):
        # original inputs
        self.objects = []
        # hashed value to build the merkle tree
        self.merkle_tree = []

    # build merkle tree
    def build_merkle_tree(self, objects: List[str]) -> str:
        self.objects = objects

        # edge case with only one element - root
        if len(objects) == 1:
            curr_level = [hashlib.sha256(objects[0].encode()).hexdigest()]
            self.merkle_tree.append(curr_level)
            return self.merkle_tree[-1][0]

        # normal case
        curr_level = [hashlib.sha256(obj.encode()).hexdigest() for obj in objects]

        # if odd number of element, append one to make it even
        if len(objects) % 2 == 1:
            curr_level.append(curr_level[-1])
        self.merkle_tree.append(curr_level)

        while len(curr_level) > 1:
            temp_level = []
            # build the parent hash
            for i in range(0, len(curr_level) // 2):
                temp_hash = hashlib.sha256((curr_level[2 * i] + curr_level[2 * i + 1]).encode()).hexdigest()
                temp_level.append(temp_hash)
            # if not root and there is odd number of elements, copy it to make it even
            if len(temp_level) != 1 and len(temp_level) % 2 == 1:
                temp_level.append(temp_level[-1])
            self.merkle_tree.append(temp_level)
            # start the next loop for their parents
            curr_level = temp_level

        return self.merkle_tree[-1][0]

    # get leaf from the objects
    def get_leaf(self, index: int) -> Optional[str]:
        if 0 <= index < len(self.objects):
            return self.objects[index]
        else:
            return None

    # "1H, 0H, ,.."
    def generate_proof(self, index: int) -> Optional[str]:
        # if not in the index, return
        if self.get_leaf(index) is None:
            return None

        # saving the results
        proof_list = []
        # loop through each level (bottom-up) except root
        # check each level to find the proof string
        for i in range(len(self.merkle_tree) - 1):
            # if index is odd, add the previous one
            if index % 2 == 1:
                proof_list.append('a' + self.merkle_tree[i][index - 1])
            # if index is even, add the following one
            else:
                proof_list.append('b' + self.merkle_tree[i][index + 1])
            # get the index for next level
            index = index // 2
        return ",".join(proof_list)