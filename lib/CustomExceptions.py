class ProgramExit(Exception):
    """
    signal program termination by local user.
    """
    pass


class PlayAgain(Exception):
    """
    signal that both players want a rematch.
    """
    pass


class TimeoutError(Exception):
    """
    signal that the attempt to establish a connection timed out.
    """
    pass


class OpponentLeft(Exception):
    """
    signal program termination by the remote user.
    """
    pass


class ServerShutdown(Exception):
    """
    signal shutdown of pyships host listing server.
    """
    pass