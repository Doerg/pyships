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


class ConnectionAborted(Exception):
    """
    signal that player canceled connection and exited from title screen.
    """
    pass


class TimeoutError(Exception):
    """
    signal that the connection to the opponent's client timed out.
    """
    pass


class OpponentLeft(Exception):
    """
    signal program termination by the remote user.
    """
    pass
