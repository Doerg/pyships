class Fleet(object):
    def __init__(self, ships_coords):
        self._intact_ships = [Ship(coords) for coords in ships_coords]
        self._destroyed_ships = []


    def receive_shot(self, coords):
        for i in range(len(self._intact_ships)):
            if self._intact_ships[i].is_hit(coords):
                hit_ship = self._intact_ships[i]
                if hit_ship.is_destroyed():
                    self._intact_ships.remove(i)
                    self._destroyed_ships.append(hit_ship)
                    return hit_ship.coords
                return True

        return False


    def is_destroyed(self):
        return len(self._intact_ships) == 0


    class Ship(object):
        def __init__(self, full_coords):
            self._full_coords = full_coords
            self._hitpoints = len(full_coords)


        def is_hit(self, coords):
            for c in self._full_coords:
                if c == coords:
                    self._hitpoints -= 1
                    return True
            return False


        def is_destroyed(self):
            return self._hitpoints == 0