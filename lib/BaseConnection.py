from queue import Queue
from threading import Thread


class BaseConnection(object):
    """
    common connection interface used by both the game client and the server.
    """
    _server_port = 12346    #ports for listeners
    _client_port = 12345

    def __init__(self):
        self._msg_queue = Queue()


    def has_message(self):
        """
        returns whether a message is available in the queue.
        :return: True when message is available in the queue, False otherwise
        """
        return not self._msg_queue.empty()


    def _get_message(self):
        """
        returns the oldest message in the message queue. blocks until a
        message is available.
        :return: the oldest message in the message queue
        """
        msg = self._msg_queue.get()
        self._msg_queue.task_done()
        self._abortion_check(msg) #each message might signal some sort of exit
        return msg


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
                for termination_type in (self._termination_messages):
                    if isinstance(msg, termination_type):
                        self._connection.close()
                        return