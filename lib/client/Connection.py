from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *
from CustomExceptions import *
import signal


class Connection(object):
    """
    connection interface used by the game client.
    """
    _server_port = 12346
    _client_port = 12345

    def __init__(self):
        self._msg_queue = Queue()


    def establish(self, server_ip):
        """
        sets up message listener/sender objects for communication with the
        server.
        :param server_ip: the ip of the server
        :return: True is the connection could be established, False otherwise
        """
        with Listener(('', self._client_port)) as connection_listener:
            try:
                with Connection.Timeout():
                    self._msg_sender = Client((server_ip, self._server_port))
            except Exception: #general b/c different things can go wrong
                return False
            server_connection = connection_listener.accept()

        self.MessageListener(self._msg_queue, server_connection).start()
        return True


    def setup_identification(self, player_name):
        """
        tells the server the local player's name, receives the remote player's
        name in return.
        :param player_name: the name of the local player
        :return: the name of the opponent
        """
        self._send_message(NameMessage(player_name))
        answer = self._get_message()
        self.player_id = answer.player_id
        return answer.opponent_name


    def inform_exit(self):
        """
        informs the server that the local player terminated the program.
        """
        self._send_message(ExitMessage(self.player_id))


    def send_placements(self, ship_placements):
        """
        sends the server the local player's ship placements.
        :param ship_placements: the local player's ship placements
        """
        self._send_message(PlacementMessage(self.player_id, ship_placements))


    def acknowledge_opponent_placements(self):
        """
        waits for message acknowledging that the remote player finished ship
        placements.
        """
        self._get_message()


    def deliver_shot(self, shot_coords):
        """
        sends the server coordinates of a shot taken by the local player.
        returns the result of that shot.
        :param shot_coords: the coordinates of the shot
        :return: the result of the shot
        """
        if self.has_message(): #can only be player exit or server shutdown here
            self._get_message()
        self._send_message(ShotMessage(self.player_id, shot_coords))
        return self._get_message()


    def receive_shot(self):
        """
        returns the result of a shot taken by the remote player.
        :return: the result of a shot taken by the remote player
        """
        return self._get_message()


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


    def _abortion_check(self, message):
        """
        checks whether the given message signals the exit of the remote player
        or the shutdown of the pyships server. raises the appropriate exception
        if either is the case.
        :param message: the message to be checked
        """
        if isinstance(message, ExitMessage):
            raise OpponentLeft
        if isinstance(message, ShutdownMessage):
            raise ServerShutdown


    def _send_message(self, message):
        """
        sends the given message out to the pyships server.
        :param message: the message to be sent
        """
        self._msg_sender.send(message)


    class Timeout:
        """
        context manager class usable via with-statement. can limit the execution
        of the statement body a certain amount of seconds. raises a TimeoutError
        if the execution of the body has not been able to complete during the
        given timeframe.
        """
        def __init__(self, seconds=1):
            self._seconds = seconds

        def _handle_timeout(self, signum, frame):
            raise Connection.TimeoutError()

        def __enter__(self):
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self._seconds)

        def __exit__(self, type, value, traceback):
            signal.alarm(0)


    class MessageListener(Thread):
        """
        daemon thread that puts all incoming messages into a message queue.
        """
        def __init__(self, msg_queue, connection):
            Thread.__init__(self)
            self.daemon = True  #causes thread to exit once main thread exits
            self._msg_queue = msg_queue
            self._connection = connection

        def run(self):
            while True:
                msg = self._connection.recv()
                self._msg_queue.put(msg)
                for msg_type in (ExitMessage, ShutdownMessage):
                    if isinstance(msg, msg_type):
                        self._connection.close()
                        return