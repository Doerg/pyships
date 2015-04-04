import curses
import curses.panel
from client import ColorDefinitions as Colors


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
    def __init__(self):
        super().__init__(curses.LINES, curses.COLS, 0, 0)

        self._place_water()
        self._place_ships()
        self._place_logo()


    def refresh(self):
        """
        redraws the whole screen.
        """
        self._win.refresh()
        self._logo_box.refresh()    #needs extra refresh to not be hidden


    def _place_water(self):
        """
        puts water tokens on the background window.
        """
        for row in range(curses.LINES):
            for col in range(curses.COLS):
                try:
                    self._win.addstr(
                        row, col, '~∽'[(row+col) % 2],
                        Colors.OCEAN
                    )
                except curses.error:
                    pass


    def _place_ships(self):
        """
        puts decorative ships on the background window.
        """
        vert_center = curses.LINES//2

        self._win.addstr(vert_center - 15, 17, '▲', Colors.SHIP)
        self._win.addstr(vert_center - 14, 17, '▣', Colors.SHIP)
        self._win.addstr(vert_center - 13, 17, '▼', Colors.SHIP)

        self._win.addstr(vert_center,     8, '▲', Colors.SHIP)
        self._win.addstr(vert_center + 1, 8, '▣', Colors.SHIP)
        self._win.addstr(vert_center + 2, 8, '▣', Colors.SHIP)
        self._win.addstr(vert_center + 3, 8, '▼', Colors.SHIP)

        self._win.addstr(vert_center + 12, 14, '▲', Colors.SHIP)
        self._win.addstr(vert_center + 13, 14, '▣', Colors.SHIP)
        self._win.addstr(vert_center + 14, 14, '▼', Colors.SHIP)

        self._win.addstr(
            vert_center - 5, curses.COLS-15, '◀ ▶',
            Colors.SHIP
        )
        self._win.addstr(
            vert_center, curses.COLS-18, '◀ ▣ ▣ ▶',
            Colors.SHIP
        )
        self._win.addstr(
            vert_center + 6, curses.COLS-13, '◀ ▶',
            Colors.SHIP
        )


    def _place_logo(self):
        """
        places the pyships logo on the background. uses an extra curses window
        to achieve this.
        """
        logo = [line for line in open("assets/front_logo.txt")]
        logo_height = len(logo)
        logo_width = len(max(logo, key=lambda line: len(line)))
        hor_padding = 1
        vert_padding = 3

        self._logo_box = curses.newwin(
            logo_height + vert_padding*2, logo_width + hor_padding*2,
            4, curses.COLS//2 - logo_width//2
        )

        self._logo_box.bkgd(' ', Colors.LOGO_BOX)
        self._logo_box.box()

        for y, row in enumerate(logo):
            for x, cell in enumerate(row.rstrip()):
                try:
                    self._logo_box.addstr(
                        y + vert_padding, x + hor_padding, cell
                    )
                except curses.error:
                    pass



# don't instantiate this class directly, choose one of NamePrompt and IpPrompt!
class LogonPrompt(Panel):
    """
    generic class to be inherited from NamePrompt and IpPrompt.
    """
    def __init__(self, text, vert_offset=0):
        self._input_offset = 14
        self._input_limit = 15
        hor_padding = 3
        vert_padding = 1
        win_height = 3
        win_width = 32
        rel_vert_location = 0.7

        super().__init__(
            win_height, win_width,
            int(curses.LINES * rel_vert_location) + vert_offset,
            curses.COLS//2 - win_width//2
        )

        self._win.box()
        self._win.bkgd(' ', Colors.PROMPT_BOX)
        self._win.addstr(vert_padding, hor_padding, text, curses.A_BOLD)


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
        self._win.getstr(1, self._input_offset, self._input_limit).rstrip()



class NamePrompt(LogonPrompt):
    """
    panel asking for the user name.
    """
    def __init__(self):
        super().__init__("Your name:")



class IpPrompt(LogonPrompt):
    """
    panel asking for the host ip.
    """
    def __init__(self):
        super().__init__("Host IP:", vert_offset=6)



class ExitPrompt(Panel):
    """
    panel asking whether user wants to exit the program.
    """
    def __init__(self):
        text = "Connection could not be established! Exit? (y/n)"
        hor_padding = 3
        vert_padding = 1
        win_height = 3
        win_width = len(text) + 2*hor_padding
        rel_vert_location = 0.75

        super().__init__(
            win_height, win_width,
            int(curses.LINES * rel_vert_location),
            curses.COLS//2 - win_width//2
        )

        self._win.box()
        self._win.bkgd(' ', Colors.PROMPT_BOX)
        self._win.addstr(vert_padding, hor_padding, text, curses.A_BOLD)


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
