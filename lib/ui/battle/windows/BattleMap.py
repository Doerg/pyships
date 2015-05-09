import curses
from .Window import Window
from ui import UIData


class BattleMap(Window):
    """
    square window which displays the battleground of the player or opponent.
    the battle screen contains two of these. don't instantiate directly, use
    one of PlayerMap or OpponentMap instead.
    """
    _ui_data = UIData.battle['map']
    _logical_size = _ui_data['logical size']
    _height = _ui_data['height']
    _width = _ui_data['width']
    _box_height = _ui_data['box']['height']
    _box_width = _ui_data['box']['width']
    _water_tokens = UIData.tokens['ocean']
    _miss_token = UIData.tokens['miss']

    def __init__(self, offset_x):
        """
        draws one of the two battlegrounds of the screen.
        :param offset_x: offset column in respect to the content frame
        """
        legend_height = UIData.battle['info bar']['height']

        super().__init__(
            self._box_height, self._box_width,
            legend_height + Window._margin + 1, offset_x
        )

        self._win.bkgd(' ', UIData.colors['battle frame'])
        self._win.bkgdset(' ', UIData.colors['ocean'])
        self._draw_ocean()


    def _draw_ocean(self):
        """
        draws the ocean of the battleground.
        """
        for row in range(1, self._height+1):
            for col in range(1, self._width+1):
                self._win.addstr(row, col, self._water_tokens[(row+col) % 2])


    def _draw_ship(self, ship, color):
        """
        draws a ship onto the map.
        :param ship: the ship to draw
        :param color: the color to use for the drawing
        """
        ship_string = str(ship)

        if ship.alignment == 'hor':
            front_y, front_x = ship.coords[0]
            self._win.addstr(
                self._scale_y(front_y), self._scale_x(front_x),
                ship_string, color
            )
        else:
            for i in range(ship.size):
                y, x = ship.coords[i]
                self._win.addstr(
                    self._scale_y(y), self._scale_x(x), ship_string[i], color
                )


    def _scale_y(self, y):
        """
        translate the given logical x-coordinate to the graphical x-coordinate
        to be displayed on the visual map.
        :param y: the y-coordinate of the logical map
        :return: the scaled y-coordinate
        """
        return y + 1


    def _scale_x(self, x):
        """
        translate the given logical x-coordinate to the graphical x-coordinate
        to be displayed on the visual map. this is necessary b/c the
        graphical map has twice the width (-1) of the logical map.
        :param x: the x-coordinate of the logical map
        :return: the scaled x-coordinate
        """
        return x*2 + 1



class PlayerMap(BattleMap):
    """
    the player's map.
    """
    def __init__(self):
        super().__init__(Window._margin + 1)

        self._ships = []


    def add_ship(self, ship):
        """
        add a ship in order for it to be displayed on this battleground.
        :param ship: the ship to be added
        """
        self._ships.append(ship)


    def draw_ship_placements(self, new_ship=None):
        """
        draws the ocean of the battleground and all ships on it. might draw
        an extra ship in the context of the player's ship placement phase.
        :param new_ship: an extra ship to display for this one drawing
        """
        self._draw_ocean()

        for ship in self._ships:
            self._draw_ship(ship, UIData.colors['ship'])
        if new_ship:
            if new_ship.blocked():
                color = UIData.colors['blocked ship']
            else:
                color = UIData.colors['placeable ship']
            self._draw_ship(new_ship, color)


    def display_shot(self, coords, is_hit):
        """
        if the shot is a miss, draws a new token @ the coordinates of the shot.
        if the token is a hit, colors the ship as an indication.
        :param coord: coordinate of the shot
        :param is_hit: whether the shot is a hit
        """
        y, x = self._scale_y(coords[0]), self._scale_x(coords[1])
        if is_hit:
            self._win.chgat(y, x, 1, UIData.colors['hit'])
        else:
            self._win.addstr(y, x, self._miss_token, UIData.colors['miss'])



class OpponentMap(BattleMap):
    """
    the opponent's map.
    """
    _hit_token = UIData.tokens['hit']
    _directions = {
        key_name: code for key_name, code in UIData.key_codes.items()
        if key_name in ('up', 'down', 'left', 'right')
    }

    def __init__(self):
        super().__init__(self._box_width + 3*Window._margin + 2)

        center = BattleMap._logical_size // 2
        self._selection_coords = [center, center]   #logical coordinates
        self._saved_cursor_coords = (
            self._scale_y(center), self._scale_x(center)
        )
        self._shot_map = [
            [False] * self._logical_size for _ in range(self._logical_size)
        ]


    def set_cursor(self):
        """
        moves the cursor to the coordinates of the last shot and makes the
        cursor visible.
        """
        self._win.move(*self._saved_cursor_coords)
        curses.curs_set(True)


    def move_cursor(self, direction):
        """
        moves the cursor in the given direction, if possible.
        :param direction: the direction in which to move the cursor
        """
        if direction == self._directions['up']:
            if self._selection_coords[0] > 0:
                self._selection_coords[0] -= 1
        elif direction == self._directions['down']:
            if self._selection_coords[0] < self._logical_size-1:
                self._selection_coords[0] += 1
        elif direction == self._directions['left']:
            if self._selection_coords[1] > 0:
                self._selection_coords[1] -= 1
        elif direction == self._directions['right']:
            if self._selection_coords[1] < self._logical_size-1:
                self._selection_coords[1] += 1

        cursor_y = self._scale_y(self._selection_coords[0])
        cursor_x = self._scale_x(self._selection_coords[1])
        self._win.move(cursor_y, cursor_x)
        self._saved_cursor_coords = (cursor_y, cursor_x)


    def is_repeated_shot(self):
        """
        returns whether a shot at the current position has already been taken.
        :return: True if shot has already been taken, False otherwise
        """
        y, x = self._selection_coords
        return self._shot_map[y][x]


    def fire_shot(self):
        """
        returns the logical map coordinates, calculated from the current
        cursor position. also undisplays the cursor.
        :return: the logical coordinates of the shot
        """
        curses.curs_set(False)

        logical_y, logical_x = self._selection_coords
        self._shot_map[logical_y][logical_x] = True

        return [logical_y, logical_x]


    def reveal_ship(self, ship, is_destroyed):
        """
        draws a ship on the opponent's map.
        :param ship: the ship of the opponent to reveal
        :param is_destroyed: True if the ship is destroyed, False otherwise
        """
        color = UIData.colors['hit'] if is_destroyed else UIData.colors['ship']
        self._draw_ship(ship, color)


    def display_shot(self, coord, is_hit):
        """
        draws a new token on the coordinates of the shot.
        :param coord: coordinate of the shot
        :param is_hit: whether the shot is a hit
        """
        if is_hit:
            token = self._hit_token
            color = UIData.colors['hit']
        else:
            token = self._miss_token
            color = UIData.colors['miss']

        self._win.addstr(
            self._scale_y(coord[0]), self._scale_x(coord[1]), token, color
        )