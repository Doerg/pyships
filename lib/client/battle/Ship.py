class Ship(object):
    _tokens = {
        'horizontal': {'front': '◀', 'back': '▶'},
        'vertical': {'front': '▲', 'back': '▼'},
        'center': '▣'
    }

    @classmethod
    def setup_class_vars(cls, keys, battle_map, map_size):
        """
        sets up variables used by all instances of ships
        :param keys: curses key codes to extract directional keys from
        :param battle_map: the map on which all ships are to be placed
        :param map_size: size of the map
        """
        cls._directions = {
            key_name: key_code for key_name, key_code in keys.items()
            if key_name in ('up', 'down', 'left', 'right')
        }
        cls._battle_map = battle_map
        cls._map_size = map_size


    def __init__(self, size):
        center = self._map_size//2
        self.coords = [[center, center - size//2 + i] for i in range(size)]
        self.alignment = 'hor'
        self.size = size
        self._rotation_axis = size//2

        self._build_string()


    def __str__(self):
        return self._string


    def _build_string(self):
        if self.alignment == 'hor':
            parts = [
                self._tokens['horizontal']['front'],
                self._tokens['horizontal']['back']
            ]
            for _ in range(self.size - 2):
                parts.insert(1, self._tokens['center'])
            self._string = ' '.join(parts)
        else:
            parts = [
                self._tokens['vertical']['front'],
                self._tokens['vertical']['back']
            ]
            for _ in range(self.size - 2):
                parts.insert(1, self._tokens['center'])
            self._string = ''.join(parts)


    def move(self, direction):
        """
        lets the ship move on the map in the given direction, if possible
        :param direction: direction to move to, given as curses key code
        """
        if direction == self._directions['up']:
            if not self.coords[0][0] == 0:
                for coord in self.coords:
                    coord[0] -= 1
        elif direction == self._directions['left']:
            if not self.coords[0][1] == 0:
                for coord in self.coords:
                    coord[1] -= 1
        elif direction == self._directions['down']:
            if not self.coords[-1][0] == self._map_size-1:
                for coord in self.coords:
                    coord[0] += 1
        elif direction == self._directions['right']:
            if not self.coords[-1][1] == self._map_size-1:
                for coord in self.coords:
                    coord[1] += 1


    def rotate(self):
        """
        rotates this ship to the opposite orientation
        """
        self.alignment = 'vert' if self.alignment == 'hor' else 'hor'
        self._build_string()
        self._rotate_coordinates()
        self._correct_border_violations()


    def _rotate_coordinates(self):
        if self.alignment == 'hor':
            for i in range(self.size):
                self.coords[i][0] += self._rotation_axis - i
                self.coords[i][1] -= self._rotation_axis - i
        else:
            for i in range(self.size):
                self.coords[i][0] -= self._rotation_axis - i
                self.coords[i][1] += self._rotation_axis - i


    def _correct_border_violations(self):
        if self.alignment == 'hor':  #correction of violations @ left & right
            while self.coords[0][1] < 0:
                self.move(self._directions['right'])
            while self.coords[-1][1] > self._map_size-1:
                self.move(self._directions['left'])
        else:                           #correction of violations @ top & bottom
            while self.coords[0][0] < 0:
                self.move(self._directions['down'])
            while self.coords[-1][0] > self._map_size-1:
                self.move(self._directions['up'])


    def blocked(self):
        """
        checks whether one of the ships coordinates is occupied by another ship
        :return: true if a coord is occupied, false otherwise
        """
        for row, col in self.coords:
            if self._battle_map[row][col]:
                return True
        return False


    def place_on_map(self):
        """
        ultimately associates this ship with the map
        """
        for row, col in self.coords:
            self._battle_map[row][col] = True