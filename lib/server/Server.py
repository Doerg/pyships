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
    msg_sender.send(IDMessage(0, 'MyEnemyXXX'))

    print('Player ship placements: %s' % msg_queue.get().coords)
    sleep(3)
    msg_sender.send(PlacementMessage())
    #msg_sender.send(ExitMessage(1))

    while True:
        msg = msg_queue.get()
        if isinstance(msg, ExitMessage):
            break