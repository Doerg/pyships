import curses
from .Connection import Connection
from CustomExceptions import ProgramExit
from . import UIData, TitleScreen, BattleScreen


def run():
    """
    wraps the client into a curses environment which does all the basic
    curses initialisations and deinitialisations automatically.
    """
    curses.wrapper(_run_client)


def _run_client(stdscr):
    """
    top level game logic.
    :param stdscr: curses default window, passed by wrapper method
    """
    UIData.init_colors()
    TitleScreen.init()

    try:
        connection, player_name = _establish_connection()
    except ProgramExit:
        return

    TitleScreen.uninit()
    BattleScreen.init(player_name)

    if not connection.has_message():
        BattleScreen.message('Waiting for an opponent to connect...')
    opponent_name = connection.setup_identification(player_name)
    player_starts = True if connection.player_id == 0 else False
    BattleScreen.introduce_opponent(opponent_name)

    try:
        _handle_ship_placements(connection, opponent_name, player_starts)
        shot_coordinates = BattleScreen.let_player_shoot()
    except ProgramExit:
        return
    finally:
        connection.inform_exit()


def _establish_connection():
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


def _handle_ship_placements(connection, opponent_name, player_starts):
    """
    lets player place his ships and waits for the opponent to either place
    his ships or exit.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    :param player_starts: boolean indicating whether player is first to shoot
    """
    ship_placements = BattleScreen.player_ship_placements()
    connection.send_placements(ship_placements)
    BattleScreen.show_battle_keys()

    if not connection.has_message():
        BattleScreen.message(
            'Waiting for %s to finish ship placement...' % opponent_name
        )

    placements_done = connection.wait_for_opponent_placements()
    if placements_done:
        message = '%s has finished ship placement. ' % opponent_name
        if player_starts:
            message += 'Please take your first shot.'
        else:
            message += 'Please wait for the first enemy shot.'
        BattleScreen.message(message)
    else:
        BattleScreen.handle_exit('%s has left the game!' % opponent_name)
        raise ProgramExit