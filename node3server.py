from socket import *
import os

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(10)
print('The server is ready to receive')
while 1:
    connectionSocket, addr = serverSocket.accept()
    modifiedMessage = connectionSocket.recv(1024).decode().split()
    totalnum = int(modifiedMessage[0])
    neednum = int(modifiedMessage[1])
    filename = modifiedMessage[2]
    str = open(os.getcwd()+"\\node3\\"+filename, 'rb').read()
    str = str[int(len(str)/totalnum*neednum):int(len(str)/totalnum*(neednum+1))]
    connectionSocket.send(str)
    print('Uploading {0}({1}/{2})'.format(filename, neednum+1, totalnum))
