class HostsMessage(object):
    """
    can be used by a client to query the available game hosts from the server,
    or it can be used by the server to deliver the available game hosts to the
    client.
    """
    def __init__(self, available_hosts=None):
        if available_hosts != None:
            self.available_hosts = available_hosts


class NameMessage(object):
    """
    delivers the name of one player to the other player's client.
    """
    def __init__(self, player_name):
        self.player_name = player_name


class ShotMessage(object):
    """
    delivers the coordinates of a shot taken by one player to the other
    player's client.
    """
    def __init__(self, coords):
        self.coords = coords


class ShotResultMessage(object):
    """
    tells the remote player's client the result of his last shot.
    """
    def __init__(self, is_hit, game_over, destroyed_ship):
        self.is_hit = is_hit
        self.game_over = game_over
        self.destroyed_ship = destroyed_ship


class RevealMessage(object):
    """
    tells the remote player's client the coordinates of the player's intact
    ships.
    """
    def __init__(self, coords):
        self.coords = coords


class ExitMessage(object):
    """
    sent by a client to signal disconnection / program exit.
    """
    pass


class AcknowledgementMessage(object):
    """
    acknowledges an action. what that action is depends on the context in which
    this message is used (for example, acknowledge having finished ship
    placements).
    """
    pass