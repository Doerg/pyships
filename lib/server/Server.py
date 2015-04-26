from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *
from time import sleep


def run():
    server_port = 12346
    client_port = 12345

    connection_listener = Listener(('', server_port))
    client_connection = connection_listener.accept()

    msg_queue = Queue()
    msg_listener = MessageListener(msg_queue, client_connection)
    msg_listener.start()

    client_ip = connection_listener.last_accepted[0]
    msg_sender = Client((client_ip, client_port))
    connection_listener.close()

    sleep(3)
    print('Player name: %s' % msg_queue.get().player_name)
    msg_sender.send(IDMessage(0, 'XXXTheEnemyXXX'))

    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        return

    print('Player ship placements: %s' % msg.coords)
    sleep(3)
    msg_sender.send(PlacementMessage())


    #some shot exchanges...

    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        return
    print('player shot at coords %s' % msg.coordinates)
    msg_sender.send(ShotResultMessage(False, False, False))
    sleep(3)
    msg_sender.send(ShotResultMessage(False, False, False, coordinates=(4,5)))

    #msg_sender.send(ShutdownMessage())
    #return

    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        return
    print('player shot at coords %s' % msg.coordinates)
    msg_sender.send(ShotResultMessage(True, False, False))
    sleep(3)
    msg_sender.send(ShotResultMessage(True, False, False, coordinates=(12,17)))


    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        return
    print('player shot at coords %s' % msg.coordinates)
    ship_coords = ((5,6),(5,7),(5,8),(5,9))
    msg_sender.send(
        ShotResultMessage(True, True, False, coordinates=ship_coords)
    )
    sleep(3)
    msg_sender.send(
        ShotResultMessage(True, True, False, coordinates=(20,20))
    )


    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        return
    print('player shot at coords %s' % msg.coordinates)
    ship_coords = ((10,10),(11,10),(12,10),(13,10))
    msg_sender.send(
        ShotResultMessage(True, True, False, coordinates=ship_coords)
    )
    sleep(3)
    msg_sender.send(
        ShotResultMessage(True, True, True, coordinates=(22,8))
    )


    msg_sender.send(ExitMessage())