from CustomExceptions import *
from .Connection import Connection
from .Fleet import Fleet
import logging
import atexit


def run():
	"""
	server entry method. loops game sessions until the server is shut down.
	one game session consists of the same two players playing one or multiple
	matches.
	"""
	atexit.register(logging.info, 'shutting down')

	while _run_session():
		logging.info('resetting session')


def _run_session():
	"""
    top level game session logic. one game session can consist of multiple
    matches between the same two players. this method only exits through an
    exception, thrown by a subroutine and evaluated by an except clause.
    :return: False if server was closed by keyboard interrupt, True otherwise
	"""
	connection = Connection()

	try:
		connection.establish()
		connection.assign_ids()
		connection.name_exchange()
		while True: #can only exit through exception throw
			_run_battle(connection)

	except OpponentLeft:
		connection.close()
		return True
	except KeyboardInterrupt:
		if connection.established:
			connection.inform_shutdown()
			connection.close()
		return False


def _run_battle(connection):
	"""
	handles a battle between the players. returns normally when both players
	agree to a rematch after the battle. otherwise, an exception will be thrown.
	:param connection: the network connection to both players
	"""
	fleets = [
		Fleet(ship_placements) for ship_placements in
		connection.exchange_placements()  #fleets come ordered by player id
	]
	while True:
		for shooter_id in range(2):
			receiving_fleet = fleets[abs(shooter_id - 1)]
			if _handle_shot(shooter_id, receiving_fleet, connection):
				connection.exchange_rematch_willingness()
				return


def _handle_shot(shooter_id, receiving_fleet, connection):
	"""
	waits for a player to shoot, gathers the shot result and informs both
	players about the result.
	:param shooter_id: the id of the player to shoot
	:param receiving_fleet: the fleet that will receive the shot
	:param connection: the network connection to both players
	:return: True if the shot ended the game, False otherwise
	"""
	shot_coords = connection.receive_shot(shooter_id)
	is_hit = receiving_fleet.receive_shot(shot_coords)
	destroyed_ship = receiving_fleet.destroyed_ship #might be None
	game_over = receiving_fleet.destroyed

	connection.inform_shot_result(
		shot_coords, is_hit, game_over, destroyed_ship
	)

	return game_over