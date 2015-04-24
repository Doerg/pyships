#!/usr/bin/env python3.4

from multiprocessing.connection import Client, Listener
from queue import Queue
from Messages import *


server_port = 12346
client_port = 12345

connection_listener = Listener(('', server_port))
client_connection = connection_listener.accept()

msg_queue = Queue()
msg_listener = MessageListener(msg_queue, client_connection)
msg_listener.start()

client_ip = connection_listener.last_accepted[0]
msg_sender = Client((client_ip, client_port))

msg_sender.send(PlacementMessage(((1,2),(3,4),(5,6))))
msg_sender.send(ResultMessage(False))
msg_sender.send(ResultMessage(((1,2),(3,4),(5,6))))
msg_sender.send(ExitMessage())

while True:
    msg = msg_queue.get()
    if isinstance(msg, ExitMessage):
        print('Exit Message')
        break
    elif isinstance(msg, ResultMessage):
        print('Result Message: ', msg.result)
    elif isinstance(msg, PlacementMessage):
        print('Placement Message: ', msg.coords)

connection_listener.close()
msg_listener.join()