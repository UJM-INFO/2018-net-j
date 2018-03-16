#!/usr/bin/python3
#
# Chain class
#

from Block import Block

class Chain:
    #transfer from god to genesis. Amount: 5000
    GENESIS_BLOCK = Block(0, "god genesis 5000", "0")

    def __init__(self):
        self.stack = [Chain.GENESIS_BLOCK]
    
    def createBlock(self, data):
        lastid = self.stack[-1].id
        lasthash = self.stack[-1].hash
        block = Block(lastid + 1, data, lasthash)
        if self.insertBlock(block):
            return block
        else:
            return -1

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
        # check user balance
        if not self.checkBalance(block.data):
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
            prehash = block.hash
        return True

    def __repr__(self):
        rp = "{chain"
        for b in self.stack:
            rp += " " + str(b)
        return rp + "}"
    def checkBalance(self,data):
        client = data.split()[0]
        amount = int(data.split()[2])
        clientBalance = 0
        for b in self.stack:
            #transfer to the client
            if b.data.split()[1] == client:
                clientBalance = clientBalance + int(b.data.split()[2])
            #transfer from the client
            if b.data.split()[0] == client:
                clientBalance = clientBalance - int(b.data.split()[2])
        return amount <= clientBalance

if __name__ == "__main__":
    c = Chain()
    print(c.createBlock("genesis Muaz 1000"))
    print(c.createBlock("Muaz Abood 500"))
    print(c.createBlock("Abood Muaz 501"))

    print(c)
    c.dropLastBlock()
    print(c)
    print(c.isValid())