import socket
import threading

addr1 = ('127.0.0.1', 1000)
addr2 = ('127.0.0.1', 1100)
addr3 = ('127.0.0.1', 1200)
dic = {"net.txt": [addr1, addr2], "network.txt": [addr1, addr3], "seeds.txt": [addr2, addr3]}


def parse(data):
    query_update = data[0]  # 0: this message is a query, 1: this message is an update
    message = data[1]
    return query_update, message


class Echo(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address

    def run(self):
        while True:
            modifiedMessage = self.conn.recv(1024).decode()
            query_update, message = parse(modifiedMessage.split())
            filename, addr = message.split('+=')
            name, port = addr.split(',')
            try:
                if (name, int(port)) in dic[filename]:
                    dic[filename].remove((name, int(port)))
                if int(query_update) == 0:
                    a = dic[filename]
                    resp = ""
                    for i in range(len(a)):
                        resp += str(a[i][0])+" "+str(a[i][1])+" "
                    self.conn.send(resp.encode())
                elif int(query_update) == 1:
                    dic[filename].append((name, int(port)))
                    print('Update!')
                    print(dic)
            except KeyError:
                self.conn.send('404'.encode())
            self.conn.close()
            break


def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 12000))
    sock.listen(10)
    print('The server is ready to receive')
    print(dic)
    while True:
        conn, address = sock.accept()
        Echo(conn, address).start()


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        pass

