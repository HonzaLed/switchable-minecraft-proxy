from threading import Thread
import socket
import sys
import os

class Proxy2Server(Thread):

    def __init__(self, host, port):
        super(Proxy2Server, self).__init__()
        self.game1 = None # game client socket not known yet
        self.game2 = None # game client socket not known yet
        self.port = port
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    # run in thread
    def run(self):
        while True:
            data = self.server.recv(4096)
            if data:
                try:
                    self.game1.sendall(data)
                    self.game2.sendall(data)
                except Exception as e:
                    print('server[{}]'.format(self.port), e)
                # forward to client

class Game2Proxy(Thread):

    def __init__(self, host, port, send, id):
        super(Game2Proxy, self).__init__()
        self.server = None # real server socket not known yet
        self.port = port
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        self.send=send
        self.id=id
        # waiting for a connection
        self.game, addr = sock.accept()
        print("New connection from",addr,"!")

    def run(self):
        print("[Game2Proxy] Starting Game2Proxy thread id",self.id)
        while True:
            data = self.game.recv(4096)
            if data:
                try:
                    if self.send:
                        self.server.sendall(data)
                        print("[{}] sending [{}] -> {}".format(self.id, self.port, data.hex()))
                    else:
                        print("[{}] [{}] -> {}".format(self.id, self.port, data.hex()))
                except Exception as e:
                    print('[{}] error client[{}]'.format(self.id, self.port), e)

class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        self.running = False
        self.g2p1=None
        self.g2p2=None

    def run(self):
        while True:
            print("[proxy({})] setting up".format(self.port))

            self.g2p1 = Game2Proxy(self.from_host, self.port, send=True, id=1) # waiting for client 1
            print("[proxy({})] connection established with client 1".format(self.port))

            self.g2p2= Game2Proxy(self.from_host, self.port+1, send=False, id=2) # waiting for client 2
            print("[proxy({})] connection established with client 2".format(self.port+1))

            self.p2s = Proxy2Server(self.to_host, self.port)

            print("[proxy({})] connection established".format(self.port))

            self.g2p1.server = self.p2s.server
            self.g2p2.server= self.p2s.server

            self.p2s.game1 = self.g2p1.game
            self.p2s.game2 = self.g2p2.game

            self.running = True

            self.g2p1.start()
            self.g2p2.start()

            self.p2s.start()

try:
    port=int(sys.argv[2])
except:
    port=25565
server = Proxy('0.0.0.0', sys.argv[1], port)
server.start()

while True:
    try:
        
        cmd = input('$ ')
        if cmd[:4] == 'quit':
            os._exit(0)

        elif cmd[0:2] == '1':
            server.g2p2.send = False
            server.g2p1.send = True
            print("Switched to 1!")
            print("server.g2p2.send", server.g2p2.send)
            print("server.g2p1.send", server.g2p1.send)

        elif cmd[0:2] == '2':
            server.g2p1.send = False
            server.g2p2.send = True
            print("Switched to 2!")
            print("server.g2p2.send", server.g2p2.send)
            print("server.g2p1.send", server.g2p1.send)

    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print(e)



