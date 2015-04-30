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
				_handle_shot_exchange(shooter_id, fleets, connection)

	except (GameOver, OpponentLeft):
		return


def _handle_shot_exchange(shooter_id, fleets, connection):
	receiver_id = _other_player_id(shooter_id)
	receiving_fleet = fleets[receiver_id]

	shot_coords = connection.receive_shot()
	is_hit = receiving_fleet.receive_shot(shot_coords)
	destroyed_ship = receiving_fleet.destroyed_ship #might be None
	game_over = receiving_fleet.destroyed

	connection.inform_shot_result(
		shot_coords, is_hit, game_over, destroyed_ship
	)

	if game_over:
		raise GameOver


def _other_player_id(player_id):
	return abs(player_id - 1)