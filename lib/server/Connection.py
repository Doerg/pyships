from multiprocessing.connection import Client, Listener
from Messages import *
from CustomExceptions import *
from BaseConnection import BaseConnection


class Connection(BaseConnection):
    """
    connection interface used by the game client.
    """
    def establish(self):
        self._msg_listeners = []
        self._msg_senders = []

        with Listener(('', self._server_port)) as connection_listener:
            for _ in range(2):
                self._msg_listeners.append(connection_listener.accept())
                client_ip = connection_listener.last_accepted[0]
                self._msg_senders.append(Client((client_ip, self._client_port)))


    def setup_identification(self):
        return [self._player_name(player_id) for player_id in range(2)]


    def _player_name(self, player_id):
        other_id = self._other_player_id(player_id)
        name_msg = self._get_message(player_id)
        player_name = name_msg.player_name
        self._msg_senders[other_id].send(IDMessage(other_id, player_name))
        return player_name


    def exchange_placements(self):
        ship_placements = [None, None]
        for _ in range(2):
            msg = self._get_message()
            ship_placements[msg.player_id] = msg.coords
            other_id = self._other_player_id(msg.player_id)
            self._msg_senders[other_id].send(PlacementMessage())
        return ship_placements


    def receive_shot(self, shooter_id):
        return self._get_message(shooter_id).coords


    def inform_shot_result(self, coords, is_hit, game_over, destroyed_ship):
        self._send_all(
            ShotResultMessage(coords, is_hit, game_over, destroyed_ship)
        )


    def inform_shutdown(self):
        self._send_all(ShutdownMessage())


    def _send_all(self, msg):
        for sender in self._msg_senders:
            sender.send(msg)


    def _get_message(self, player_id=None):
        """
        if player_id is given, will return the oldest message in the player's
        message listener. if player_id is not given, will return the oldest
        message of both listeners.
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
            raise OpponentLeft


    def _other_player_id(self, player_id):
        return abs(player_id - 1)