# Messenger Application

 Implementation Details
 - A separate child process of server (client handler) is created whenever a new client is connected with the server.
 - A client can select wait mode in which it tells the server handler (a child process of the server with whom the client is connected) a port number
on which it will listen for other peers (clients) to connect with it.
Note: A client should only select wait mode only when it has exposed a port for communication over the internet from its gateway | router settings 
otherwise wait will only work within its localmachine | localhost and it will wait for other clients on localhost and not at the hosted server on cloud.
- A client can select connect mode in which it tells the client handler (a child process of server) that he want to connect with this 'abc' ip address on 
some 'xyz' port number.
- A client can select upload mode to upload files from his current directory to the FTP server.
- A client can select download mode to download files in its current directory from the FTP server.

 Features
 - Sending and Recieving of messages simulataneously without blocking.
 - File transfer (Upload, and Download) functionality for any type of files (JPG,TXT,MP3,MP4 ETC).
 - One-one secure communication via a proxy server hosted at ubuntu server 20.04 on azure.
 - Peer-peer secure communication using private IP addresses using global virtual network peering.
