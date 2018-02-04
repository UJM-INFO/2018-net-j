#!/usr/bin/python3
#
# member class
#

from Chain import Chain
from socket import socket, create_connection
from threading import Thread
import netutils

TRACKER_IP = "127.0.0.1"
TRACKER_PORT = 9876

class Member:
    
    def __init__(self, port=1112):
        self.port = port
        self.registered = False
        self.blockChain = Chain() # TODO: reload the old chain from hard drive

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
    mem = Member()
    mem.register()
    mem.startListening()
