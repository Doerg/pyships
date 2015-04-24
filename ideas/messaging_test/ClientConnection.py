from queue import Queue
from multiprocessing.connection import Client, Listener
from netifaces import ifaddresses
from Messages import *


class Connection(object):
    _port = 12345

    def establish(self, server_ip):
        machine_ip = ifaddresses('eth0')[2][0]['addr']

        try:
            self._msg_sender = Client((server_ip, self._port))
            self._msg_sender.send(GreetingsMessage('player xy', machine_ip))
        except ConnectionRefusedError:
            return False

        self._server_listener = Listener((machine_ip, self._port))
        self._msg_queue = Queue()
        self._msg_listener = MessageListener(
            self._msg_queue, self._server_listener.accept()
        )
        self._msg_listener.start()

        return True


    def server_message(self):
        msg = self._msg_queue.get()
        self._msg_queue.task_done()
        return msg


    def send_message(self, msg):
        self._msg_sender.send(msg)


    def tear_down(self):
        self._server_listener.close()
        self._msg_listener.join()