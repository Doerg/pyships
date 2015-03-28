import curses
from client import ColorDefinitions as Colors


def init(stdscr):
    global _stdscr
    _stdscr = stdscr
    Colors.init_colors()
    _setup_background()


def display_background():
    _stdscr.refresh()
    _bkgd_win.refresh()
    _logo_win.refresh()


def logon_prompt():
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
    input_offset = len(max((name_prompt, ip_prompt), key=lambda s: len(s))) + 4
    input_limit = 15

    name_win.addstr(1, 3, name_prompt, curses.A_BOLD)
    ip_win.addstr(1, 3, ip_prompt, curses.A_BOLD)

    name_win.refresh()
    ip_win.refresh()

    curses.echo()
    name = name_win.getstr(1, input_offset, input_limit)
    ip = ip_win.getstr(1, input_offset, input_limit)
    curses.noecho()

    return name, ip


def exit_prompt():
    _stdscr.getch()
    return True


### PRIVATE METHODS ###

def _setup_background():
    global _bkgd_win, _logo_win

    logo = [line for line in open("assets/front_logo.txt")]
    logo_height = len(logo)
    logo_width = len(max(logo, key=lambda line: len(line)))

    _bkgd_win = curses.newwin(
        curses.LINES, curses.COLS, 0, 0
    )
    _logo_win = curses.newwin(
        logo_height+5, logo_width+2, 4, curses.COLS//2 - logo_width//2
    )

    _setup_ocean(_bkgd_win)
    _setup_logo(_logo_win, logo)


def _setup_ocean(bkgd_win):
    win_height, win_width = bkgd_win.getmaxyx()

    for row in range(win_height):
        for col in range(win_width):
            try:
                bkgd_win.addstr(
                    row, col, '~∽'[(row+col) % 2],
                    curses.color_pair(Colors.OCEAN)
                )
            except curses.error:
                pass

    bkgd_win.bkgd(' ', curses.color_pair(Colors.OCEAN))

    bkgd_win.addstr(win_height//2, 8, '▲', curses.color_pair(Colors.SHIP))
    bkgd_win.addstr(win_height//2 + 1, 8, '▣', curses.color_pair(Colors.SHIP))
    bkgd_win.addstr(win_height//2 + 2, 8, '▣', curses.color_pair(Colors.SHIP))
    bkgd_win.addstr(win_height//2 + 3, 8, '▼', curses.color_pair(Colors.SHIP))

    bkgd_win.addstr(
        win_height//2, win_width-15, '◀ ▣ ▣ ▶',
        curses.color_pair(Colors.SHIP)
    )


def _setup_logo(logo_win, logo):
    logo_win.bkgd(' ', curses.color_pair(Colors.LOGO_BOX))
    logo_win.box()

    for y, row in enumerate(logo):
        for x, cell in enumerate(row.rstrip()):
            try:
                logo_win.addstr(y+1, x+1, cell)
            except curses.error:
                pass
