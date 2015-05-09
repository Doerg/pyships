import curses
from .Panel import Panel
from ui import UIData


class Background(Panel):
    """
    title screen backround including ocean, ships and pyships logo.
    """
    _logo = [line for line in open("assets/front_logo.txt")]
    _logo_height = len(_logo)
    _logo_width = len(max(_logo, key=lambda line: len(line)))
    _logo_hpadding = UIData.title['logo']['hpadding']
    _logo_vpadding = UIData.title['logo']['vpadding']
    _logo_rel_vert_loc = UIData.title['logo']['relative vertical location']
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