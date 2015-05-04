from CustomExceptions import TimeoutError
import signal


class BaseConnection(object):
    """
    common connection class to be inherited from both client and server
    connections.
    """
    _server_port = 12346    #ports for listeners
    _client_port = 12345

    def __init__(self):
        self.established = False


    class Timeout:
        """
        context manager class usable via with-statement. can limit the execution
        of the statement body a certain amount of seconds. raises a TimeoutError
        if the execution of the body has not been able to complete during the
        given timeframe.
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