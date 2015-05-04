from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
from BaseConnection import BaseConnection
import logging


class Connection(BaseConnection):
    """
    connection interface used by the game client.
    """
    def establish(self):
        """
        listens for two connections and sets up a message listener and message
        sender for each connection. the listeners and senders will be ordered
        by id.
        """
        self._msg_listeners = []
        self._msg_senders = []

        with Listener(('', self._server_port)) as connection_listener:
            logging.info('listening for connections...')

            self._setup_connection(connection_listener)  #1st client connection

            while True:                                  #2nd client connection
                try:
                    with BaseConnection.Timeout():
                        self._setup_connection(connection_listener)
                        break
                except TimeoutError:
                    pass
                if self._msg_listeners[0].poll(): #true if 1st client terminated
                    logging.info('client left again')
                    raise OpponentLeft

        self.established = True


    def _setup_connection(self, connection_listener):
        """
        listens for a client to connect to the server and sets up a message
        listener and sender to that client once connected.
        :param connection_listener: the connection listener
        """
        self._msg_listeners.append(connection_listener.accept())
        client_ip = connection_listener.last_accepted[0]
        self._msg_senders.append(Client((client_ip, self._client_port)))
        logging.info('client with ip %s logged on' % client_ip)


    def assign_ids(self):
        """
        assigns each player his id.
        """
        for player_id in range(2):
            self._msg_senders[player_id].send(IDMessage(player_id))


    def name_exchange(self):
        """
        for each player, it receives a name message and delivers it to
        the other.
        """
        for player_id in range(2):
            other_id = self._other_player_id(player_id)
            name_msg = self._get_message(player_id)
            self._msg_senders[other_id].send(name_msg)
            logging.info(
                "player '%s' received id %d" %
                (name_msg.player_name.decode('utf-8'), player_id)
            )


    def exchange_placements(self):
        """
        receives a placement message from each player. for each message, the
        other player will be informed about the arrival of the opponent's
        placements by an empty placement message (containing no data).
        :return: a list containing both player's ship placements, ordered by id
        """
        logging.info('Waiting for ship placements...')
        ship_placements = [None, None]
        for _ in range(2):
            msg = self._get_message()
            ship_placements[msg.player_id] = msg.coords
            other_id = self._other_player_id(msg.player_id)
            self._msg_senders[other_id].send(PlacementMessage())
            logging.info(
                'player %d placed the following ships: %s' %
                (msg.player_id, msg.coords)
            )
        return ship_placements


    def receive_shot(self, shooter_id):
        """
        receives a shot message of the player with the given id. the shot's
        coordinates will be extracted from the message and returned.
        :param shooter_id: the id of the player to receive the shot message from
        :return: the coordinates of the shot
        """
        logging.info('Waiting for player %d to shoot...' % shooter_id)
        coords = self._get_message(shooter_id).coords
        logging.info(
            'player %d shot at coordinates %s' % (shooter_id, coords)
        )
        return coords


    def inform_shot_result(self, coords, is_hit, game_over, destroyed_ship):
        """
        send a shot result message out to both players.
        :param coords: the coordinates of the shot
        :param is_hit: True if the shot was a hit, False otherwise
        :param game_over: True if the shot ended the game, False otherwise
        :param destroyed_ship: if a ship was destroyed by the shot, this will
        contain the ship's coordinates. otherwise it will be None
        """
        if game_over:
            logging.info('game over')
        self._send_all(
            ShotResultMessage(coords, is_hit, game_over, destroyed_ship)
        )


    def exchange_rematch_willingness(self):
        """
        waits for a rematch message by each player. once a message arrives, the
        other player will be informed about it.
        """
        for _ in range(2):
            msg = self._get_message()
            logging.info('player %d agrees to a rematch' % msg.player_id)
            other_id = self._other_player_id(msg.player_id)
            self._msg_senders[other_id].send(RematchMessage())


    def inform_shutdown(self):
        """
        sends a shutdown message out to both players.
        """
        self._send_all(ShutdownMessage())


    def close(self):
        """
        closes all message senders and listeners.
        """
        for connection in self._msg_senders + self._msg_listeners:
            connection.close()


    def _send_all(self, message):
        """
        sends the given message to both players.
        :param message: the message to be sent
        """
        for sender in self._msg_senders:
            sender.send(message)


    def _get_message(self, player_id=None):
        """
        if player_id is given, will return the oldest message in the player's
        message listener. if no player_id is given, it will return the oldest
        message of either listener.
        :param player_id: the id of the player to get the message from
        :return: the oldest message of a particular player
        """
        if player_id != None:
            return self._read_message(self._msg_listeners[player_id])
        else:
            while True:
                for player_id in range(2):
                    if self._msg_listeners[player_id].poll():
                        return self._read_message(
                            self._msg_listeners[player_id]
                        )


    def _read_message(self, msg_listener):
        """
        returns a message read from the given message listener.
        :param msg_listener: the listener to read the message from
        :return: the oldest message of this listener
        """
        message = msg_listener.recv()
        self._abortion_check(message) #message might signal player exit
        return message


    def _abortion_check(self, message):
        """
        checks whether the given message signals the exit of a remote player.
        if that is the case, it informs the other remote player about the exit
        and raises the appropriate exception.
        :param message: the message to be checked
        """
        if isinstance(message, ExitMessage):
            other_id = self._other_player_id(message.player_id)
            self._msg_senders[other_id].send(ExitMessage())
            logging.info('player %d left the game' % message.player_id)
            raise OpponentLeft


    def _other_player_id(self, player_id):
        """
        calculates the other player's id based on the given player id. returns
        1 if player_id is 0 or 0 if player_id is 1.
        :param player_id: the id of a player
        :return: the id of the other player
        """
        return abs(player_id - 1)