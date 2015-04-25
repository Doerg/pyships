import curses
from .Connection import Connection
from CustomExceptions import ProgramExit
from . import UIData, TitleScreen, BattleScreen


def run():
    """
    wraps the client into a curses environment which does all the basic
    curses initialisations and deinitialisations automatically.
    """
    curses.wrapper(run_client)


def run_client(stdscr):
    """
    top level game logic.
    :param stdscr: curses default window, passed by wrapper method
    """
    UIData.init_colors()
    TitleScreen.init()

    try:
        connection, player_name = establish_connection()
    except ProgramExit:
        return

    TitleScreen.uninit()
    BattleScreen.init(player_name)

    if not connection.has_message():
        BattleScreen.message('Waiting for an opponent to connect...')
    opponent_name = connection.setup_identification(player_name)
    BattleScreen.introduce_opponent(opponent_name)

    try:
        ship_placements = BattleScreen.player_ship_placements()
        BattleScreen.show_battle_keys()
        shot_coordinates = BattleScreen.let_player_shoot()
    except ProgramExit:
        return
    finally:
        connection.inform_exit()


def establish_connection():
    """
    sets up a connection, requiring user input from the title screen.
    :return: connection object
    """
    connection = Connection()

    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        if connection.establish(host_ip):
            return connection, player_name
        else:
            if not TitleScreen.ask_connection_retry():
                raise ProgramExit