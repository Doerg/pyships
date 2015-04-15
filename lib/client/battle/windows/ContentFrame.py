import curses
from .Window import Window
from client import UIData


class ContentFrame(Window):
    """
    the outermost frame of the battle screen. this frame is centralized and
    contains all sub-windows.
    """
    _height = UIData.battle['frame']['height']
    _width = UIData.battle['frame']['width']

    def __init__(self, player_name):
        """
        draws the frame and writes player names.
        :param player_name: the name of the player
        """
        legend_height = UIData.battle['info bar']['height']
        map_box_height = UIData.battle['map']['box']['height']
        map_box_width = UIData.battle['map']['box']['width']

        super().__init__(self._height, self._width, 0, 0)

        curses.noecho()
        curses.curs_set(False)

        self._win.bkgd(' ', UIData.colors['content frame'] | curses.A_BOLD)
        self._win.vline(
            legend_height + 1, self._width//2,
            curses.ACS_VLINE, map_box_height + 2*Window._margin
        )

        self._win.addstr(
            legend_height + Window._margin,
            Window._margin + map_box_width//2 - len(player_name)//2,
            player_name, UIData.colors['player name']
        )
        self._win.addstr(
            legend_height + Window._margin,
            1 + 3*Window._margin + map_box_width +
            map_box_width//2 - len('Opponent')//2,
            'Opponent', UIData.colors['opponent name']
        )