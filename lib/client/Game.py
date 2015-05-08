from .Connection import Connection
from . import UIData, TitleScreen, BattleScreen
from CustomExceptions import *
import curses
import atexit


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

    connection = Connection()

    try:
        player_name = _establish_connection(connection)

        atexit.register(connection.close)

        TitleScreen.uninit()
        BattleScreen.init(player_name)
        BattleScreen.message('Waiting for an opponent to connect...')

        player_starts = True if connection.obtain_player_id() == 0 else False
        opponent_name = connection.exchange_names(player_name)

        BattleScreen.show_ship_placement_keys()
        BattleScreen.introduce_opponent(opponent_name)

        while True:  #runs until Exception arrives
            _run_battle(connection, opponent_name, player_starts)

    except ConnectionAborted:   #player left the title screen
        return
    except ProgramExit:         #only raised after connection established
        connection.inform_exit()
    except KeyboardInterrupt:   #can happen anytime
        if connection.established: connection.inform_exit()
    except ServerShutdown:      #server got killed
        BattleScreen.handle_exit('Server has shut down!')
    except OpponentLeft:        #remote player quit
        BattleScreen.handle_exit('%s has left the game!' % opponent_name)


def _establish_connection(connection):
    """
    establishes a connection to the server, requiring user input from the
    title screen.
    :param connection: the connection to the server, not established yet
    :return: the name of the player
    """
    while True:
        player_name, host_ip = TitleScreen.ask_logon_data()
        if connection.establish(host_ip):
            return player_name
        else:
            if not TitleScreen.ask_connection_retry():
                raise ConnectionAborted


def _run_battle(connection, opponent_name, player_starts):
    """
    runs one battle between two players. includes initial ship placements.
    only returns once an exception is thrown.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    :param player_starts: boolean indicating whether player is first to shoot
    """
    _handle_ship_placements(connection, opponent_name, player_starts)

    try:
        if player_starts:
            _player_shot(connection, opponent_name)
        while True: #can only exit through exception throw
            _opponent_shot(connection, opponent_name)
            _player_shot(connection, opponent_name)
    except PlayAgain:
        BattleScreen.reset_battle()
        return


def _handle_ship_placements(connection, opponent_name, player_starts):
    """
    lets player place his ships and waits for the opponent to either place
    his ships or exit.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    :param player_starts: boolean indicating whether player is first to shoot
    """
    ships = (5, 4, 4, 3, 3, 3, 2, 2, 2, 2)
    ship_placements = BattleScreen.player_ship_placements(ships)
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
    shot_coords = BattleScreen.let_player_shoot()
    shot_result = connection.deliver_shot(shot_coords)

    if shot_result.destroyed_ship:
        BattleScreen.reveal_ship(shot_result.destroyed_ship, True)
        if shot_result.game_over:
            _check_for_rematch(connection, opponent_name, True)
            raise PlayAgain
        else:
            BattleScreen.message(
                "You destroyed a ship of size %d! It's %s's turn now..." %
                (len(shot_result.destroyed_ship), opponent_name)
            )
    else:
        BattleScreen.show_shot(
            shot_coords, shot_result.is_hit, opponent=True
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
    displays the result of the opponent's shot.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    """
    shot_result = connection.receive_shot()
    BattleScreen.show_shot(shot_result.coords, shot_result.is_hit)

    if shot_result.destroyed_ship:
        if shot_result.game_over:
            BattleScreen.reveal_intact_ships(connection.enemy_intact_ships())
            _check_for_rematch(connection, opponent_name, False)
            raise PlayAgain
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


def _check_for_rematch(connection, opponent_name, player_won):
    """
    asks the player whether he wants to play another game. if this is the case
    and the opponent also agrees to a rematch, this method simply returns. for
    other cases, an exception will be thrown.
    :param connection: the connection to the server
    :param opponent_name: the name of the opponent
    :param player_won: True if the player won the last battle, False otherwise
    """
    if player_won:
        message = 'Congratulations! You win!'
    else:
        message = '%s has destroyed your fleet! You lose!' % opponent_name

    if BattleScreen.ask_for_another_battle(message):
        connection.inform_rematch_willingness()
        if not connection.has_message():
            BattleScreen.message(
                'Waiting for the decision of %s to play again...' %
                opponent_name
            )
        connection.acknowledge_rematch_willingness()
        BattleScreen.message(
            "%s agreed to another battle! Please place your ships." %
            opponent_name
        )
    else:
        raise ProgramExit
