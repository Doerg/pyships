from CustomExceptions import *
from .Connection import Connection
from .Fleet import Fleet
import atexit


def run():
	connection = Connection()
	connection.establish()

	atexit.register(connection.inform_shutdown)

	game_info = ({},{})	#one dict for each player

	try:
		_handle_identification(game_info, connection)
		_handle_ship_placement(game_info, connection)
		while True:
			_handle_shot_exchange(game_info, connection)
	except (GameOver, OpponentLeft):
		return


def _handle_identification(game_info, connection):
	player_names = connection.setup_identification()
	game_info[0]['name'] = player_names[0]
	game_info[1]['name'] = player_names[1]


def _handle_ship_placement(game_info, connection):
	ship_placements = connection.exchange_placements()
	game_info[0]['fleet'] = Fleet(ship_placements[0])
	game_info[1]['fleet'] = Fleet(ship_placements[1])


def _handle_shot_exchange(game_info, connection):
	for shooter_id in range(2):
		receiver_id = _other_player_id(shooter_id)
		receiving_fleet = game_info[receiver_id]['fleet']

		shot_coords = connection.receive_shot()

		#can be True (hit), False (no hit) or a list (destroyed ship):
		shot_result = receiving_fleet.receive_shot(shot_coords)

		if isinstance(shot_result, list): #list = full ship coords
			is_hit = True
			ship_destroyed = True
			coords = shot_result #coords is a list holding all ship coords here
			game_over = receiving_fleet.is_destroyed()
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