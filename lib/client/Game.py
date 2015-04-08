import curses
from client import TitleScreen, BattleScreen
from sys import exit


def run():
    """
    wraps the client into a curses environment which does all the basic
    curses initialisations and deinitialisations automatically.
    """
    curses.wrapper(run_client)


def run_client(stdscr):
    """
    client game logic.
    :param stdscr: curses default window, passed by wrapper method
    """
    TitleScreen.init()
    connection, player_name = establish_connection()
    TitleScreen.uninit()

    BattleScreen.init(player_name)


def establish_connection():
    """
    sets up a connection, requiring user input from the title screen.
    can end the program if the user tells it to exit.
    :return: connection object of some sort
    """
    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        connection = True #some_method(player_name, host_ip)
        if not connection:
            if TitleScreen.ask_exit():
                exit()
        else:
            return connection, player_name
