import curses


def init_colors():
    """
    initialises user defined color pairs for curses, using descriptive
    constants as numeration integers.
    """
    ocean = 1
    ship = 2
    logo_box = 3
    prompt_box = 4

    curses.init_pair(ocean, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(ship, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(logo_box, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(prompt_box, curses.COLOR_BLACK, curses.COLOR_WHITE)

    global OCEAN, SHIP, LOGO_BOX, PROMPT_BOX
    OCEAN = curses.color_pair(ocean)
    SHIP = curses.color_pair(ship)
    LOGO_BOX = curses.color_pair(logo_box)
    PROMPT_BOX = curses.color_pair(prompt_box)
