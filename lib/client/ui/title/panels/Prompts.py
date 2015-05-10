from .Panel import Panel
from client.ui import UIData
import curses


class Prompt(Panel):
    """
    prompt parent class. don't instantiate directly.
    """
    _ui_data = UIData.title['prompts']['general']
    _height = _ui_data['height']
    _rel_vert_loc = _ui_data['relative vertical location']
    _hpadding = _ui_data['hpadding']
    _vpadding = _ui_data['vpadding']

    def __init__(self, prompt_type):
        super().__init__(
            self._height, self._width,
            int(curses.LINES * self._rel_vert_loc),
            curses.COLS//2 - self._width//2
        )

        self._win.bkgd(' ', UIData.colors['prompt box'])
        self._win.box()
        self._text = self._texts[prompt_type]



class InputPrompt(Prompt):
    """
    prompt that asks the user to enter some text.
    """
    _ui_data = UIData.title['prompts']['input']
    _width = _ui_data['width']
    _texts = _ui_data['texts']
    _input_offset = _ui_data['input offset']
    _input_limit = _ui_data['input limit']

    def __init__(self, prompt_type):
        super().__init__(prompt_type)
        self._win.addstr(
            self._vpadding, self._hpadding, self._text, curses.A_BOLD
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
    _width = _ui_data['width']
    _texts = _ui_data['texts']


    def __init__(self, prompt_type):
        super().__init__(prompt_type)
        text_offset = (self._width - len(self._text)) // 2
        self._win.addstr(
            self._vpadding, text_offset, self._text, curses.A_BOLD
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