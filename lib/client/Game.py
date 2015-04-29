import curses
from .Connection import Connection
from CustomExceptions import *
from . import UIData, TitleScreen, BattleScreen


def run():
    """
    wraps the client into a curses environment which does all the basic
    curses initialisations and deinitialisations automatically.
    """
    curses.wrapper(_run_game)


def _run_game(stdscr):
    """
    top level game logic.
    :param stdscr: curses default window, passed by wrapper method
    """
    UIData.init_colors()
    TitleScreen.init()

    try:
        connection, player_name = _establish_connection()

        TitleScreen.uninit()
        BattleScreen.init(player_name)

        opponent_name = _handle_identification(connection, player_name)

        player_starts = True if connection.player_id == 0 else False

        _handle_ship_placements(connection, opponent_name, player_starts)

        if player_starts:
            _player_shot(connection, opponent_name)
        while True: #can only exit through exception throw
            _opponent_shot(connection, opponent_name)
            _player_shot(connection, opponent_name)

    except (ConnectionAborted, GameOver):
        return
    except ProgramExit:
        connection.inform_exit()
    except ServerShutdown:
        BattleScreen.handle_exit('Server has shut down!')
    except OpponentLeft:
        BattleScreen.handle_exit('%s has left the game!' % opponent_name)


def _establish_connection():
    """
    sets up a connection, requiring user input from the title screen.
    :return: the connection to the server
    """
    connection = Connection()

    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        if connection.establish(host_ip):
            return connection, player_name
        else:
            if not TitleScreen.ask_connection_retry():
                raise ConnectionAborted


def _handle_identification(connection, player_name):
    """
    tells the server the player's name. the server will then return the name
    of the opponent, which will be introduced on the screen.
    :param connection: the connection to the server
    :param player_name: the name of the player
    :return: the name of the opponent
    """
    if not connection.has_message():
        BattleScreen.message('Waiting for an opponent to connect...')
    opponent_name = connection.setup_identification(player_name)
    BattleScreen.introduce_opponent(opponent_name)
    return opponent_name


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

    connection.acknowledge_opponent_placements()
    message = '%s has finished ship placement. ' % opponent_name
    if player_starts:
        BattleScreen.message(message + 'Please take your first shot.')
    else:
        BattleScreen.message(message + 'Please wait for the first enemy shot.')


def _player_shot(connection, opponent_name):
    """
    lets the player shoot and will display the result of the shot on screen.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    """
    shot_coordinates = BattleScreen.let_player_shoot()
    shot_result = connection.deliver_shot(shot_coordinates)

    if shot_result.ship_destroyed:
        BattleScreen.reveal_ship(shot_result.coordinates)
        if shot_result.game_over:
            BattleScreen.handle_exit('Congratulations! You win!')
            raise GameOver
        else:
            BattleScreen.message(
                "You destroyed a ship of size %d! It's %s's turn now..." %
                (len(shot_result.coordinates), opponent_name)
            )
    else:
        BattleScreen.show_shot(
            shot_coordinates, shot_result.is_hit, opponent=True
        )
        if shot_result.is_hit:
            BattleScreen.message(
                "You scored a hit! It's %s's turn now..." % opponent_name
            )
        else:
            BattleScreen.message(
                "You missed! It's %s's turn now..." % opponent_name
            )


def _opponent_shot(connection, opponent_name):
    """
    display the result of the opponent's shot.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    """
    shot_result = connection.receive_shot()
    BattleScreen.show_shot(shot_result.coordinates, shot_result.is_hit)

    if shot_result.ship_destroyed:
        if shot_result.game_over:
            BattleScreen.handle_exit(
                '%s has destroyed your fleet! You lose!' % opponent_name
            )
            raise GameOver
        else:
            BattleScreen.message(
                '%s has destroyed one of your ships! Take revenge!' %
                opponent_name
            )
    else:
        if shot_result.is_hit:
            BattleScreen.message(
                '%s hit one of your ships! Shoot back!' % opponent_name
            )
        else:
            BattleScreen.message(
                "%s missed! Time to show %s how it's done!" %
                (opponent_name, opponent_name)
            )