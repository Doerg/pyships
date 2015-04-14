import socket
import logging


class Connection:
    def __init__(self, host, port):
        logging.debug('init socket with %s:%i', host, port)
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None

    def establish(self):
        if self.connected:
            logging.warning('Already connected!')
            return

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except socket.error as msg:
            logging.error(msg)
            self.socket = None
        else:
            self.connected = True

    def listen(self):
        while True:
            msg = self.socket.recv(1024)

    def disconnect(self):
        if self.socket:
            self.socket.close()

        self.connected = False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(filename)s:%(funcName)s:%(message)s")

    conn = Connection('127.0.0.1', 12345)
    try:
        conn.establish()
    except KeyboardInterrupt:
        conn.disconnect()

    conn.disconnect()
