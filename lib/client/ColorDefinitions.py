import curses

OCEAN = 1
SHIP = 2
LOGO_BOX = 3
PROMPT_BOX = 4

def init_colors():
    """
    initialises user defined color pairs for curses, using descriptive
    constants as numeration integers.
    """
    curses.init_pair(OCEAN, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(SHIP, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(LOGO_BOX, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(PROMPT_BOX, curses.COLOR_BLACK, curses.COLOR_WHITE)