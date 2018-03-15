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
                self.handleClient(conn, addr[0])
        
        def pingAll():
            while True:
                print("debug mes: start new ping cycle")
                for mem in self.membersList:
                    try:
                        
                        ip = mem.split(':')[0]
                        port = int (mem.split(':')[1])
                        print("debug mes: ping member:",ip,port)
                        conn = create_connection((ip,port))
                        conn.sendall(b"PING\r\n")
                        l = readLine(conn)
                        if l != "PONG":
                            print("debug mes: ping member:",ip,port," bad response: ",l)
                        else:
                            print("debug mes: ping member:",ip,port," good response: ",l)
                    except:
                        print("debug mes: ping member:",ip,port," Exception ")
                        self.membersList.remove(mem)
                time.sleep(10000)

        Thread(target=pingAll).start()
        Thread(target=acceptAll).start()
    
    def handleClient(self,conn, ip):
        def handle():
            #print("handle client")
            l = readLine(conn)
            #print(l)
            if l == addMemberCommand:
                port = readLine(conn)
                addr = ip + ":" + port
                if addr not in self.membersList:
                    self.membersList.append(addr)
                    print("debug mes: add member:",addr)
                conn.sendall(b"OK\r\n")
                
                
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
