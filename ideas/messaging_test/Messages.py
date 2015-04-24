from threading import Thread


class GreetingsMessage(object):
    def __init__(self, player_name, ip):
        self.player_name = player_name
        self.ip = ip

class ResultMessage(object):
    def __init__(self, result):
        self.result = result

class ExitMessage(object):
    pass

class PlacementMessage(object):
    def __init__(self, coords):
        self.coords = coords


class MessageListener(Thread):
    def __init__(self, msg_queue, connection):
        self._msg_queue = msg_queue
        self._connection = connection
        Thread.__init__(self)

    def run(self):
        while True:
            msg = self._connection.recv()
            self._msg_queue.put(msg)
            if isinstance(msg, ExitMessage):
                self._connection.close()
                return