#!/usr/bin/env python3

# algorithm development playground / proof of concept for
# ship placement by user @ game start of pyships
#
# controls:
# move ship with w/a/s/d
# rotate ship with space
# exit program with q

the_map = [
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
]
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
    for row in the_map:
        for i in range(len(row)):
            row[i] = '.'


while True:
    place_ship()
    show_map()
    clear_map()

    key = input('--> ')
    if key == 'q':
        break

    if key == 'w':
        if not coords[0][0] == 0:
            for coord in coords:
                coord[0] -= 1
    elif key == 'a':
        if not coords[0][1] == 0:
            for coord in coords:
                coord[1] -= 1
    elif key == 's':
        if not coords[-1][0] == 9:
            for coord in coords:
                coord[0] += 1
    elif key == 'd':
        if not coords[-1][1] == 9:
            for coord in coords:
                coord[1] += 1
    elif key == ' ':
        #rot_axis = len(coords) / 2
        pass
