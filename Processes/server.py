import socket
import sys
import os
import threading
import time



isTerminated = False
def API(first_peer, second_peer, current_peer_context):
    global isTerminated
    recv_message = " "
    while recv_message != 'q':
        if isTerminated == True:
            break
        try:
            if current_peer_context == 'first':
                recv_message = str(first_peer.recv(1024).decode("utf-8")) 
                # recv from client # 1
                second_peer.send(bytes(recv_message, "utf-8"))            
                # send received message to client # 2
            elif current_peer_context == 'second':
                recv_message = str(second_peer.recv(1024).decode("utf-8")) 
                # recv from client # 2
                first_peer.send(bytes(recv_message, "utf-8"))   
                # send received message to client # 1
        except socket.error as msg:
            print(f'Socket Error: {msg}')

    isTerminated = True
    first_peer.close()
    second_peer.close()


clients_list = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# helps in fast and separate non concatenated sending and recieving of data.
server_socket.bind(('127.0.0.1', int(sys.argv[1]) ))
server_socket.listen(10)
print("Server listening on port # " + str(sys.argv[1]) )
print("Note: Enter 'q' to terminate connections")
while True:
    first_peer, client_information = server_socket.accept()
    clients_list.append(client_information)
    if os.fork() == 0 :
        server_socket.close() 
        print(f"\nServer got a new connection with ip {client_information[0]} and port {client_information[1]}")

        while True:
            mode = str(first_peer.recv(1024).decode("utf-8"))
            if mode == 'connect':
                first_peer.send(bytes(str(clients_list), "utf-8"))
                second_peer_ip = '' 
                second_peer_port = ''
                second_peer_ip = str(first_peer.recv(1024).decode("utf-8"))
                first_peer.settimeout(2)
                second_peer_port = str(first_peer.recv(1024).decode("utf-8"))
                second_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                second_peer.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                try:
                    second_peer.connect((second_peer_ip, int(second_peer_port) ))
                    first_peer_thread = threading.Thread(target=API, args=(first_peer, second_peer, 'first'))
                    first_peer_thread.start()
                    second_peer_thread = threading.Thread(target=API, args=(first_peer, second_peer, 'second'))
                    second_peer_thread.start()
                except socket.error as msg:
                    print(f'Socket Error: {msg}')

            elif mode == 'wait':
                first_peer.send(bytes(str(client_information[0]), "utf-8"))

            elif mode == 'file upload':
                file_name = first_peer.recv(1024).decode("utf-8")
                file_data = bytes()
                first_peer.settimeout(5) # setting recv timeout
                start = time.time()
                while True:
                    try:
                        data = first_peer.recv(1024)
                        file_data = file_data + data
                    except socket.timeout:  # run when recv timeout expires
                        break
                first_peer.settimeout(None)
                with open("server_files/"+file_name, "wb") as file:
                    file.write(file_data)
                    file.close()
                stop = time.time()
                print(f'{file_name} took {stop-start} seconds for downloading from peer to server.')
                

            elif mode == 'file download':
                file_name = first_peer.recv(1024).decode("utf-8")
                start = time.time()
                with open("server_files/"+file_name, "rb") as file:
                    file_data = file.read()
                    first_peer.send(file_data)
                    print(f'...Sending file to client {client_information[0]} {client_information[1]}...')
                    time.sleep(5)
                    print(f'{file_name} is sent successfully')
                    file.close()
                stop = time.time()
                print(f'{file_name} took {stop-start} seconds to send file to the peer from server.')
                