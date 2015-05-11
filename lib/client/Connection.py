from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
import signal


class Connection(object):
    """
    connection interface used by the game client.
    """
    _host_port = 12345

    def __init__(self):
        self._connection = None


    @property
    def established(self):
        return self._connection != None


    def wait_for_connection(self):
        """
        as a game host, waits for a client to connect.
        """
        with Listener(('', self._host_port)) as connection_listener:
            self._connection = connection_listener.accept()


    def connect_to_host(self, host_ip):
        """
        sets up connection to a game host.
        :param host_ip: the ip of the game host
        :return: True if the connection could be established, False otherwise
        """
        try:
            with self.Timeout():
                self._connection = Client((host_ip, self._host_port))
        except:  #general b/c different things can go wrong
            return False

        return True


    def exchange_names(self, player_name):
        """
        tells the opponent's client the local player's name, receives the
        remote player's name in return.
        :param player_name: the name of the local player
        :return: the name of the opponent
        """
        self._connection.send(NameMessage(player_name))
        return self._get_message().player_name.decode('utf-8') #came as bytes


    def send_acknowledgement(self):
        """
        acknowledges to the opponent that a desired action took place.
        """
        self._connection.send(AcknowledgementMessage())


    def wait_for_acknowledgement(self):
        """
        waits a for an acknowledging message of the remote player.
        """
        self._get_message()


    def deliver_shot(self, shot_coords):
        """
        sends the opponent's client coordinates of a shot taken by the local
        player. returns the result of that shot.
        :param shot_coords: the coordinates of the shot
        :return: the result of the shot
        """
        if self.has_message(): #can only be remote player exit here
            self._get_message()
        self._connection.send(ShotMessage(shot_coords))
        return self._get_message()


    def receive_shot(self):
        """
        returns the result of a shot taken by the remote player.
        :return: the result of a shot taken by the remote player
        """
        return self._get_message().coords


    def inform_shot_result(self, is_hit, game_over, destroyed_ship):
        """
        sends the opponent's client the result of his last shot.
        :param is_hit: True if the shot was a hit, False otherwise
        :param game_over: True if the shot ended the game, False otherwise
        :param destroyed_ship: if a ship was destroyed by the shot, this will
        contain the ship's coordinates. otherwise it will be None
        """
        self._connection.send(
            ShotResultMessage(is_hit, game_over, destroyed_ship)
        )


    def send_intact_ships(self, fleet):
        """
        sends the opponent's client all the coordinates of the player's ships
        that are still intact.
        :param fleet: the player's fleet
        """
        ship_coords = [ship.full_coords for ship in fleet.intact_ships]
        self._connection.send(RevealMessage(ship_coords))


    def enemy_intact_ships(self):
        """
        returns the ships of the opponent that are still intact after game end.
        :return: the coordinates of the opponent's intact ships
        """
        return self._get_message().coords


    def inform_exit(self):
        """
        informs the opponent's client that the local player terminated the
        program.
        """
        self._connection.send(ExitMessage())


    def has_message(self):
        """
        returns whether there is a message from the opponent's client not read
        yet.
        :return: True if a message is available, False otherwise
        """
        return self._connection.poll()


    def close(self):
        """
        closes the connection to the opponent's client.
        """
        if self.established:
            self._connection.close()
            self._connection = None


    def _get_message(self):
        """
        returns the oldest message of the connection. blocks until a message is
        available.
        :return: the oldest message of the connection
        """
        message = self._connection.recv()
        self._abortion_check(message) #message might signal some sort of exit
        return message


    def _abortion_check(self, message):
        """
        checks whether the given message signals the exit of the remote player.
        raises the appropriate exception that is the case.
        :param message: the message to be checked
        """
        if isinstance(message, ExitMessage):
            raise OpponentLeft


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