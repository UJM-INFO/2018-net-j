#!/usr/bin/python3
#
# member class
#

from Chain import Chain
from socket import socket, create_connection
from threading import Thread, Timer
import netutils
import pickle
import os

TRACKER_IP = "127.0.0.1"
TRACKER_PORT = 9876

class Member:
    
    CHAIN_PATH = str(os.path.expanduser("~")) + "/.chain/"
    os.makedirs(CHAIN_PATH, exist_ok=True)

    def __init__(self, identity, port=1112):
        self.path = Member.CHAIN_PATH + identity
        self.port = port
        self.registered = False
        self.blockChain = self.reloadChain() # reloadChain from Disk
        Timer(10, self.dumpChain).start() # dumpChain every 10 seconds

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
            conn.sendall(bytes('127.0.0.1:' + str(self.port) + '\r\n', 'utf-8')) 
            conn.close()
            self.registered = True
        except Exception as e:
            print("cannot register member: ", e)

    def startListening(self):
        listenerSocket = socket()
        listenerSocket.bind(("localhost", self.port))
        listenerSocket.listen()
        print("socket is listening", listenerSocket)
        def listenerThread():
            while True:
                conn, addr = listenerSocket.accept()
                print("handle connection", conn)
                Thread(target=self.handleClient, args=(conn,)).start()
        Thread(target=listenerThread).start()

    def handleClient(self, conn):
        l = netutils.readLine(conn)
        print("RECIEVED: ", l)

        if l == "PING":
            conn.sendall(b"OK\r\n")
            print("SENT: OK")
    
        conn.close()
        print("connection closed", conn)


    def startSYNC(self):
        pass
    

if __name__ == "__main__":
    mem = Member("1")
    mem.register()
    mem.startListening()
