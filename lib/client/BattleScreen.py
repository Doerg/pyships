from client import BattleWindows
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

    _content_frame = BattleWindows.ContentFrame(player_name)
    _key_legend = BattleWindows.KeyLegend()
    _player_map = BattleWindows.BattleGround()
    _opponent_map = BattleWindows.BattleGround(opponent=True)
    _message_bar = BattleWindows.MessageBar()

    _content_frame.update()
    _key_legend.update()
    _player_map.update()
    _opponent_map.update()
    _message_bar.update()


def player_ship_placements():
    """
    lets player position his ships.
    """
    _message_bar.put_message('Welcome to pyships! Please place your ships.')
    _message_bar.update()
    map_size = BattleWindows.logical_map_size
    the_map = [
        [False for _col in range(map_size)] for _row in range(map_size)
    ]

    ships = (4, 4, 3, 3, 3, 2, 2)

    return [_position_ship(ship_size, the_map, map_size) for ship_size in ships]


def _position_ship(ship_size, the_map, map_size):
    center = map_size//2
    ship = {    # ship placement selection starts @ map center & horizontal
        'alignment': 'hor',
        'coords': [
            [center, center - ship_size//2 + i] for i in range(ship_size)
        ]
    }
    misplacement = False

    while True:
        _player_map.draw_map(tmp_ship=ship)
        _player_map.update()

        key = _player_map.get_key()

        if key == _keys['exit']:
            raise ProgramExit

        if key in (_keys['up'], _keys['down'], _keys['left'], _keys['right']):
            _move_ship(ship, key, map_size)

        elif key == _keys['rotate']:
            _rotate_ship(ship, map_size)

        elif key == _keys['place ship']:
            if _ship_blocked(ship, the_map):
                _message_bar.put_message(
                    'You have already placed a ship at this location. ' +
                    'Please choose another one.'
                )
                _message_bar.update()
                misplacement = True
            else:
                _place_ship(ship, the_map)
                _player_map.add_ship(ship)
                if misplacement:
                    _message_bar.put_message('Please place your next ship.')
                    _message_bar.update()
                    misplacement = False
                break

    return ship['coords'] # server will only need coords


def _move_ship(ship, direction, map_size):
    coords = ship['coords']

    if direction == _keys['up']:
        if not coords[0][0] == 0:
            for coord in coords:
                coord[0] -= 1
    elif direction == _keys['left']:
        if not coords[0][1] == 0:
            for coord in coords:
                coord[1] -= 1
    elif direction == _keys['down']:
        if not coords[-1][0] == map_size-1:
            for coord in coords:
                coord[0] += 1
    elif direction == _keys['right']:
        if not coords[-1][1] == map_size-1:
            for coord in coords:
                coord[1] += 1


def _rotate_ship(ship, map_size):
    coords = ship['coords']
    rotation_axis = len(coords)//2

    if ship['alignment'] == 'hor':
        _rotate_to_vertical(coords, rotation_axis)
        ship['alignment'] = 'vert'
    else:
        _rotate_to_horizontal(coords, rotation_axis)
        ship['alignment'] = 'hor'

    _border_violation_correction(ship, map_size)


def _rotate_to_vertical(coords, rotation_axis):
    for i in range(len(coords)):
        coords[i][0] -= rotation_axis - i
        coords[i][1] += rotation_axis - i


def _rotate_to_horizontal(coords, rotation_axis):
    for i in range(len(coords)):
        coords[i][0] += rotation_axis - i
        coords[i][1] -= rotation_axis - i


def _border_violation_correction(ship, map_size):
    coords = ship['coords']

    if ship['alignment'] == 'hor':  #correction of violations @ left & right
        while coords[0][1] < 0:
            _move_ship(ship, _keys['right'], map_size)
        while coords[-1][1] > map_size-1:
            _move_ship(ship, _keys['left'], map_size)
    else:                           #correction of violations @ top & bottom
        while coords[0][0] < 0:
            _move_ship(ship, _keys['down'], map_size)
        while coords[-1][0] > map_size-1:
            _move_ship(ship, _keys['up'], map_size)


def _ship_blocked(ship, the_map):
    for row, col in ship['coords']:
        if the_map[row][col]:
            return True
    return False


def _place_ship(ship, the_map):
    for row, col in ship['coords']:
        the_map[row][col] = True