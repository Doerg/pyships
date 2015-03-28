#!/usr/bin/env python3.4

import curses
import curses.panel

def run(stdscr):
    logo = [line for line in open("front_logo.txt")]
    logo_height = len(logo)
    logo_width = len(logo[0])

    main_pane = curses.panel.new_panel(curses.newwin(
        curses.LINES, curses.COLS, 0, 0
    ))
    logo_pane = curses.panel.new_panel(curses.newwin(
        logo_height+5, logo_width+2, 4, curses.COLS//2 - logo_width//2
    ))
    name_pane = curses.panel.new_panel(curses.newwin(
        3, 32, int(curses.LINES * 0.7), curses.COLS//2 - 16
    ))
    ip_pane = curses.panel.new_panel(curses.newwin(
        3, 32, int(curses.LINES * 0.7) + 6, curses.COLS//2 - 16
    ))

    logo_pane.window().box()
    name_pane.window().box()
    ip_pane.window().box()

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
    main_pane.window().bkgd('~', curses.color_pair(1))
    logo_pane.window().bkgd(' ', curses.color_pair(3))
    name_pane.window().bkgd(' ', curses.color_pair(2))
    ip_pane.window().bkgd(' ', curses.color_pair(2))

    main_pane.window().addstr(curses.LINES//2, 8, '▲', curses.color_pair(4))
    main_pane.window().addstr(curses.LINES//2 + 1, 8, '▣', curses.color_pair(4))
    main_pane.window().addstr(curses.LINES//2 + 2, 8, '▣', curses.color_pair(4))
    main_pane.window().addstr(curses.LINES//2 + 3, 8, '▼', curses.color_pair(4))

    main_pane.window().addstr(
        curses.LINES//2, curses.COLS-15, '◀-▣-▣-▶',
        curses.color_pair(4)
    )

    for y, row in enumerate(logo):
        for x, cell in enumerate(row.rstrip()):
            try:
                logo_pane.window().addstr(y+1, x+1, cell)
            except curses.error:
                pass
    name_pane.window().addstr(1, 3, "Your name: ", curses.A_BOLD)
    ip_pane.window().addstr(1, 3, "Host IP:   ", curses.A_BOLD)

    main_pane.window().refresh()
    logo_pane.window().refresh()
    name_pane.window().refresh()
    ip_pane.window().refresh()

    curses.echo()
    name_pane.window().getstr(1, 14, 15)
    ip_pane.window().getstr(1, 14, 15)
    curses.noecho()

    ip_pane.hide()
    name_pane.hide()
    logo_pane.move(
        5, 5
        #curses.LINES//2 - logo_height//2, curses.COLS//2 - logo_width//2
    )
    logo_pane.window().refresh()

    curses.curs_set(False)
    main_pane.window().getch()


curses.wrapper(run)
