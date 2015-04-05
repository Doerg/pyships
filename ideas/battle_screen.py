#!/usr/bin/env python3.4

import curses

def run(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    key_win = curses.newwin(3, 80, 0, 0)
    key_win.bkgd(' ', curses.color_pair(4))
    key_win.box()
    key_win.addstr(1, 2, 'key legend here...', curses.color_pair(3))

    player_win = curses.newwin(19, 38, 3, 0)
    player_win.box()

    height, width = player_win.getmaxyx()
    for row in range(height-2):
        for col in range(width-2):
            try:
                player_win.addstr(
                    row+1, col+1, '~∽'[(row+col) % 2],
                    curses.color_pair(1)
                )
            except curses.error:
                pass

    enemy_win = curses.newwin(19, 38, 3, 42)
    enemy_win.box()

    height, width = enemy_win.getmaxyx()
    for row in range(height-2):
        for col in range(width-2):
            try:
                enemy_win.addstr(
                    row+1, col+1, '~∽'[(row+col) % 2],
                    curses.color_pair(1)
                )
            except curses.error:
                pass

    message_win = curses.newwin(3, 80, 22, 0)
    message_win.bkgd(' ', curses.color_pair(4))
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
