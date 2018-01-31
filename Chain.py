#!/usr/bin/python3
#
# Chain class
#

from Block import Block

class Chain:

    GENESIS_BLOCK = Block(0, "genesis", "0")

    def __init__(self):
        self.stack = [Chain.GENESIS_BLOCK]
    
    def createBlock(self, data):
        lastid = self.stack[-1].id
        lasthash = self.stack[-1].hash
        block = Block(lastid + 1, data, lasthash)
        self.stack.append(block)
        return block

    def insertBlock(self, block):
        # make sure hash is valid 
        if block.hash != block.calculateHash():
            return False
        # hash must pass the difficulty check
        if not block.hash.startswith("0" * Block.DIFFICULTY):
            return False
        # increment id check
        if block.id != self.stack[-1].id + 1:
            return False
        # check chain link is valid
        if block.prehash != self.stack[-1].hash:
            return False
        self.stack.append(block)
        return True

    def getBlockById(self, id):
        return self.stack[id]

    def dropLastBlock(self):
        self.stack.pop()

    def isValid(self):
        prehash = Chain.GENESIS_BLOCK.hash
        for block in self.stack[1:]:
            if block.hash != block.calculateHash():
                return False
            if block.prehash != prehash:
                return False
        return True

    def __repr__(self):
        rp = "{chain"
        for b in self.stack:
            rp += " " + str(b)
        return rp + "}"

if __name__ == "__main__":
    c = Chain()
    c.createBlock("new data")
    c.createBlock("more data")
    print(c)
    c.dropLastBlock()
    print(c)
    print(c.isValid())