from socket import *
from threading import Thread
from netutils import *
import random 
import time

tracker_ip = '192.168.1.3'
tracker_port = 9876
max_member_sample_size = 3

class Tracker:

    def __init__(self):
        self.membersList = []

    def startListning(self):
        def acceptAll():
            serverSocket = socket()
            serverSocket.bind((tracker_ip,tracker_port))
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
                        print("debug mes: start ping member:",ip,port)
                        conn = create_connection((ip,port))
                        conn.sendall(b"PING\r\n")
                        l = readLine(conn)
                        if l != "OK":
                            print("debug mes: ping member:",ip,port," bad response: ",l)
                        else:
                            print("debug mes: ping member:",ip,port," good response: ",l)
                    except:
                        print("debug mes: ping member:",ip,port," Member timeout, Deleting member!")
                        self.membersList.remove(mem)
                time.sleep(60)

        Thread(target=pingAll).start()
        Thread(target=acceptAll).start()
    
    def handleClient(self,conn, ip):
        def handle():
            
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
                        max_member_sample_size if len(self.membersList) > max_member_sample_size else len(self.membersList))) ]
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
