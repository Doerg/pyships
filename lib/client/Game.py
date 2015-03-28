import curses
from client import TitleScreen
from client import BattleScreen
from sys import exit


def run():
    curses.wrapper(run_client)


def run_client(stdscr):
    TitleScreen.init()
    connection = establish_connection()


def establish_connection():
    while True:
        player_name, host_ip = TitleScreen.logon_prompt()
        connection = False #some_method(player_name, host_ip)
        if not connection:
            if TitleScreen.exit_prompt():
                exit()
        else:
            return connection