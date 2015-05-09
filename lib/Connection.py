from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
import signal


class Connection(object):
    """
    connection interface used by the game client.
    """
    _server_port = 12346    #ports for listeners
    _client_port = 12345

    def __init__(self):
        self.established = False


    def establish(self, server_ip):
        """
        sets up connection object for communication with the server.
        :param server_ip: the ip of the server
        :return: True is the connection could be established, False otherwise
        """
        try:
            with self.Timeout():
                self._connection = Client((server_ip, self._server_port))
        except:  #general b/c different things can go wrong
            return False

        return True


    def obtain_player_id(self):
        """
        listens for an id message by the server and extracts the assigned id.
        """
        self._player_id = self._get_message().player_id
        self.established = True  #considered established once id received
        return self._player_id


    def exchange_names(self, player_name):
        """
        tells the server the local player's name, receives the remote player's
        name in return.
        :param player_name: the name of the local player
        :return: the name of the opponent
        """
        self._connection.send(NameMessage(player_name))
        return self._get_message().player_name.decode('utf-8') #came as bytes


    def send_placements(self, ship_placements):
        """
        sends the server the local player's ship placements.
        :param ship_placements: the local player's ship placements
        """
        self._connection.send(
            PlacementMessage(self._player_id, ship_placements)
        )


    def acknowledge_opponent_placements(self):
        """
        waits a for message acknowledging that the remote player finished ship
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
        self._connection.send(ShotMessage(shot_coords))
        return self._get_message()


    def receive_shot(self):
        """
        returns the result of a shot taken by the remote player.
        :return: the result of a shot taken by the remote player
        """
        return self._get_message()


    def enemy_intact_ships(self):
        """
        returns the ships of the opponent that are still intact after game end.
        :return: the coordinates of the opponent's intact ships
        """
        return self._get_message().coords


    def inform_rematch_willingness(self):
        """
        informs the opponent that the player wants a rematch.
        """
        self._connection.send(RematchMessage(self._player_id))


    def acknowledge_rematch_willingness(self):
        """
        waits a for message acknowledging that the remote player is willing to
        play a rematch.
        """
        self._get_message()


    def inform_exit(self):
        """
        informs the server that the local player terminated the program.
        """
        self._connection.send(ExitMessage(self._player_id))


    def has_message(self):
        """
        returns whether there is a message from the server not read yet.
        :return: True if a message from the server is available, False otherwise
        """
        return self._connection.poll()


    def close(self):
        """
        closes both message sender and listener.
        """
        self._connection.close()


    def _get_message(self):
        """
        returns the oldest message in the message queue. blocks until a
        message is available.
        :return: the oldest message in the message queue
        """
        message = self._connection.recv()
        self._abortion_check(message) #message might signal some sort of exit
        return message


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


    class Timeout:
        """
        context manager class usable via with-statement. can limit the execution
        of the statement body to a certain amount of seconds. raises a
        TimeoutError if the execution of the body has not been able to complete
        during the given time frame.
        """
        def __init__(self, seconds=1):
            self._seconds = seconds

        def _handle_timeout(self, signum, frame):
            raise TimeoutError

        def __enter__(self):
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self._seconds)

        def __exit__(self, type, value, traceback):
            signal.alarm(0)