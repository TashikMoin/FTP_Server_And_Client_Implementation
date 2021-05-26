import socket
import sys
import os
import threading
import time

recv_terminated = False
send_terminated = False
def recv_msg(client_socket):
    global recv_terminated
    global send_terminated
    recv_message = ""
    while recv_message != 'q':
        if send_terminated == False:
            recv_message = str(client_socket.recv(1024).decode("utf-8"))
            time.sleep(1)
            if recv_message == 'q':
                client_socket.send(bytes('q', "utf-8"))
                time.sleep(1)
                print(f'\nConnection terminated.')
                recv_terminated = True
                break
            elif recv_message == '...Recieving a file from peer...':
                print("...Receiving File...")
                file_name = str(client_socket.recv(1024).decode("utf-8"))
                time.sleep(1)
                print("Here 1")
                file_size = str(client_socket.recv(1024).decode("utf-8"))
                time.sleep(1)
                print("Here 2")
                data = str(client_socket.recv(int(file_size)).decode("utf-8"))
                time.sleep(1)
                print("Here 3")
                print(f'peer # 2 received file_name --> {file_name}  file_size --> {file_size}  file_data --> {data}')
                file_name = os.getcwd() + '/server_files/' + file_name
                print(file_name)
                file = open("abc.txt", "w")
                file.write(data)
                file.close()


            print(f'\nMessage recieved from peer  --->  {recv_message}\n>>')
        else:
            break

def chat(client_socket, mode):
    os.system('clear')
    global send_terminated
    global recv_terminated
    recv_thread = threading.Thread(target=recv_msg, args=(client_socket,))
    recv_thread.start()
    send_msg = ' '
    print(f"Press 'q' to disconnect ")
    while send_msg != 'q' and recv_terminated == False:
        send_msg = input('\nEnter a message for peer : ')
        if( send_msg == "upload file"):
            file_name = input("Enter file name : ")
            file = open(file_name, "r")
            file_data = file.read()
            file.close()
            print(f'File data red  ---> {file_data}')
            client_socket.send(bytes("file", "utf-8"))
            time.sleep(1)
            client_socket.send(bytes(file_name, "utf-8"))
            time.sleep(1)
            client_socket.send(bytes(str(len(file_data)), "utf-8"))
            time.sleep(1)
            client_socket.send(bytes(file_data, "utf-8"))
            time.sleep(1)
        else:
            client_socket.send(bytes(send_msg, "utf-8"))
            time.sleep(1)
    send_terminated = True
    if mode == 'wait':
        client_socket.close()


def connect_mode(client_socket):
    os.system('clear')
    online_connections = str(client_socket.recv(2048).decode("utf-8"))
    print(f'Available peers are ---> {online_connections}')
    peer_ip = input(f'Enter peer IP address : ')
    peer_port = input(f'Enter peer port : ')
    print(f'\n...Establishing Connection...')
    print(f'\n...Sending Connection Request...')
    client_socket.send(bytes(peer_ip, "utf-8"))
    time.sleep(1)
    client_socket.send(bytes(peer_port, "utf-8"))
    time.sleep(1)
    print(f'Connecting with {peer_ip} on port {peer_port}')
    time.sleep(5)
    print(f'\n...Connection Established...')
    print(f'\n...Wait for the chat window to open...')
    chat(client_socket, 'connect')

def wait_connection_mode(client_ip, client_port):
    os.system('clear')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((client_ip, int(client_port) ))
    server_socket.listen(10)
    print(f'...Waiting for the connection...')
    peer, peer_information = server_socket.accept()
    print(f'Connected with peer {peer_information[0]} {peer_information[1]}')
    print(f'...wait for the chat window to open...')
    time.sleep(5)
    chat(peer, 'wait')
    peer.close()




client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((sys.argv[1], int(sys.argv[2])) )
while True:
    os.system('clear')
    print(f'There are two modes for the client,')
    print(f'1. Wait connection mode')
    print(f'2. Connect mode')
    mode = input(f"Enter '1' for 'Wait connection mode' and '2' for 'Connect mode' : ")
    if mode == '1':
        client_socket.send(bytes('wait', "utf-8"))
        time.sleep(1)
        client_ip = str(client_socket.recv(1024).decode("utf-8"))
        time.sleep(1)
        client_port = int(input('Enter port number to start listening : '))
        wait_connection_mode(client_ip, client_port)
    elif mode == '2':
        client_socket.send(bytes('connect', "utf-8"))
        time.sleep(1)
        connect_mode(client_socket)


    
    