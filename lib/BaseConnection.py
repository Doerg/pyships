class BaseConnection(object):
    """
    common connection class to be inherited from both client and server
    connections.
    """
    _server_port = 12346    #ports for listeners
    _client_port = 12345

    def __init__(self):
        self.established = False