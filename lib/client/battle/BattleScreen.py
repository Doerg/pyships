from CustomExceptions import ProgramExit
from client.battle.Windows import *
from client.battle.Ship import Ship
from client import UIData


def init(player_name):
    """
    initializes all the windows of the battle screen and displays them.
    :param player_name: the name of the player
    """
    global _content_frame, _key_legend, _message_bar
    global _player_map, _opponent_map, _player_name

    _content_frame = ContentFrame(player_name)
    _key_legend = KeyLegend()
    _player_map = BattleGround()
    _opponent_map = BattleGround(opponent=True)
    _message_bar = MessageBar()

    _content_frame.update()
    _key_legend.update()
    _player_map.update()
    _opponent_map.update()
    _message_bar.update()


def player_ship_placements():
    """
    lets the player position his ships.
    :return: the coordinates of all placed ships
    """
    _message('Welcome to pyships! Please place your ships.')

    map_size = UIData.battle['map']['logical size']
    the_map = [
        [False for _col in range(map_size)] for _row in range(map_size)
    ]

    Ship.setup_class_vars(the_map, map_size)

    coords = [_position_ship(Ship(size)) for size in (4, 4, 3, 3, 3, 2, 2)]

    _player_map.draw_map()
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
        _player_map.draw_map(new_ship=ship)
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
                _message(
                    'You have already placed a ship at this location. ' +
                    'Please choose another one.'
                )
                misplacement = True
            else:
                ship.place_on_map()
                _player_map.add_ship(ship)
                if misplacement:
                    _message('Please place your next ship.')
                    misplacement = False
                break

    return ship.coords  # server will only need coords


def _message(msg):
    """
    writes the message to the message bar and displays it.
    :param msg: the message to display
    """
    _message_bar.put_message(msg)
    _message_bar.update()