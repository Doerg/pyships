from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
from BaseConnection import BaseConnection


class Connection(BaseConnection):
    """
    connection interface used by the game client.
    """
    def establish(self, server_ip):
        """
        sets up message listener/sender objects for communication with the
        server.
        :param server_ip: the ip of the server
        :return: True is the connection could be established, False otherwise
        """
        with Listener(('', self._client_port)) as connection_listener:
            try:
                with BaseConnection.Timeout():
                    self._msg_sender = Client((server_ip, self._server_port))
            except:  #general b/c different things can go wrong
                return False
            self._msg_listener = connection_listener.accept()

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
        self._msg_sender.send(NameMessage(player_name))
        return self._get_message().player_name.decode('utf-8') #came as bytes


    def send_placements(self, ship_placements):
        """
        sends the server the local player's ship placements.
        :param ship_placements: the local player's ship placements
        """
        self._msg_sender.send(
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
        self._msg_sender.send(ShotMessage(shot_coords))
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
        self._msg_sender.send(RematchMessage(self._player_id))


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
        self._msg_sender.send(ExitMessage(self._player_id))


    def has_message(self):
        """
        returns whether there is a message from the server not read yet.
        :return: True if a message from the server is available, False otherwise
        """
        return self._msg_sender.poll()


    def close(self):
        """
        closes both message sender and listener.
        """
        self._msg_sender.close()
        self._msg_listener.close()


    def _get_message(self):
        """
        returns the oldest message in the message queue. blocks until a
        message is available.
        :return: the oldest message in the message queue
        """
        message = self._msg_listener.recv()
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