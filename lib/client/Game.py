import curses
from .Connection import Connection
from CustomExceptions import ProgramExit
from Messages import *
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

    try:
        BattleScreen.reveal_ship(((4, 5), (4, 6), (4, 7), (4, 8)))   #remove me
        BattleScreen.show_shot((3,4), False, opponent=True)    #remove me
        BattleScreen.show_shot((5,14), False, opponent=True)   #remove me
        BattleScreen.show_shot((6,14), False, opponent=True)   #remove me
        BattleScreen.show_shot((10,17), True, opponent=True)   #remove me
        BattleScreen.show_shot((10,18), True, opponent=True)   #remove me

        ship_placements = BattleScreen.player_ship_placements()
        BattleScreen.show_battle_keys()
        shot_coordinates = BattleScreen.let_player_shoot()

        BattleScreen.show_shot((6,14), False)   #remove me
        BattleScreen.show_shot((10,17), True)   #remove me
        BattleScreen.show_shot((10,18), True)   #remove me

        BattleScreen._message_bar.put_message("That's it so far!!!") #remove me
        BattleScreen._message_bar._win.getch()      #remove me

    except ProgramExit:
        connection.send_message(ExitMessage())
        return


def establish_connection():
    """
    sets up a connection, requiring user input from the title screen.
    :return: connection object of some sort
    """
    connection = Connection()

    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        if not connection.establish(host_ip):
            if TitleScreen.ask_exit():
                raise ProgramExit
        else:
            return connection, player_name
