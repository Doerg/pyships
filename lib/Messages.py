from threading import Thread


### messages from client only ###
class NameMessage(object):
    """
    tells the server the name of the local player.
    """
    def __init__(self, player_name):
        self.player_name = player_name


class ShotMessage(object):
    """
    tells the server the coordinates of the shot taken by the local player.
    """
    def __init__(self, coords):
        self.coords = coords


### messages from server only ###
class IDMessage(object):
    """
    tells the client the id of the local player (chosen by the server)
    and the name of the remote player.
    """
    def __init__(self, player_id, opponent_name):
        self.opponent_name = opponent_name
        self.player_id = player_id


class ShotResultMessage(object):
    """
    tells the client the result of a shot, either taken by himself or the
    remote player.
    """
    def __init__(self, coords, is_hit, game_over, destroyed_ship):
        self.coords = coords
        self.is_hit = is_hit
        self.game_over = game_over
        self.destroyed_ship = destroyed_ship


class ShutdownMessage(object):
    """
    tells the client that the server shut down.
    """
    pass


### messages sent by server and client ###
class ExitMessage(object):
    """
    can either be sent by the client to tell the server that the local player
    terminated the program, or it can be sent by the server to tell the client
    that the remote player terminated the program.
    """
    def __init__(self, player_id=None):
        if player_id != None:
            self.player_id = player_id


class PlacementMessage(object):
    """
    can either be sent by the client to tell the server the local player's
    ship placements, or it can be sent by the server to tell the client that
    the remote player finished ship placements.
    """
    def __init__(self, player_id=None, coords=None):
        if player_id != None:
            self.player_id = player_id
        if coords != None:
            self.coords = coords