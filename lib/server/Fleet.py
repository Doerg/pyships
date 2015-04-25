class Fleet(object):

    def __init__(self, ships_coords):
        self._intact_ships = [self.Ship(coords) for coords in ships_coords]


    def receive_shot(self, coords):
        """
        checks whether the shot hits a ship of this fleet.
        :param coords: coordinates of the shot
        :return: False when no ship is hit, True when a ship is hit and not
        destroyed, the ship's coordinates when the shot destroyed the ship.
        """
        for ship in self._intact_ships:
            if ship.is_hit(coords):
                if ship.is_destroyed():
                    self._intact_ships.remove(ship)
                    return ship.full_coords
                return True

        return False


    def is_destroyed(self):
        """
        checks whether the fleet is destroyed, meaning it has no intact ships
        left.
        :return: True when all ships are destroyed, False otherwise
        """
        return len(self._intact_ships) == 0


    class Ship(object): #inner class
        def __init__(self, full_coords):
            self.full_coords = full_coords
            self._hitpoints = len(full_coords)


        def is_hit(self, coords):
            """
            checks whether the ship is hit by the shot.
            :param coords: the coordinates of the shot
            :return: True when the shot hit, False otherwise
            """
            for c in self.full_coords:
                if c == coords:
                    self._hitpoints -= 1
                    return True
            return False


        def is_destroyed(self):
            """
            checks whether the ship is destroyed.
            :return: True when the ship is destroyed, False otherwise
            """
            return self._hitpoints == 0