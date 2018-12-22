from socket import *
import os

addr = ('127.0.0.1', 1000)
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
# input web domain and type and combine them as a string and send to sever
filename = input('Input the filename:')

clientSocket.send(('0 {0}+={1},{2}'.format(filename, addr[0], addr[1])).encode())
while 1:
    modifiedSentence = clientSocket.recv(1024).decode()
    if modifiedSentence:
        if modifiedSentence=='404':
            clientSocket.close()
            print('No such file found!')
            break
        else:
            ans = b''
            mess = ""
            list = []
            j = 0
            while j < len(modifiedSentence.split()):
                list.append((modifiedSentence.split()[j], int(modifiedSentence.split()[j+1])))
                j = j+2
            print("Download from: "+str(list))
            for i in range(len(list)):
                mess=str(len(list))+" "+str(i)+" "+filename
                clientSocket.close()
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect(list[i])
                clientSocket.send(mess.encode())
                modifiedSentence = clientSocket.recv(1048576)
                ans = ans + modifiedSentence
            f = open(os.getcwd()+"\\node1\\"+filename, 'w')
            f.write(ans.decode())
            f.close()
            clientSocket.close()
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(('1 {0}+={1},{2}'.format(filename, addr[0], addr[1])).encode())
            break
