from client.battle import Windows
from client.battle.Ship import Ship
from CustomExceptions import ProgramExit


# usable keys
_keys = {
    'up': 65,    #curses returns these codes for arrow keys. like wtf?
    'down': 66,
    'left': 68,
    'right': 67,
    'rotate': ord(' '),
    'place ship': 10,   #enter
    'fire': 10,
    'exit': ord('q')
}


def init(player_name):
    global _content_frame, _key_legend, _message_bar
    global _player_map, _opponent_map, _player_name

    _content_frame = Windows.ContentFrame(player_name)
    _key_legend = Windows.KeyLegend()
    _player_map = Windows.BattleGround()
    _opponent_map = Windows.BattleGround(opponent=True)
    _message_bar = Windows.MessageBar()

    _content_frame.update()
    _key_legend.update()
    _player_map.update()
    _opponent_map.update()
    _message_bar.update()


def player_ship_placements():
    """
    lets the player position his ships.
    :return: coordinates of all placed ships
    """
    _message_bar.put_message('Welcome to pyships! Please place your ships.')
    _message_bar.update()

    map_size = Windows.logical_map_size
    the_map = [
        [False for _col in range(map_size)] for _row in range(map_size)
    ]

    Ship.setup_class_vars(_keys, the_map, map_size)

    coords = [_position_ship(Ship(size)) for size in (4, 4, 3, 3, 3, 2, 2)]

    _player_map.draw_map()
    _player_map.update()

    return coords


def _position_ship(ship):
    misplacement = False

    while True:
        _player_map.draw_map(new_ship=ship)
        _player_map.update()

        key = _player_map.get_key()

        if key == _keys['exit']:
            raise ProgramExit

        if key in (_keys['up'], _keys['down'], _keys['left'], _keys['right']):
            ship.move(key)

        elif key == _keys['rotate']:
            ship.rotate()

        elif key == _keys['place ship']:
            if ship.blocked():
                _message_bar.put_message(
                    'You have already placed a ship at this location. ' +
                    'Please choose another one.'
                )
                _message_bar.update()
                misplacement = True
            else:
                ship.place_on_map()
                _player_map.add_ship(ship)
                if misplacement:
                    _message_bar.put_message('Please place your next ship.')
                    _message_bar.update()
                    misplacement = False
                break

    return ship.coords  # server will only need coords