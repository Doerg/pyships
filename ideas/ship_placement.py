#!/usr/bin/env python3.4

# algorithm development playground / proof of concept for
# ship placement by user @ game start of pyships
#
# controls:
# move ship with w/a/s/d
# rotate ship with r
# place ship with space
# exit program with q

from copy import deepcopy

# usable keys
LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'
ROTATE = 'r'
PLACE_SHIP = ' '
QUIT = 'q'

# map tokens
SHIP = 'X'
WATER = '.'


def show_map(ship, the_map):
    temporary_map = deepcopy(the_map)
    for row, col in ship['coords']:
        temporary_map[row][col] = SHIP
    for row in temporary_map:
        print(' '.join(row))


def move_ship(ship, direction):
    coords = ship['coords']

    if direction == UP:
        if not coords[0][0] == 0:
            for coord in coords:
                coord[0] -= 1
    elif direction == LEFT:
        if not coords[0][1] == 0:
            for coord in coords:
                coord[1] -= 1
    elif direction == DOWN:
        if not coords[-1][0] == 9:
            for coord in coords:
                coord[0] += 1
    elif direction == RIGHT:
        if not coords[-1][1] == 9:
            for coord in coords:
                coord[1] += 1


def rotate_ship(ship):
    coords = ship['coords']
    rotation_axis = len(coords) // 2

    if ship['alignment'] == 'hor':
        rotate_to_vertical(coords, rotation_axis)
        ship['alignment'] = 'vert'
    else:
        rotate_to_horizontal(coords, rotation_axis)
        ship['alignment'] = 'hor'

    border_violation_correction(ship)


def rotate_to_vertical(coords, rotation_axis):
    for i in range(len(coords)):
        coords[i][0] -= rotation_axis - i
        coords[i][1] += rotation_axis - i


def rotate_to_horizontal(coords, rotation_axis):
    for i in range(len(coords)):
        coords[i][0] += rotation_axis - i
        coords[i][1] -= rotation_axis - i


def border_violation_correction(ship):
    coords = ship['coords']

    if ship['alignment'] == 'hor':  #correction of violations @ left & right
        while coords[0][1] < 0:
            move_ship(ship, RIGHT)
        while coords[-1][1] > 9:
            move_ship(ship, LEFT)
    else:                           #correction of violations @ top & bottom
        while coords[0][0] < 0:
            move_ship(ship, DOWN)
        while coords[-1][0] > 9:
            move_ship(ship, UP)


def ship_blocked(ship, the_map):
    for row, col in ship['coords']:
        if the_map[row][col] == SHIP:
            return True
    return False


def place_ship(ship, the_map):
    for row, col in ship['coords']:
        the_map[row][col] = SHIP


def run():
    map_size = 10
    center = map_size // 2
    the_map = [[WATER for field in range(map_size)] for row in range(map_size)]

    for ship_size in (4, 4, 3, 3, 2, 2):
        ship = {    # ship placement selection starts @ map center & horizontal
            'alignment': 'hor',
            'coords': [
                [center, center - ship_size//2 + i]
                for i in range(ship_size)
            ]
        }

        while True:
            show_map(ship, the_map)

            key = input('--> ')

            if key == QUIT:
                return
            if key in (LEFT, RIGHT, UP, DOWN):
                move_ship(ship, key)
            elif key == ROTATE:
                rotate_ship(ship)
            elif key == PLACE_SHIP:
                if ship_blocked(ship, the_map):
                    print('Ship blocked!')
                else:
                    place_ship(ship, the_map)
                    break


if __name__ == '__main__':
    run()
