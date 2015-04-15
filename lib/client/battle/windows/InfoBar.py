import curses
from .Window import Window
from client import UIData


class InfoBar(Window):
    """
    common ancestor class for MessageBar and KeyLegend. don't instantiate
    directly, use MessageBar and KeyLegend instead.
    """
    _ui_data = UIData.battle['info bar']
    _width = _ui_data['width']
    _height = _ui_data['height']
    _padding = _ui_data['padding']
    _content_width = _width - _padding - 1

    def __init__(self, y, x):
        """
        common constructor for info bars. only needs the y and x coordinates
        as arguments b/c all info bars have the same size.
        :param y: row offset of the window in respect to the content frame
        :param x: column offset of the window in respect to the content frame
        """
        self._text_line = self._height//2
        super().__init__(self._height, self._width, y, x)


    def _clear(self, color):
        """
        clears the info bar using blanks.
        :param color: the color with which to clear the bar
        """
        self._win.addstr(
            self._text_line, self._padding, ' ' * self._content_width, color
        )



class KeyLegend(InfoBar):
    """
    info bar which contains the currently usable keys, plus their descriptions.
    """
    _ship_placement_keys = InfoBar._ui_data['legend keys']['ship placement']
    _battle_keys = InfoBar._ui_data['legend keys']['battle']

    def __init__(self):
        super().__init__(1, Window._margin + 1)

        self._win.bkgd(' ', UIData.colors['legend'])
        self._win.bkgdset(' ', curses.A_BOLD)

        self.set_ship_placement_keys()


    def set_ship_placement_keys(self):
        """
        set key descriptions for initial ship placement.
        """
        self._set_keys(self._ship_placement_keys)


    def set_battle_keys(self):
        """
        set key descriptions for battle mode.
        """
        self._set_keys(self._battle_keys)


    def _set_keys(self, keys):
        """
        puts a new key description into the key legend.
        :param keys: a list of tuples holding pairs of key/description strings
        """
        self._clear()
        self._win.move(self._text_line, 1)

        for key, description in keys:
            self._append_key(key, description)


    def _clear(self):
        """
        fills key legend with blanks in order to clear it.
        """
        super()._clear(UIData.colors['legend'])


    def _append_key(self, key, description):
        """
        appends a key/description pair to the key legend.
        :param key: name of the key
        :param description: description of the key
        """
        self._win.addstr(
            ' ' * InfoBar._padding + key + ': ', UIData.colors['legend']
        )
        self._win.addstr('  %s  ' % description, UIData.colors['legend entry'])



class MessageBar(InfoBar):
    """
    bar used for displaying ingame messages to the player. these messages
    include instructions, enemy moves, current state of the game, etc.
    """
    def __init__(self):
        map_box_height = UIData.battle['map']['box']['height']

        super().__init__(
            InfoBar._height + map_box_height + 2*Window._margin + 1,
            Window._margin + 1
        )

        self._win.bkgd(' ', UIData.colors['message'])
        self._win.bkgdset(' ', curses.A_BOLD | UIData.colors['message'])


    def put_message(self, message):
        """
        writes the given message into the message bar.
        :param message: the message to write
        """
        self._clear()
        self._win.addnstr(
            self._text_line, InfoBar._padding, message, InfoBar._content_width
        )


    def _clear(self):
        """
        fills message bar with blanks in order to clear it.
        """
        super()._clear(UIData.colors['message'])