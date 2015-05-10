import curses
from client.ui import UIData


class Window(object):
    """
    base class for all window objects.
    """
    _margin = UIData.battle['window margin']

    def __init__(self, height, width, y, x):
        """
        initializer for all windows. the y and x values are interpreted as
        offsets from the upper left corner of the central frame window.
        :param height: number of rows of the window
        :param width: number of columns of the window
        :param y: row offset of the window in respect to the content frame
        :param x: column offset of the window in respect to the content frame
        """
        frame_height = UIData.battle['frame']['height']
        frame_width = UIData.battle['frame']['width']

        frame_y = curses.LINES//2 - frame_height//2
        frame_x = curses.COLS//2 - frame_width//2
        self._win = curses.newwin(height, width, frame_y + y, frame_x + x)
        self._win.box() #all windows on this screen are boxed


    def update(self):
        """
        redraw the window.
        """
        self._win.refresh()


    def get_key(self):
        """
        returns a keypress.
        :return: the key code of the pressed key
        """
        return self._win.getch()