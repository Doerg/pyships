from CustomExceptions import *
from .Connection import Connection
from .Fleet import Fleet
import atexit


def run():
	connection = Connection()
	connection.establish()

	atexit.register(connection.inform_shutdown)

	try:
		connection.setup_identification()
		fleets = [
			Fleet(ship_placements) for ship_placements in
			connection.exchange_placements()
		]
		while True:
			for shooter_id in range(2):
				receiving_fleet = fleets[abs(shooter_id - 1)]
				_handle_shot(shooter_id, receiving_fleet, connection)

	except (GameOver, OpponentLeft):
		return


def _handle_shot(shooter_id, receiving_fleet, connection):
	shot_coords = connection.receive_shot(shooter_id)
	is_hit = receiving_fleet.receive_shot(shot_coords)
	destroyed_ship = receiving_fleet.destroyed_ship #might be None
	game_over = receiving_fleet.destroyed

	connection.inform_shot_result(
		shot_coords, is_hit, game_over, destroyed_ship
	)

	if game_over:
		raise GameOver