### messages from client only ###
class ShotMessage(object):
    """
    tells the server the coordinates of the shot taken by the local player.
    """
    def __init__(self, coords):
        self.coords = coords


### messages from server only ###
class IDMessage(object):
    """
    tells the client the id of the local player (chosen by the server).
    """
    def __init__(self, player_id):
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
class NameMessage(object):
    """
    delivers the name of a player. can either be sent by the client to tell the
    server the name of the local player, or it can be sent by the server to
    tell a client the name of the opponent.
    """
    def __init__(self, player_name):
        self.player_name = player_name


class ExitMessage(object):
    """
    can either be sent by the client to tell the server that the local player
    terminated the program, or it can be sent by the server to tell a client
    that the remote player terminated the program.
    """
    def __init__(self, player_id=None):
        if player_id != None:
            self.player_id = player_id


class PlacementMessage(object):
    """
    can either be sent by the client to tell the server the local player's
    ship placements, or it can be sent by the server to tell a client that
    the remote player finished ship placements. the server can also use this
    message to tell a client which ships of the opponent the player didn't
    manage to destroy (after the player lost the game).
    """
    def __init__(self, player_id=None, coords=None):
        if player_id != None:
            self.player_id = player_id
        if coords != None:
            self.coords = coords


class RematchMessage(object):
    """
    can either be sent by the client to tell the server that the local player
    is willing to player a rematch, or it can be sent by the server to tell a
    client that the remote player agreed to a rematch.
    """
    def __init__(self, player_id=None):
        if player_id != None:
            self.player_id = player_id