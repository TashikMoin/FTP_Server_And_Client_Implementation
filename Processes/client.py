import socket
import sys
import threading

Recv_Terminated = False
Send_Terminated = False
def recv_msg(client_socket):
    global Recv_Terminated
    global Send_Terminated
    Recv_Message = ""
    while Recv_Message != 'q':
        if Send_Terminated == False:
            Recv_Message = str(client_socket.recv(1024).decode('utf-8'))
            if Recv_Message == 'q':
                client_socket.send(bytes('q', "utf-8"))
                print(f'\nConnection terminated.')
                Recv_Terminated = True
                break
            print(f'\nMessage recieved from server  --->  {Recv_Message}\n>>')
        else:
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((sys.argv[1], int(sys.argv[2])) )
Recv_Thread = threading.Thread(target=recv_msg, args=(client_socket,))
Recv_Thread.start()
Send_Message = ""
while Send_Message != 'q':
    if Recv_Terminated == True:
        break
    Send_Message = input(f'\nSend a message to the server\n>>')
    client_socket.send(bytes(Send_Message, "utf-8"))
Send_Terminated = True
client_socket.close()