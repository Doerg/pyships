import socket
from threading import Thread
import logging


class PyShipsServer:
    def __init__(self, host, port):
        self.socket = None
        self.running = False
        self.host = host
        self.port = port
        self.clients = []

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logging.info('listening on %s:%i', self.host, self.port)
        self.running = True

        while len(self.clients) < 2:
            conn, addr = self.socket.accept()
            client = ClientHandler(conn, addr)
            self.clients.append(client)
            client.start()

    def stop(self):
        self.socket.close()
        for client in self.clients:
            client.join()

        self.running = False


class ClientHandler(Thread):
    def __init__(self, conn, addr):
        super(ClientHandler, self).__init__()
        self.conn = conn
        self.addr = addr
        
    def start(self):
        print('start')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)#, format="%(levelname)s:%(filename)s:%(funcName)s:%(message)s")

    server = PyShipsServer('127.0.0.1', 12345)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
