from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *


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

    while True:
        msg = msg_queue.get()
        if isinstance(msg, ExitMessage):
            break