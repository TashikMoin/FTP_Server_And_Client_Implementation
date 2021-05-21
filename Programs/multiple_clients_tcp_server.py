import socket
import sys
import os
import threading

Recv_Terminated = False
Send_Terminated = False

def recv_msg(Client_Socket,address):
    global Recv_Terminated
    global Send_Terminated
    Recv_Message = ""
    while Recv_Message != 'q':
        if Send_Terminated == False:
            Recv_Message = str(Client_Socket.recv(1024).decode('utf-8'))
            if Recv_Message == 'q':
                print(f'\nConnection with client {address} is now terminated.')
                Client_Socket.send(bytes('q', "utf-8"))
                Recv_Terminated = True
                break
            print(f'\nMessage recieved from client {address}  --->  {Recv_Message}\n>>')
        else:
            break


Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server_Socket.bind(('127.0.0.1', int(sys.argv[1]) ))
Server_Socket.listen(10)
print("Server started listening on port # " + str(sys.argv[1]) )
print("Note: Enter 'q' to terminate connections")
while True:
    Client_Socket, address = Server_Socket.accept()
    if os.fork() == 0 :
        Server_Socket.close() 
        print(f'\nConnected with client {address}')
        Recv_Thread = threading.Thread(target=recv_msg, args=(Client_Socket,address))
        Recv_Thread.start()
        Send_Message = ""
        while Send_Message != 'q':
            if Recv_Terminated == True:
                break
            Send_Message = input(f'\nSend a message to the client {address}\n>>')
            Client_Socket.send(bytes(Send_Message, "utf-8"))
        Send_Terminated = True
        Client_Socket.close()