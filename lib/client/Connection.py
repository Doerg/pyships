from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *
import signal


class Connection(object):
    _server_port = 12346
    _client_port = 12345

    def __init__(self):
        self._connection_listener = Listener(('', self._client_port))
        self._msg_queue = Queue()


    def establish(self, server_ip):
        try:
            with Connection.Timeout():
                self._msg_sender = Client((server_ip, self._server_port))
        except Exception: #general Exception b/c different things can go wrong
            return False

        server_connection = self._connection_listener.accept()
        self._connection_listener.close()
        self._msg_listener = MessageListener(self._msg_queue, server_connection)
        self._msg_listener.start()

        return True


    def has_message(self):
        return not self._msg_queue.empty()


    def setup_identification(self, player_name):
        self._send_message(NameMessage(player_name))
        answer = self._get_message()
        self._player_id = answer.player_id
        return answer.opponent_name


    def inform_exit(self):
        self._send_message(ExitMessage(self._player_id))


    def _get_message(self):
        msg = self._msg_queue.get()
        self._msg_queue.task_done()
        return msg


    def _send_message(self, msg):
        self._msg_sender.send(msg)



    class Timeout:
        def __init__(self, seconds=1, error_message='Timeout'):
            self._seconds = seconds
            self._error_message = error_message

        def _handle_timeout(self, signum, frame):
            raise Connection.TimeoutError(self._error_message)

        def __enter__(self):
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self._seconds)

        def __exit__(self, type, value, traceback):
            signal.alarm(0)


    class TimeoutError(Exception):
        pass