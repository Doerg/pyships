from CustomExceptions import *
from .Connection import Connection
from .Fleet import Fleet
import atexit


def run():
	"""
    top level server logic.
	"""
	connection = Connection()
	connection.establish()

	atexit.register(connection.close)

	try:
		connection.setup_identification()
		while True: #can only exit through exception throw
			_run_battle(connection)
	except OpponentLeft:
		return
	except KeyboardInterrupt:
		connection.inform_shutdown()


def _run_battle(connection):
	"""
	handles a battle between the players. returns normally when both players
	agree to a rematch after the battle. otherwise, an exception will be thrown.
	:param connection: the network connection to both players
	"""
	fleets = [
		Fleet(ship_placements) for ship_placements in
		connection.exchange_placements()
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