#!/usr/bin/env python3.4

# algorithm development playground / proof of concept for
# ship placement by user @ game start of pyships
#
# controls:
# move ship with w/a/s/d
# rotate ship with space
# exit program with q

map_size = 10
the_map = [['.' for field in range(map_size)] for row in range(map_size)]
ship = {
    'alignment': 'hor',
    'coords': ([5, 3], [5, 4], [5, 5], [5, 6])
}
coords = ship['coords']


def place_ship():
    for row, col in coords:
        the_map[row][col] = 'X'


def show_map():
    for row in the_map:
        print(' '.join(row))


def clear_map():
    global the_map
    the_map = [['.' for field in row] for row in the_map]


def move_ship(direction):
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


def rotate_ship():
    rotation_axis = len(coords) // 2

    if ship['alignment'] == 'hor':
        rotate_to_vertical(rotation_axis)
        ship['alignment'] = 'vert'
    else:
        rotate_to_horizontal(rotation_axis)
        ship['alignment'] = 'hor'

    border_violation_correction(ship['alignment'])


def rotate_to_vertical(rotation_axis):
    for i in range(len(coords)):
        coords[i][0] -= rotation_axis - i
        coords[i][1] += rotation_axis - i


def rotate_to_horizontal(rotation_axis):
    for i in range(len(coords)):
        coords[i][0] += rotation_axis - i
        coords[i][1] -= rotation_axis - i


def border_violation_correction(rotation_type):
    if rotation_type == 'hor':  #check for violations @ left & right hand side
        while coords[0][1] < 0:
            move_ship('d')
        while coords[-1][1] > 9:
            move_ship('a')
    else:                       #check for violations @ top & bottom
        while coords[0][0] < 0:
            move_ship('s')
        while coords[-1][0] > 9:
            move_ship('w')


while True:
    place_ship()
    show_map()
    clear_map()

    key = input('--> ')

    if key == 'q':
        break
    if key in "wasd":
        move_ship(key)
    elif key == ' ':
        rotate_ship()
