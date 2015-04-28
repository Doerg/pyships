from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *
from CustomExceptions import *


class Connection(object):
    """
    connection interface used by the game client.
    """
    _server_port = 12346
    _client_port = 12345

    def __init__(self):
        self._msg_queue = Queue()
        self._senders = []


    def establish(self):
    	with Listener(('', self._server_port)) as connection_listener:
    		for _ in range(2):
    			client_connection = connection_listener.accept()
    			self.MessageListener(self._msg_queue, client_connection).start()
    			client_ip = connection_listener.last_accepted[0]
    			self._senders.append(
    				Client((client_ip, self._client_port))
    			)


    class MessageListener(Thread):
        """
        daemon thread that puts all incoming messages into a message queue.
        """
        def __init__(self, msg_queue, connection):
            Thread.__init__(self)
            self.daemon = True  # causes thread to exit once main thread exits
            self._msg_queue = msg_queue
            self._connection = connection

        def run(self):
            while True:
                msg = self._connection.recv()
                self._msg_queue.put(msg)
                if isinstance(msg, ExitMessage):
                    self._connection.close()
                    return