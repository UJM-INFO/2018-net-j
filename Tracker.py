from socket import socket
from threading import Thread
from netutils import *
import random 

SAMPLE_SIZE = 3

class Tracker:

    def __init__(self):
        self.membersList = ['1','5','3','4','4','5','6','8','4','4']

    def startListning(self):
        def acceptAll():
            serverSocket = socket()
            serverSocket.bind(('localhost',9876))
            serverSocket.listen()
            while True:
                conn, addr = serverSocket.accept()
                self.handleClient(conn)
                
        Thread(target=acceptAll).start()
    
    def handleClient(self,conn):
        def handle():
            #print("handle client")
            l = readLine(conn)
            print(l)
            if l == addMemberCommand:
                addr = readLine(conn)
                self.membersList.append(addr)
                conn.sendall(b"OK\r\n")
                print(self.membersList)
            elif l == getMembersCommand:
                sample = [ self.membersList[i] for i in sorted(random.sample(range(len(self.membersList)), SAMPLE_SIZE)) ]
                for s in sample:
                    conn.sendall((s+"\r\n").encode('UTF-8'))
                conn.sendall(b"END\r\n")
            else:
                conn.sendall((badCommand+"\r\n").encode('UTF-8'))
            conn.close()
        Thread(target=handle).start()
if __name__ == "__main__":
    t = Tracker()
    t.startListning()
