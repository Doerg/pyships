#!/usr/bin/env python3.4

# algorithm development playground / proof of concept for
# ship placement by user @ game start of pyships
#
# controls:
# move ship with w/a/s/d
# rotate ship with space
# place ship with r
# exit program with q

from copy import deepcopy


def show_map(ship, the_map):
    temporary_map = deepcopy(the_map)
    for row, col in ship['coords']:
        temporary_map[row][col] = 'X'
    for row in temporary_map:
        print(' '.join(row))


def move_ship(ship, direction):
    coords = ship['coords']

    if direction == 'w':
        if not coords[0][0] == 0:
            for coord in coords:
                coord[0] -= 1
    elif direction == 'a':
        if not coords[0][1] == 0:
            for coord in coords:
                coord[1] -= 1
    elif direction == 's':
        if not coords[-1][0] == 9:
            for coord in coords:
                coord[0] += 1
    elif direction == 'd':
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

    if ship['alignment'] == 'hor':  #check for violations @ left & right
        while coords[0][1] < 0:
            move_ship(ship, 'd')
        while coords[-1][1] > 9:
            move_ship(ship, 'a')
    else:                           #check for violations @ top & bottom
        while coords[0][0] < 0:
            move_ship(ship, 's')
        while coords[-1][0] > 9:
            move_ship(ship, 'w')


def ship_blocked(ship, the_map):
    for row, col in ship['coords']:
        if the_map[row][col] == 'X':
            return True
    return False


def place_ship(ship, the_map):
    for row, col in ship['coords']:
        the_map[row][col] = 'X'


def run():
    map_size = 10
    center = map_size // 2
    the_map = [['.' for field in range(map_size)] for row in range(map_size)]

    for ship_size in (4, 4, 3, 3, 2, 2):
        ship = {
            'alignment': 'hor',
            'coords': [
                [center, center - ship_size//2 + i]
                for i in range(ship_size)
            ]
        }

        while True:
            show_map(ship, the_map)

            key = input('--> ')

            if key == 'q':
                return
            if key in "wasd":
                move_ship(ship, key)
            elif key == 'r':
                rotate_ship(ship)
            elif key == ' ':
                if ship_blocked(ship, the_map):
                    print('Ship blocked!')
                else:
                    place_ship(ship, the_map)
                    break


if __name__ == '__main__':
    run()
