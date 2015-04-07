#!/usr/bin/env python3.4

import curses

def run(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_BLACK)

    background_win = curses.newwin(29, 83, 0, 0)
    background_win.bkgdset(' ', curses.A_BOLD)
    background_win.box()
    background_win.addstr(4, 18, 'Player', curses.color_pair(12))
    background_win.addstr(4, 59, 'Enemy', curses.color_pair(10))
    background_win.vline(4, 41, curses.ACS_VLINE, 21)

    key_win = curses.newwin(3, 79, 1, 2)
    key_win.bkgd(' ', curses.color_pair(4))
    key_win.box()
    key_win.bkgdset(' ', curses.A_BOLD)
    key_win.addstr(1, 2, 'key legend here...', curses.color_pair(8))

    player_win = curses.newwin(19, 38, 5, 2)
    player_win.bkgd(' ', curses.color_pair(8))
    player_win.box()

    #player_win.bkgdset(' ', curses.A_BOLD)
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

    enemy_win = curses.newwin(19, 38, 5, 43)
    enemy_win.bkgd(' ', curses.color_pair(8))
    enemy_win.box()

    #enemy_win.bkgdset(' ', curses.A_BOLD)
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

    message_win = curses.newwin(3, 79, 25, 2)
    message_win.bkgd(' ', curses.color_pair(4))
    message_win.box()
    message_win.addstr(
        1, 2, 'messages for player here...', curses.A_BOLD
    )

    background_win.refresh()
    key_win.refresh()
    player_win.refresh()
    enemy_win.refresh()
    message_win.refresh()

    key_win.getch()

curses.wrapper(run)
