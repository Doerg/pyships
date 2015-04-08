import curses
import curses.panel
from client import ColorDefinitions as Colors


### window layout data ###

# logo
logo_hpad = 1
logo_vpad = 3
logo_vert_loc = 0.1

# name/ip prompt
name_text = "Your name:"
ip_text = "Host IP:"
logon_hpad = 3
logon_vpad = 1
logon_vert_loc = 0.7
logon_input_offset = len(
    max((name_text, ip_text), key=lambda s: len(s))
) + 2*logon_hpad
logon_input_limit = 15
logon_width = logon_input_offset + logon_input_limit + logon_hpad
logon_height = 3

# exit prompt
exit_text = "Connection could not be established! Exit? (y/n)"
exit_hpad = 3
exit_vpad = 1
exit_height = 3
exit_width = len(exit_text) + 2*exit_hpad
exit_vert_loc = 0.75



### classes ###

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


    def clear(self):
        self._win.bkgd(Colors.CLEAR)
        self._win.clear()


    def _place_water(self):
        """
        puts water tokens on the background window.
        """
        self._win.bkgdset(' ', Colors.OCEAN)
        for row in range(curses.LINES):
            for col in range(curses.COLS):
                try:
                    self._win.addstr(row, col, '~∽'[(row+col) % 2])
                except curses.error:
                    pass


    def _place_ships(self):
        """
        puts decorative ships on the background window.
        """
        vert_center = curses.LINES//2

        self._win.bkgdset(' ', Colors.SHIP)
        self._win.addstr(vert_center - 15, 17, '▲')
        self._win.addstr(vert_center - 14, 17, '▣')
        self._win.addstr(vert_center - 13, 17, '▼')

        self._win.addstr(vert_center,     8, '▲')
        self._win.addstr(vert_center + 1, 8, '▣')
        self._win.addstr(vert_center + 2, 8, '▣')
        self._win.addstr(vert_center + 3, 8, '▼')

        self._win.addstr(vert_center + 12, 14, '▲')
        self._win.addstr(vert_center + 13, 14, '▣')
        self._win.addstr(vert_center + 14, 14, '▼')

        self._win.addstr(vert_center - 5, curses.COLS-15, '◀ ▶')
        self._win.addstr(vert_center, curses.COLS-18, '◀ ▣ ▣ ▶')
        self._win.addstr(vert_center + 6, curses.COLS-13, '◀ ▶')


    def _place_logo(self):
        """
        places the pyships logo on the background. uses an extra curses window
        to achieve this.
        """
        logo = [line for line in open("assets/front_logo.txt")]
        logo_height = len(logo)
        logo_width = len(max(logo, key=lambda line: len(line)))

        self._logo_box = curses.newwin(
            logo_height + logo_vpad*2,
            logo_width + logo_hpad*2,
            int(curses.LINES * logo_vert_loc),
            curses.COLS//2 - logo_width//2
        )

        self._logo_box.bkgd(' ', Colors.LOGO_BOX)
        self._logo_box.box()

        self._logo_box.bkgdset(' ', curses.A_BOLD | Colors.LOGO_BOX)
        for y, row in enumerate(logo):
            for x, cell in enumerate(row.rstrip()):
                try:
                    self._logo_box.addstr(y + logo_vpad, x + logo_hpad, cell)
                except curses.error:
                    pass



# don't instantiate this class directly, choose one of NamePrompt and IpPrompt!
class LogonPrompt(Panel):
    """
    generic class to be inherited from NamePrompt and IpPrompt.
    """
    def __init__(self, text, vert_offset=0):
        super().__init__(
            logon_height, logon_width,
            int(curses.LINES * logon_vert_loc) + vert_offset,
            curses.COLS//2 - logon_width//2
        )

        self._win.bkgd(' ', Colors.PROMPT_BOX)
        self._win.box()
        self._win.addstr(logon_vpad, logon_hpad, text, curses.A_BOLD)


    def show(self):
        """
        clears out all previous user input in this prompt using blanks before
        displaying the prompt.
        """
        self._win.addstr(1, logon_input_offset, ' ' * logon_input_limit)
        super().show()


    def get_input(self):
        """
        queries user string input from this prompt.
        """
        curses.echo()
        curses.curs_set(True)
        user_input = self._win.getstr(1, logon_input_offset, logon_input_limit)
        return user_input.rstrip()



class NamePrompt(LogonPrompt):
    """
    panel asking for the user name.
    """
    def __init__(self):
        super().__init__(name_text)



class IpPrompt(LogonPrompt):
    """
    panel asking for the host ip.
    """
    def __init__(self):
        super().__init__(ip_text, vert_offset=6)



class ExitPrompt(Panel):
    """
    panel asking whether user wants to exit the program.
    """
    def __init__(self):
        super().__init__(
            exit_height, exit_width,
            int(curses.LINES * exit_vert_loc),
            curses.COLS//2 - exit_width//2
        )

        self._win.bkgd(' ', Colors.PROMPT_BOX)
        self._win.box()
        self._win.addstr(exit_vpad, exit_hpad, exit_text, curses.A_BOLD)


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