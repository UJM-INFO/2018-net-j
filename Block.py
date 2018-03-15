#!/usr/bin/python3
#
# Block class
#
# TODO: timestamp required?
# self.timestamp.isoformat()

import hashlib

class Block:

    DIFFICULTY = 4

    def __init__(self, id, data, prehash):
        self.id = id
        self.data = data
        self.prehash = prehash
        self.mineHash()
    
    def mineHash(self):
        self.nonce = 0
        self.hash = ""
        while not self.hash.startswith("0" * Block.DIFFICULTY):
            self.nonce += 1 # or random?
            self.hash = self.calculateHash()

    def calculateHash(self):
        encodedBlock = (
                str(self.id) +
                str(self.data) +
                str(self.nonce) + 
                self.prehash).encode('utf-8')
        return hashlib.sha256(encodedBlock).hexdigest()

    def __repr__(self):
        return "<block " + str(self.id) + " " + self.hash[-7:] + ">"


if __name__ == "__main__":
    b = Block(27, "hello block", "0")
    print(b)
    print(b.hash)
