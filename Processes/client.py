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
    while recv_message != 'q' and send_terminated == False:
        try:
            recv_message = str(client_socket.recv(1024).decode("utf-8"))
            if recv_message == 'q':
                client_socket.send(bytes('q', "utf-8"))
                print(f'\nConnection terminated.')
                recv_terminated = True
                break
            print(f'\nMessage recieved from peer  --->  {recv_message}\n>>')
        except socket.error as msg:
            print(f'Socket Error: {msg}')

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
        client_socket.send(bytes(send_msg, "utf-8"))
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
    client_socket.send(bytes(peer_port, "utf-8"))
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
    print(f'There are three modes for the client,')
    print(f'1. Wait connection mode')
    print(f'2. Connect mode')
    print(f'3. FTP File upload')
    print(f'4. FTP File download')
    mode = input(f"Select mode : ")
    if mode == '1':
        client_socket.send(bytes('wait', "utf-8"))
        client_ip = str(client_socket.recv(1024).decode("utf-8"))
        client_port = int(input('Enter port number to start listening : '))
        wait_connection_mode(client_ip, client_port)
        recv_terminated = False
        send_terminated = False

    elif mode == '2':
        client_socket.send(bytes('connect', "utf-8"))
        connect_mode(client_socket)
        recv_terminated = False
        send_terminated = False
    
    elif mode == '3':
        client_socket.send(bytes('file upload', "utf-8"))
        file_name = input('\nEnter file name :')
        client_socket.send(bytes(file_name, "utf-8"))
        with open(file_name, "rb") as file:
            file_data = file.read()
            client_socket.send(file_data)
            print(f'...Uploading file...')
            time.sleep(5)
            print(f'{file_name} is uploaded successfully')
            file.close()



    elif mode == '4':
        client_socket.send(bytes('file download', "utf-8"))
        file_name = input('\nEnter file name :')
        client_socket.send(bytes(file_name, "utf-8"))
        file_data = bytes()
        print(f'\n...Downloading file from the server...')
        print(f'...Please wait...')
        client_socket.settimeout(5) # setting recv timeout
        while True:
            try:
                data = client_socket.recv(1024)
                file_data = file_data + data
            except socket.timeout:  # run when recv timeout expires
                break
        client_socket.settimeout(None)
        with open(file_name, "wb") as file:
            file.write(file_data)
            file.close()
            