from threading import Thread


class NameMessage(object):
    def __init__(self, player_name):
        self.player_name = player_name


class IDMessage(object):
    def __init__(self, player_id, opponent_name):
        self.opponent_name = opponent_name
        self.player_id = player_id


class ExitMessage(object):
    def __init__(self, player_id):
        self.player_id = player_id


class ResultMessage(object):
    def __init__(self, result):
        self.result = result


class PlacementMessage(object):
    #empty parameters as indication by server that opponent finished placement
    def __init__(self, player_id=None, coords=None):
        self.player_id = player_id
        self.coords = coords


class MessageListener(Thread):
    def __init__(self, msg_queue, connection):
        Thread.__init__(self)
        self.daemon = True  # causes thread to exit once main thread exits
        self._msg_queue = msg_queue
        self._connection = connection

    def run(self):
        while True:
            msg = self._connection.recv()
            self._msg_queue.put(msg)
            if isinstance(msg, ExitMessage):
                self._connection.close()
                return