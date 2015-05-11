from .Panel import Panel
from client.ui import UIData
import curses


class Prompt(Panel):
    """
    prompt parent class. don't instantiate directly.
    """
    _ui_data = UIData.title['prompts']['common']
    _hpadding = _ui_data['hpadding']
    _vpadding = _ui_data['vpadding']

    def __init__(self, gap=False):
        """
        sets up a prompt with all the common graphical features.
        :param gap: True if the prompt has a vertical offset, False otherwise
        """
        vertical_gap = self._ui_data['gap height'] if gap else 0

        super().__init__(
            self._height, self._width,
            int(curses.LINES * self._rel_vert_loc) + vertical_gap,
            curses.COLS//2 - self._width//2
        )

        self._win.bkgd(' ', UIData.colors['prompt box'])
        self._win.box()



class InputPrompt(Prompt):
    """
    prompt that asks the user to enter some text.
    """
    _ui_data = UIData.title['prompts']['input']
    _rel_vert_loc = _ui_data['relative vertical location']
    _width = _ui_data['width']
    _height = _ui_data['height']
    _texts = _ui_data['texts']
    _input_offset = _ui_data['input offset']
    _input_limit = _ui_data['input limit']

    def __init__(self, text_key, gap=False):
        """
        sets up an input prompt.
        :param text_key: key to access the text of this prompt
        :param gap: True if the prompt has a vertical offset, False otherwise
        """
        super().__init__(gap)
        self._win.addstr(
            self._vpadding, self._hpadding, self._texts[text_key], curses.A_BOLD
        )


    def show(self):
        """
        clears out all previous user input in this prompt using blanks before
        displaying the prompt.
        """
        self._win.addstr(1, self._input_offset, ' ' * self._input_limit)
        super().show()


    def get_input(self):
        """
        queries user text input from this prompt.
        :return: user text input
        """
        curses.echo()
        curses.curs_set(True)
        while True:
            user_input = self._win.getstr(
                1, self._input_offset, self._input_limit
            )
            if user_input: break  # user input can't be empty
        curses.curs_set(False)
        curses.noecho()

        return user_input.rstrip()



class QuestionPrompt(Prompt):
    """
    prompt that asks the user a specific yes/no question.
    """
    _ui_data = UIData.title['prompts']['question']
    _rel_vert_loc = _ui_data['relative vertical location']
    _width = _ui_data['width']
    _height = _ui_data['height']
    _texts = _ui_data['texts']


    def __init__(self, text_key):
        """
        sets up a question prompt.
        :param text_key: key to access the text of this prompt
        """
        super().__init__()
        text = self._texts[text_key]
        text_offset = (self._width - len(text)) // 2
        self._win.addstr(self._vpadding, text_offset, text, curses.A_BOLD)


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



class HostList(Prompt):
    """
    panel that lists all available host and lets the user choose to either join
    one of those hosts or to host a game himself.
    """
    _ui_data = UIData.title['prompts']['host list']
    _rel_vert_loc = _ui_data['relative vertical location']
    _width = _ui_data['width']
    _height = _ui_data['height']
    _texts = _ui_data['texts']
    _list_length = _ui_data['max hosts']

    def __init__(self):
        super().__init__()
        self._win.addstr(
            self._vpadding, self._hpadding, self._texts['top'], curses.A_BOLD
        )
        self._win.addstr(
            self._height - self._vpadding - 1, self._hpadding,
            self._texts['bottom'], curses.A_BOLD
        )
        self._win.bkgdset(' ', UIData.colors['host list'] | curses.A_BOLD)


    def fill_hosts(self, available_hosts):
        """
        fills the host list with all currently available hosts.
        :param available_hosts: all currently available hosts
        """
        list_offset = self._vpadding + 1

        for index, host in enumerate(available_hosts, start=1):
            self._win.addstr(
                list_offset + index, self._hpadding,
                "%2d\t%-15s: %-16s" % (index, host['ip'], host['name'])
            )

        index += 1
        while index <= self._list_length:
            self._win.addstr(
                list_offset + index, self._hpadding,
                "%2d\t%-33s" % (index, "Free slot")
            )
            index += 1

        self._win.addstr(
            list_offset + index + 1, self._hpadding,
            " 0\t%-33s" % "Host a game yourself "
        )


    def select_host(self):
        """
        returns user input for this panel. allowed inputs are numbers 0-9 and
        the letter 'r'.
        :return: the selected host number as an integer, or the refresh key code
        """
        while True:
            key = self._win.getch()
            if key == UIData.key_codes['refresh']:
                return key
            if key in UIData.key_codes['hosts']:
                return key - ord('0')