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


	#ugly ass code here. needs redesign
def _handle_shot_exchange(shooter_id, fleets, connection):
	receiver_id = _other_player_id(shooter_id)
	shot_coords = connection.receive_shot()
	shot_result = fleets[receiver_id].receive_shot(shot_coords)
	#shot_result can be True (hit), False (no hit) or list (destroyed ship)

	if isinstance(shot_result, list): #list = full ship coords
		is_hit = True
		ship_destroyed = True
		coords = shot_result #coords is a list holding all ship coords here
		game_over = fleets[receiver_id].is_destroyed()
	else:
		is_hit = shot_result
		ship_destroyed = False
		coords = shot_coords
		game_over = False

	connection.inform_shot_result(
		receiver_id, is_hit, ship_destroyed, game_over, shot_coords
	)
	connection.inform_shot_result(
		shooter_id, is_hit, ship_destroyed, game_over, coords
	)

	if game_over:
		raise GameOver


def _other_player_id(player_id):
	return abs(player_id - 1)