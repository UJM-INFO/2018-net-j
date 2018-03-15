#!/usr/bin/python3
#
# member class
#

from Chain import Chain
from socket import socket, create_connection, gethostname, gethostbyname_ex
from threading import Thread, Timer
import threading
import netutils
import pickle
import os
import time

TRACKER_IP = "192.168.1.3"
TRACKER_PORT = 9876

MY_IP = "192.168.1.12"

class Member:
    
    CHAIN_PATH = str(os.path.expanduser("~")) + "/.chain/"
    os.makedirs(CHAIN_PATH, exist_ok=True)

    def __init__(self, port=1112):
        self.path = Member.CHAIN_PATH + str(port)
        self.port = port
        self.memberList = []
        self.registered = False
        self.blockChain = self.reloadChain() # reloadChain from Disk

    def runLoops(self):
        self.isLoop = True
        def loop():
            self.register() # register client once
            while True and self.isLoop: 
                Thread(target=self.dumpChain).start() # dumpChain every 10 seconds
                Thread(target=self.sniffBlocks).start() # sniff for new blocks every 10 seconds
                time.sleep(30)
        Thread(target=loop).start()
    
    def stopLoops(self):
        self.isLoop = False

    def reloadChain(self):
        try:
            return pickle.load(open(self.path, "rb"))
        except:
            return Chain()

    def dumpChain(self):        
        pickle.dump(self.blockChain, open(self.path, "wb"))

    def register(self):
        try:
            conn = create_connection((TRACKER_IP, TRACKER_PORT))
            conn.sendall(b'REGISTER\r\n') # TODO: send network ip?
            conn.sendall(bytes(str(self.port) + '\r\n', 'utf-8')) 
            conn.close()
            self.registered = True
        except Exception as e:
            print("cannot register member: ", e)

    def fetchMembers(self):
        try:
            conn = create_connection((TRACKER_IP, TRACKER_PORT))
            conn.sendall(b"GETMEMBERS\r\n")
            print("SENT: GETMEMBERS")
            self.memberList = []
            while True:
                l = netutils.readLine(conn)
                if l == "END":
                    break
                else:
                    if (l == MY_IP + ':' + str(self.port)): # ignore self
                        continue
                    self.memberList.append(l)
            print("RECIEVED MEMBERS: ", self.memberList)

        except Exception as e:
            print("getmembers error: ", e)

    def startListening(self):
        listenerSocket = socket()
        listenerSocket.bind((MY_IP, self.port))
        listenerSocket.listen()
        print("socket is listening", self.port )
        def listenerThread():
            while True:
                conn, addr = listenerSocket.accept()
                print("handle connection", addr)
                Thread(target=self.handleClient, args=(conn,)).start()
        Thread(target=listenerThread).start()

    def handleClient(self, conn):
        l = netutils.readLine(conn)
        print("RECIEVED: ", l)

        if l == "PING":
            conn.sendall(b"OK\r\n")
            print("SENT: OK")
        
        if l == "SENDBLOCK":
            blkdump = netutils.readLine(conn)
            blk = pickle.loads(blkdump)
            print("RECIVED BLOCK: ", blk)
            if len(self.blockChain.stack) != blk.id:
                print("SENT: DROP")
                conn.sendall(b"DROP\r\n")
            else:    
                status = self.blockChain.insertBlock(blk)
                if status:
                    print("SENT: OK")
                    conn.sendall(b"OK\r\n")
                else:
                    print("SENT: INVALID")
                    conn.sendall(b"INVALID\r\n")
        
        if l == "GETBLOCK":
            id = netutils.readLine(conn)
            id = int(id)
            print("RECIEVED: ", id)
            if len(self.blockChain.stack) > id:
                blkdump = pickle.dumps(self.blockChain.stack[id])
                conn.sendall(blkdump)
                conn.sendall(b"\r\n")
                print("SENT BLOCK: ", self.blockChain.stack[id])
            else:
                conn.sendall(b"NONE\r\n")
                print("SENT: NONE")

        conn.close()
        print("connection closed")

    def sniffBlocks(self):
        self.fetchMembers()    
        for mem in self.memberList:
            ip, port = mem.split(":")
            fetchid = str(len(self.blockChain.stack))
            try:
                conn = create_connection((ip, port))
                conn.sendall(b'GETBLOCK\r\n')
                print("SENT: GETBLOCK")
                conn.sendall(bytes(fetchid + '\r\n', 'utf-8'))
                print("SENT: ", fetchid)
                response = netutils.readLine(conn)
                conn.close()
                if response == "NONE":
                    print("RECIEVED: NONE")
                    continue
                else:
                    blk = pickle.loads(response)
                    print("RECIEVED BLOCK: ", blk)
                    status = self.blockChain.insertBlock(blk)
                    if status:
                        print("block added!")
                    else:
                        print("block ignored!")
            except Exception as e:
                print("sniffing error: ", e)

    def broadcastBlock(self, id):
        def broadcasterThread():
            self.fetchMembers()
            blkdump = pickle.dumps(self.blockChain.stack[id])
            for mem in self.memberList:
                ip, port = mem.split(":")
                try:
                    conn = create_connection((ip, port))
                    conn.sendall(b'SENDBLOCK\r\n')
                    print("SENT: SENDBLOCK")
                    conn.sendall(blkdump)
                    conn.sendall(b"\r\n")
                    print("SENT BLOCK:", self.blockChain.stack[id])
                    response = netutils.readLine(conn)
                    print("RECIVED: ", response)
                    conn.close()
                    self.registered = True
                except Exception as e:
                    print("broadcast error: ", e)

        Thread(target=broadcasterThread).start()



if __name__ == "__main__":
    from random import randint
    mem = Member(randint(1000, 8999))
    mem.runLoops()
    mem.startListening()
    #mem.blockChain.createBlock("new block 1")
    #mem.blockChain.createBlock("new block 2")
