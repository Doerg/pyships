from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import MessageListener


class Connection(object):
    _server_port = 12346
    _client_port = 12345

    def __init__(self):
        self._connection_listener = Listener(('', self._client_port))
        self._msg_queue = Queue()


    def establish(self, server_ip):
        try:
            self._msg_sender = Client((server_ip, self._server_port))
        except ConnectionRefusedError:
            return False

        server_connection = self._connection_listener.accept()
        self._msg_listener = MessageListener(self._msg_queue, server_connection)
        self._msg_listener.start()

        return True


    def get_message(self):
        msg = self._msg_queue.get()
        self._msg_queue.task_done()
        return msg


    def send_message(self, msg):
        self._msg_sender.send(msg)


    def tear_down(self):
        self._connection_listener.close()
        self._msg_listener.join()