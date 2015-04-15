import curses
import curses.panel


class Panel(object):
    """
    title screen consists of showable / hidable panels. this means that all
    frontend window classes are expected to inherit from this base class.
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