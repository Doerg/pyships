from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
from BaseConnection import BaseConnection


class Connection(BaseConnection):
    """
    connection interface used by the game client.
    """
    def __init__(self):
        super().__init__()
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


    class MessageListener(BaseConnection.MessageListener):
	    """
	    daemon thread that puts all incoming messages into a message queue.
	    """
	    def __init__(self, msg_queue, connection):
	        super().__init__(msg_queue, connection)
	        self._termination_messages = (ExitMessage,)