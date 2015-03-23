#!/usr/bin/env python3.4

import curses

def run(stdscr):
    logo = [line for line in open("front_logo.txt")]
    logo_height = len(logo)
    logo_width = len(logo[0])

    logo_win = curses.newwin(
        logo_height+5, logo_width+2, 4, curses.COLS//2 - logo_width//2
    )
    upper_win = curses.newwin(
        4, 32, int(curses.LINES * 0.7), curses.COLS//2 - 16
    )
    lower_win = curses.newwin(
        4, 32, int(curses.LINES * 0.7) + 6, curses.COLS//2 - 16
    )

    logo_win.box()
    upper_win.box()
    lower_win.box()

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.bkgd('~', curses.color_pair(1))
    logo_win.bkgd(' ', curses.color_pair(3))
    upper_win.bkgd(' ', curses.color_pair(2))
    lower_win.bkgd(' ', curses.color_pair(2))

    for y, row in enumerate(logo):
        for x, cell in enumerate(row.rstrip()):
            try:
                logo_win.addstr(y+1, x+1, cell)
            except curses.error:
                pass
    upper_win.addstr(1, 10, "Your name: ", curses.A_BOLD)
    lower_win.addstr(1, 11, "Host IP: ", curses.A_BOLD)

    stdscr.refresh()
    logo_win.refresh()
    upper_win.refresh()
    lower_win.refresh()

    curses.echo()
    upper_win.getstr(2, 5)
    lower_win.getstr(2, 5)
    curses.noecho()

    curses.curs_set(False)
    upper_win.getch()


curses.wrapper(run)
