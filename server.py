import socket
import threading
import os

class Server():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.host=input("ENTER IP:")
        # self.port=int(input("Enter port:"))
        self.host="127.0.0.1"
        self.port=1224
        self.client_num= int(input("Enter num of clients:"))
        self.clients=[]

        try:
            self.server.bind((self.host,self.port))
            print(f"succsessfully connected to {self.host} {self.port}")
        except:
            print(f"couldnt connect to {self.host} {self.port}")
            exit(-1)
        
        self.server.listen(self.client_num)

        threading.Thread(target=self.connect_listener, args=()).start()


    def connect_listener(self):
        while 1 :
            client, address=self.server.accept()
            print(f"successfully connected to {address[0]} {address[1]}")

            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while 1:
            username = client.recv(2048).decode('utf-8')
            if username != '':
                self.clients.append((client,username))
                break
            else:
                print("empty username")
        threading.Thread(target=self.message_listener, args=(client, username,)).start()
    
    def  message_listener(self, client, username):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                msg =username + ":  " + message
                self.send_all(msg)
            else:
                continue

    def send_all(self, msg):
        for client in self.clients:
            client[0].sendall(msg.encode())



if __name__=="__main__":
    s=Server()
