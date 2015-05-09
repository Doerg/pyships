import curses
from .Panel import Panel
from ui import UIData


class LogonPrompt(Panel):
    """
    generic class to be inherited from NamePrompt and IpPrompt. don't
    instantiate directly, choose one of NamePrompt and IpPrompt instead.
    """
    _ui_data = UIData.title['logon prompt']
    _input_offset = _ui_data['input offset']
    _input_limit = _ui_data['input limit']
    _height = _ui_data['height']
    _width = _ui_data['width']
    _rel_vert_loc = _ui_data['relative vertical location']
    _hpadding = _ui_data['hpadding']
    _vpadding = _ui_data['vpadding']

    def __init__(self, text, vert_offset=0):
        super().__init__(
            self._height, self._width,
            int(curses.LINES * self._rel_vert_loc) + vert_offset,
            curses.COLS//2 - self._width//2
        )

        self._win.bkgd(' ', UIData.colors['prompt box'])
        self._win.box()
        self._win.addstr(self._vpadding, self._hpadding, text, curses.A_BOLD)


    def show(self):
        """
        clears out all previous user input in this prompt using blanks before
        displaying the prompt.
        """
        self._win.addstr(1, self._input_offset, ' ' * self._input_limit)
        super().show()


    def get_input(self):
        """
        queries user string input from this prompt.
        :return: user string input
        """
        curses.echo()
        curses.curs_set(True)
        user_input = self._win.getstr(1, self._input_offset, self._input_limit)
        curses.curs_set(False)
        curses.noecho()

        return user_input.rstrip()



class NamePrompt(LogonPrompt):
    """
    panel asking for the user name.
    """
    _text = LogonPrompt._ui_data['name text']

    def __init__(self):
        super().__init__(self._text)



class IpPrompt(LogonPrompt):
    """
    panel asking for the host ip.
    """
    _text = LogonPrompt._ui_data['ip text']
    _vert_offset = LogonPrompt._ui_data['gap']

    def __init__(self):
        super().__init__(
            UIData.title['logon prompt']['ip text'],
            vert_offset=self._vert_offset
        )



class ExitPrompt(Panel):
    """
    panel asking whether the user wants to retry connecting to the server or
    exit the program.
    """
    _ui_data = UIData.title['exit prompt']
    _text = _ui_data['text']
    _hpadding = _ui_data['hpadding']
    _vpadding = _ui_data['vpadding']
    _rel_vert_loc = _ui_data['relative vertical location']
    _height = _ui_data['height']
    _width = _ui_data['width']

    def __init__(self):
        super().__init__(
            self._height, self._width,
            int(curses.LINES * self._rel_vert_loc),
            curses.COLS//2 - self._width//2
        )

        self._win.bkgd(' ', UIData.colors['prompt box'])
        self._win.box()
        self._win.addstr(
            self._vpadding, self._hpadding, self._text, curses.A_BOLD
        )


    def get_answer(self):
        """
        asks the user to press either 'y' or 'n'. doesn't accept other input.
        :return: True for input 'Y/y', False for input 'N/n'
        """
        curses.noecho()
        curses.curs_set(False)

        while True:
            answer = self._win.getkey().upper()
            if answer == 'Y':
                return True
            elif answer == 'N':
                return False