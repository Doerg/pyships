from CustomExceptions import ProgramExit
from .windows import *
from .Ship import Ship
from client import UIData


def init(player_name):
    """
    initializes all the windows of the battle screen and displays them.
    :param player_name: the name of the player
    """
    global _content_frame, _key_legend, _message_bar, _player_map, _opponent_map

    _content_frame = ContentFrame(player_name)
    _key_legend = KeyLegend()
    _player_map = PlayerMap()
    _opponent_map = OpponentMap()
    _message_bar = MessageBar()

    _content_frame.update()
    _key_legend.update()
    _player_map.update()
    _opponent_map.update()
    _message_bar.update()


def introduce_opponent(opponent_name):
    """
    writes the opponent's name on top of his map and introduces him in the
    message bar.
    :param opponent_name: the name of the player's opponent
    """
    _content_frame.set_opponent_name(opponent_name)
    _content_frame.update()
    message("Your opponent is '%s'! Please place your ships." % opponent_name)


def player_ship_placements(ships):
    """
    lets the player position his ships.
    :param ships: the ships to be placed, represented by integers (their size)
    :return: the coordinates of all placed ships
    """
    map_size = UIData.battle['map']['logical size']
    the_map = [
        [False for _col in range(map_size)] for _row in range(map_size)
    ]

    Ship.setup_class_vars(the_map, map_size)

    coords = [_position_ship(Ship(size)) for size in ships]

    _player_map.draw_ship_placements()
    _player_map.update()

    return coords


def _position_ship(ship):
    """
    does user interaction in order to place a new ship on the map.
    :param ship: the ship to be placed on the map
    :return: the coordinates of the placed ship
    """
    keys = UIData.key_codes
    misplacement = False

    while True:
        _player_map.draw_ship_placements(new_ship=ship)
        _player_map.update()

        key = _player_map.get_key()

        if key == keys['exit']:
            raise ProgramExit

        if key in (keys['up'], keys['down'], keys['left'], keys['right']):
            ship.move(key)

        elif key == keys['rotate']:
            ship.rotate()

        elif key == keys['place ship']:
            if ship.blocked():
                message(
                    'You have already placed a ship at this location. ' +
                    'Please choose another one.'
                )
                misplacement = True
            else:
                ship.place_on_map()
                _player_map.add_ship(ship)
                if misplacement:
                    message('Please place your next ship.')
                    misplacement = False
                break

    return ship.coords  # server will only need coords


def show_ship_placement_keys():
    """
    displays the ship placement key legend.
    """
    _key_legend.set_ship_placement_keys()
    _key_legend.update()


def show_battle_keys():
    """
    replaces the ship placement key legend with the battle mode key legend.
    """
    _key_legend.set_battle_keys()
    _key_legend.update()


def reveal_intact_ships(ship_coords):
    """
    reveals the ships of the opponent that the player did not manage to destroy.
    :param ship_coords: the coordinates of all intact ships of the opponent
    """
    for coords in ship_coords:
        reveal_ship(coords, False)


def reveal_ship(coords, is_destroyed):
    """
    reveals a ship of the opponent.
    :param coords: coordinates of the ship to reveal
    :param is_destroyed: True if the ship is destroyed, False otherwise
    """
    ship = Ship(len(coords), coords=coords)
    _opponent_map.reveal_ship(ship, is_destroyed)
    _opponent_map.update()


def show_shot(coords, is_hit, opponent=False):
    """
    displays a shot on the player's map per default, or on the opponent's map
    if the flag 'opponent' is set to true.
    :param coords: coordinates of the shot
    :param is_hit: whether the shot to display is a hit
    :param opponent: whether the shot is to be displayed on the opponent's map
    """
    map_to_update = _opponent_map if opponent else _player_map
    map_to_update.display_shot(coords, is_hit)
    map_to_update.update()


def let_player_shoot():
    """
    lets the player select a coordinate on the opponent's map and shoot.
    :return: the (logical) coordinates of the shot
    """
    keys = UIData.key_codes

    _opponent_map.set_cursor()

    while True:
        key = _opponent_map.get_key()

        if key == keys['exit']:
            raise ProgramExit
        if key in (keys['up'], keys['down'], keys['left'], keys['right']):
            _opponent_map.move_cursor(key)
        elif key == keys['fire']:
            if _opponent_map.is_repeated_shot():
                message(
                    "You already fired at this position. " +
                    "Please choose another one."
                )
                _opponent_map.set_cursor() #b/c cursor moved to message bar
            else:
                return _opponent_map.fire_shot()


def ask_for_another_battle(msg):
    """
    asks the player if he is willing to play a rematch. only accepts inputs
    y/n.
    :param msg: the message to display to the player
    :return: True if the player wants a rematch, False otherwise
    """
    message(msg + ' Play again? (Y/N)')

    while True:
        key = _message_bar.get_key()
        if key == UIData.key_codes['yes']:
            return True
        if key == UIData.key_codes['no']:
            return False


def reset_battle():
    """
    resets the player's and opponent's map to their default empty state.
    """
    global _player_map, _opponent_map

    _player_map = PlayerMap()
    _opponent_map = OpponentMap()
    _player_map.update()
    _opponent_map.update()


def handle_exit(msg):
    """
    displays the message and returns once the player pressed exit.
    :param msg: the message to display
    """
    message(msg + " Please press 'Q' to exit.")
    while _message_bar.get_key() != UIData.key_codes['exit']:
        pass


def message(msg):
    """
    writes the message to the message bar and displays it.
    :param msg: the message to display
    """
    _message_bar.put_message(msg)
    _message_bar.update()