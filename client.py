import socket
import threading
import os

class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # self.host=input("ENTER IP:")
        # self.port=int(input("Enter port:"))
        self.username=input("Enter username: ")
        if self.username == "":
            print("empty userrname")
            exit(-1)
        self.host="127.0.0.1"
        self.port=1224

        try:
            self.client.connect((self.host,self.port))
            print(f"succsessfully connected to server")
        except:
            print(f"couldnt connect to server {self.host} {self.port}")
            exit(-1)

        threading.Thread(target=self.server_signup, args=()).start()


    def server_signup(self):
        self.client.sendall(self.username.encode())

        threading.Thread(target=self.message_listener, args=(self.client,)).start()
        self.message_sender()

    def  message_listener(self, client):
            while 1:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    username = message.split(": ")[0]
                    msg = message.split(": ")[1]
                    print(f"\033[F\033[{100}G \n{username}|> {msg} \nYOU|> ", end="")
                else:
                    continue
   
    def message_sender(self):
        while 1:
            message=input("YOU|> ")
            if message != '':
                self.client.sendall(message.encode())
            else:
                print("empty message")
                continue



if __name__=="__main__":
    s=Client()
   
