import curses
import curses.panel
from client import UIData


class Panel(object):
    """
    title screen consists of showable / hidable panels. this means that all
    classes in this module are expected to inherit from this base class.
    """
    def __init__(self, height, width, y, x):
        self._win = curses.newwin(height, width, y, x)
        self._panel = curses.panel.new_panel(self._win)


    def show(self):
        """
        redraw the window belonging to this panel and make this panel visible.
        """
        self._win.refresh()
        self._panel.show()


    def hide(self):
        """
        make this panel invisible.
        """
        self._panel.hide()



class Background(Panel):
    """
    title screen backround including ocean, ships and pyships logo.
    """
    _logo = [line for line in open("assets/front_logo.txt")]
    _logo_height = len(_logo)
    _logo_width = len(max(_logo, key=lambda line: len(line)))
    _logo_hpadding = UIData.intro['logo']['hpadding']
    _logo_vpadding = UIData.intro['logo']['vpadding']
    _logo_rel_vert_loc = UIData.intro['logo']['relative vertical location']
    _water_tokens = UIData.tokens['ocean']
    _ship_tokens = UIData.tokens['ship']

    def __init__(self):
        super().__init__(curses.LINES, curses.COLS, 0, 0)

        self._place_water()
        self._place_ships()
        self._place_logo()


    def update(self):
        """
        redraws the whole screen.
        """
        self._win.refresh()
        self._logo_box.refresh()    #needs extra refresh to not be hidden


    def clear(self):
        """
        removes all content from the background.
        """
        self._win.bkgd(UIData.colors['clear'])
        self._win.clear()


    def _place_water(self):
        """
        puts water tokens on the background window.
        """
        self._win.bkgdset(' ', UIData.colors['ocean'])
        for row in range(curses.LINES):
            for col in range(curses.COLS):
                try:
                    self._win.addstr(
                        row, col, self._water_tokens[(row+col) % 2]
                    )
                except curses.error:
                    pass


    def _place_ships(self):
        """
        puts decorative ships on the background window.
        """
        front_hor = self._ship_tokens['horizontal']['front']
        back_hor = self._ship_tokens['horizontal']['back']
        front_vert = self._ship_tokens['vertical']['front']
        back_vert = self._ship_tokens['vertical']['back']
        center = self._ship_tokens['center']

        vert_middle = curses.LINES//2

        self._win.bkgdset(' ', UIData.colors['ship'])
        self._win.addstr(vert_middle - 15, 17, front_vert)
        self._win.addstr(vert_middle - 14, 17, center)
        self._win.addstr(vert_middle - 13, 17, back_vert)

        self._win.addstr(vert_middle,     8, front_vert)
        self._win.addstr(vert_middle + 1, 8, center)
        self._win.addstr(vert_middle + 2, 8, center)
        self._win.addstr(vert_middle + 3, 8, back_vert)

        self._win.addstr(vert_middle + 12, 14, front_vert)
        self._win.addstr(vert_middle + 13, 14, center)
        self._win.addstr(vert_middle + 14, 14, back_vert)

        self._win.addstr(
            vert_middle - 5, curses.COLS-15, ' '.join((front_hor, back_hor))
        )
        self._win.addstr(
            vert_middle, curses.COLS-18,
            ' '.join((front_hor, center, center, back_hor))
        )
        self._win.addstr(
            vert_middle + 6, curses.COLS-13, ' '.join((front_hor, back_hor))
        )


    def _place_logo(self):
        """
        places the pyships logo on the background. uses an extra curses window
        to achieve this.
        """
        self._logo_box = curses.newwin(
            self._logo_height + self._logo_vpadding*2,
            self._logo_width + self._logo_hpadding*2,
            int(curses.LINES * self._logo_rel_vert_loc),
            curses.COLS//2 - self._logo_width//2
        )

        self._logo_box.bkgd(' ', UIData.colors['logo box'])
        self._logo_box.box()

        self._logo_box.bkgdset(' ', curses.A_BOLD | UIData.colors['logo box'])
        for y, row in enumerate(self._logo):
            for x, cell in enumerate(row.rstrip()):
                try:
                    self._logo_box.addstr(
                        y + self._logo_vpadding, x + self._logo_hpadding, cell
                    )
                except curses.error:
                    pass



class LogonPrompt(Panel):
    """
    generic class to be inherited from NamePrompt and IpPrompt. don't
    directly, choose one of NamePrompt and IpPrompt instead.
    """
    _ui_data = UIData.intro['logon prompt']
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
        """
        curses.echo()
        curses.curs_set(True)
        user_input = self._win.getstr(1, self._input_offset, self._input_limit)
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
            UIData.intro['logon prompt']['ip text'],
            vert_offset=self._vert_offset
        )



class ExitPrompt(Panel):
    """
    panel asking whether user wants to exit the program.
    """
    _ui_data = UIData.intro['exit prompt']
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
        """
        curses.noecho()
        curses.curs_set(False)

        while True:
            answer = self._win.getkey().upper()
            if answer == 'Y':
                return True
            elif answer == 'N':
                return False