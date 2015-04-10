import curses
from client import TitleScreen, BattleScreen
from CustomExceptions import ProgramExit


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
    try:
        TitleScreen.init()
        connection, player_name = establish_connection()
        TitleScreen.uninit()

        BattleScreen.init(player_name)
        ship_placements = BattleScreen.player_ship_placements()
        BattleScreen._key_legend.set_battle_keys()  #remove me
        BattleScreen._key_legend.update()           #remove me
        BattleScreen._message_bar.put_message("That's it so far!!!") #remove me
        BattleScreen._message_bar._win.getch()      #remove me
    except ProgramExit:
        return


def establish_connection():
    """
    sets up a connection, requiring user input from the title screen.
    :return: connection object of some sort
    """
    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        connection = True #some_method(player_name, host_ip)
        if not connection:
            if TitleScreen.ask_exit():
                raise ProgramExit
        else:
            return connection, player_name
