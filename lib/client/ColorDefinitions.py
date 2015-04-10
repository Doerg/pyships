import curses


def init_colors():
    """
    initialises user defined color pairs for curses, using descriptive
    constants. curses color pairs can only be set after curses.initscr() has
    been executed. therefore this method has to be called after the fact.
    """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(14, curses.COLOR_RED, curses.COLOR_BLUE)

    global CLEAR, OCEAN, SHIP, LOGO_BOX, PROMPT_BOX, CONTENT_FRAME, PLAYER_NAME
    global OPPONENT_NAME, LEGEND, LEGEND_ENTRY, MESSAGE, BATTLE_FRAME
    global PLACEABLE_SHIP, BLOCKED_SHIP

    CLEAR = curses.color_pair(1)
    OCEAN = curses.color_pair(2)
    SHIP = curses.color_pair(3)
    LOGO_BOX = curses.color_pair(4)
    PROMPT_BOX = curses.color_pair(5)
    CONTENT_FRAME = curses.color_pair(6)
    PLAYER_NAME = curses.color_pair(7)
    OPPONENT_NAME = curses.color_pair(8)
    LEGEND = curses.color_pair(9)
    LEGEND_ENTRY = curses.color_pair(10)
    MESSAGE = curses.color_pair(11)
    BATTLE_FRAME = curses.color_pair(12)
    PLACEABLE_SHIP = curses.color_pair(13)
    BLOCKED_SHIP = curses.color_pair(14)