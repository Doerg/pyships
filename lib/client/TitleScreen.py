import curses
import curses.panel
from client import ColorDefinitions as Colors


def init():
    """
    initialises all the panels of the title screen.
    displays background and logo panels.
    """
    global _main_panel, _logo_panel, _name_panel, _ip_panel, _exit_panel

    Colors.init_colors()
    _main_panel = _setup_background()
    _logo_panel = _setup_logo()
    _name_panel, _ip_panel = _setup_logon_panels()
    _exit_panel = _setup_exit_panel()

    _main_panel.window().refresh()
    _logo_panel.window().refresh()


def logon_prompt():
    """
    prompts the user for logon data.
    :return: user name and host ip as strings
    """
    input_offset = 14
    input_limit = 15
                                            #delete last user input
    _name_panel.window().addstr(1, input_offset, ' ' * input_limit)
    _ip_panel.window().addstr(1, input_offset, ' ' * input_limit)

    _exit_panel.hide()
    _name_panel.show()
    _ip_panel.show()

    _main_panel.window().refresh()
    _name_panel.window().refresh()
    _ip_panel.window().refresh()

    curses.echo()
    curses.curs_set(True)                   #collect user input
    name = _name_panel.window().getstr(1, input_offset, input_limit).rstrip()
    ip = _ip_panel.window().getstr(1, input_offset, input_limit).rstrip()

    return name, ip


def exit_prompt():
    """
    asks the user if he wants to exit the program.
    :return: True if user wants to exit, False otherwise
    """
    _name_panel.hide()
    _ip_panel.hide()
    _exit_panel.show()

    _main_panel.window().refresh()
    _exit_panel.window().refresh()

    curses.noecho()
    curses.curs_set(False)

    while True:         #collect answer
        answer = _exit_panel.window().getkey().upper()
        if answer == 'Y':
            return True
        elif answer == 'N':
            break



### PRIVATE METHODS ###

def _setup_background():
    main_win = curses.newwin(curses.LINES, curses.COLS, 0, 0)

    for row in range(curses.LINES):     #place water
        for col in range(curses.COLS):
            try:
                main_win.addstr(
                    row, col, '~∽'[(row+col) % 2],
                    curses.color_pair(Colors.OCEAN)
                )
            except curses.error:
                pass

    #place decorational ships
    vert_center = curses.LINES//2

    main_win.addstr(vert_center - 15, 17, '▲', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center - 14, 17, '▣', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center - 13, 17, '▼', curses.color_pair(Colors.SHIP))

    main_win.addstr(vert_center,     8, '▲', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center + 1, 8, '▣', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center + 2, 8, '▣', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center + 3, 8, '▼', curses.color_pair(Colors.SHIP))

    main_win.addstr(vert_center + 12, 14, '▲', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center + 13, 14, '▣', curses.color_pair(Colors.SHIP))
    main_win.addstr(vert_center + 14, 14, '▼', curses.color_pair(Colors.SHIP))

    main_win.addstr(
        vert_center - 5, curses.COLS-15, '◀ ▶',
        curses.color_pair(Colors.SHIP)
    )
    main_win.addstr(
        vert_center, curses.COLS-18, '◀ ▣ ▣ ▶',
        curses.color_pair(Colors.SHIP)
    )
    main_win.addstr(
        vert_center + 6, curses.COLS-13, '◀ ▶',
        curses.color_pair(Colors.SHIP)
    )

    return curses.panel.new_panel(main_win)


def _setup_logo():
    logo = [line for line in open("assets/front_logo.txt")]
    logo_height = len(logo)
    logo_width = len(max(logo, key=lambda line: len(line)))
    hor_padding = 1
    vert_padding = 3

    logo_win = curses.newwin(
        logo_height + vert_padding*2, logo_width + hor_padding*2,
        4, curses.COLS//2 - logo_width//2
    )

    logo_win.bkgd(' ', curses.color_pair(Colors.LOGO_BOX))
    logo_win.box()

    for y, row in enumerate(logo):
        for x, cell in enumerate(row.rstrip()):
            try:
                logo_win.addstr(y + vert_padding, x + hor_padding, cell)
            except curses.error:
                pass

    return curses.panel.new_panel(logo_win)


def _setup_logon_panels():
    hor_padding = 3
    vert_padding = 1
    win_height = 3
    win_width = 32
    space_between_wins = 6
    rel_vert_location = 0.7

    name_win = curses.newwin(
        win_height, win_width,
        int(curses.LINES * rel_vert_location),
        curses.COLS//2 - win_width//2
    )
    ip_win = curses.newwin(
        win_height, win_width,
        int(curses.LINES * rel_vert_location) + space_between_wins,
        curses.COLS//2 - win_width//2
    )

    name_win.box()
    ip_win.box()

    name_win.bkgd(' ', curses.color_pair(Colors.PROMPT_BOX))
    ip_win.bkgd(' ', curses.color_pair(Colors.PROMPT_BOX))

    name_prompt = "Your name:"
    ip_prompt = "Host IP:"

    name_win.addstr(vert_padding, hor_padding, name_prompt, curses.A_BOLD)
    ip_win.addstr(vert_padding, hor_padding, ip_prompt, curses.A_BOLD)

    return curses.panel.new_panel(name_win), curses.panel.new_panel(ip_win)


def _setup_exit_panel():
    exit_prompt = "Connection could not be established! Exit? (y/n)"
    hor_padding = 3
    vert_padding = 1
    win_height = 3
    win_width = len(exit_prompt) + 2*hor_padding
    rel_vert_location = 0.75

    exit_win = curses.newwin(
        win_height, win_width,
        int(curses.LINES * rel_vert_location),
        curses.COLS//2 - win_width//2
    )

    exit_win.box()
    exit_win.bkgd(' ', curses.color_pair(Colors.PROMPT_BOX))
    exit_win.addstr(vert_padding, hor_padding, exit_prompt, curses.A_BOLD)

    return curses.panel.new_panel(exit_win)