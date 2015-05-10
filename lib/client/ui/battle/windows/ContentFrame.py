import curses
from .Window import Window
from client.ui import UIData


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
        self.set_opponent_name('Opponent')


    def set_opponent_name(self, opponent_name):
        """
        sets a new opponent name above the opponent's map.
        :param opponent_name: the name of the opponent
        """
        legend_height = UIData.battle['info bar']['height']
        map_box_width = UIData.battle['map']['box']['width']
        clear_string = ' ' * UIData.title['prompts']['input']['input limit']

        name_position_center = (1 + 3*Window._margin + map_box_width +
                                map_box_width//2)
        self._win.addstr(   #clear out any previous name string
            legend_height + Window._margin,
            name_position_center - len(clear_string)//2,
            clear_string
        )
        self._win.addstr(
            legend_height + Window._margin,
            name_position_center - len(opponent_name)//2,
            opponent_name, UIData.colors['opponent name']
        )