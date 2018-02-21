from socket import *
from threading import Thread
from netutils import *
import random 
import time

SAMPLE_SIZE = 3

class Tracker:

    def __init__(self):
        self.membersList = []

    def startListning(self):
        def acceptAll():
            serverSocket = socket()
            serverSocket.bind(('localhost',9876))
            serverSocket.listen()
            while True:
                conn, addr = serverSocket.accept()
                self.handleClient(conn)
        
        def pingAll():
            while True:
                for mem in self.membersList:
                    try:
                        ip = mem.split(':')[0]
                        port = int (mem.split(':')[1])
                        conn = create_connection((ip,port))
                        conn.sendall(b"PING\r\n")
                        l = readLine(conn)
                        if l != "PONG":
                            print("Oh NO!!")
                        else:
                            print("Oh Yeah!")
                    except:
                        self.membersList.remove(mem)
                time.sleep(5000*60)

        Thread(target=pingAll).start()
        Thread(target=acceptAll).start()
    
    def handleClient(self,conn):
        def handle():
            #print("handle client")
            l = readLine(conn)
            print(l)
            if l == addMemberCommand:
                addr = readLine(conn)
                if addr not in self.membersList:
                    self.membersList.append(addr)
                conn.sendall(b"OK\r\n")
                print(self.membersList)
            elif l == getMembersCommand:
                sample = [ self.membersList[i] for i in sorted(random.sample(range(len(self.membersList)), 
                        SAMPLE_SIZE if len(self.membersList) > SAMPLE_SIZE else len(self.membersList))) ]
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
