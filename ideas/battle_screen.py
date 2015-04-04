#!/usr/bin/env python3.4

import curses

def run(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    key_win = curses.newwin(3, 80, 0, 0)
    key_win.bkgd(' ', curses.color_pair(2))
    key_win.box()
    key_win.addstr(1, 2, 'key legend here...', curses.color_pair(3))

    player_win = curses.newwin(18, 35, 4, 2)
    player_win.bkgd(' ', curses.color_pair(1))

    stdscr.addstr(3, 2, '1 2 3 4 5 6 7 8 9 A B C D E F G H I')
    for row in range(18):
        stdscr.addstr(4 + row, 0, 'abcdefghijklmnopqr'[row])

    height, width = player_win.getmaxyx()
    for row in range(height):
        for col in range(width):
            try:
                player_win.addstr(
                    row, col, '~∽'[(row+col) % 2],
                    curses.color_pair(1)
                )
            except curses.error:
                pass

    enemy_win = curses.newwin(18, 35, 4, 43)
    enemy_win.bkgd(' ', curses.color_pair(1))
    stdscr.addstr(3, 43, '1 2 3 4 5 6 7 8 9 A B C D E F G H I')
    for row in range(18):
        stdscr.addstr(4 + row, 41, 'abcdefghijklmnopqr'[row])

    height, width = enemy_win.getmaxyx()
    for row in range(height):
        for col in range(width):
            try:
                enemy_win.addstr(
                    row, col, '~∽'[(row+col) % 2],
                    curses.color_pair(1)
                )
            except curses.error:
                pass

    message_win = curses.newwin(3, 80, 23, 0)
    message_win.bkgd(' ', curses.color_pair(2))
    message_win.box()
    message_win.addstr(
        1, 2, 'messages for player here...', curses.color_pair(3)
    )

    stdscr.refresh()
    key_win.refresh()
    player_win.refresh()
    enemy_win.refresh()
    message_win.refresh()

    key_win.getch()

curses.wrapper(run)
