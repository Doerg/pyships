class ProgramExit(Exception):
    """
    signal program termination by local user.
    """
    pass

class OpponentLeft(Exception):
    """
    signal program termination by remote user.
    """
    pass

class ServerShutdown(Exception):
    """
    signal shutdown of pyships server.
    """
    pass

class ConnectionAborted(Exception):
    """
    signal that player canceled connection and exited from title screen.
    """
    pass

class GameOver(Exception):
    """
    signal that one of the two players won.
    """
    pass


class TimeoutError(Exception):
    """
    signal that the connection to the server timed out.
    """
    pass