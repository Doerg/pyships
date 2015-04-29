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
        self._msg_senders = []


    def establish(self):
        with Listener(('', self._server_port)) as connection_listener:
            for _ in range(2):
                client_connection = connection_listener.accept()
                self.MessageListener(self._msg_queue, client_connection).start()
                client_ip = connection_listener.last_accepted[0]
                self._msg_senders.append(Client((client_ip, self._client_port)))


    def inform_shutdown(self):
        for sender in self._msg_senders:
            sender.send(ShutdownMessage())


    def setup_identification(self):
        player_names = []
        for player_id in range(2):
            other_id = self._other_player_id(player_id)
            name_msg = self._get_message()
            player_name = name_msg.player_name
            player_names.append(player_name)
            self._msg_senders[other_id].send(IDMessage(other_id, player_name))

        return player_names


    def exchange_placements(self):
        pass


    def receive_shot(self):
        pass


    def inform_shot_result(self):
        pass


    def _abortion_check(self, message):
        """
        checks whether the given message signals the exit of a remote player.
        if that is the case, it informs the other remote player about the exit
        and raises the appropriate exception.
        :param message: the message to be checked
        """
        if isinstance(message, ExitMessage):
            other_id = _other_player_id(ExitMessage.player_id)
            self._msg_senders[other_id].send(ExitMessage())
            raise OpponentLeft


    def _other_player_id(self, player_id):
        return abs(player_id - 1)


    class MessageListener(BaseConnection.MessageListener):
	    """
	    daemon thread that puts all incoming messages into a message queue.
	    """
	    def __init__(self, msg_queue, connection):
	        super().__init__(msg_queue, connection)
	        self._termination_messages = (ExitMessage,)