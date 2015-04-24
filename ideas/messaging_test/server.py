#!/usr/bin/env python3.4

from Messages import *
from queue import Queue
from multiprocessing.connection import Client, Listener
from netifaces import ifaddresses


machine_ip = 'localhost' #ifaddresses('eth0')[2][0]['addr']
port = 12345

client_listener = Listener((machine_ip, port))
client_connection = client_listener.accept()

msg_queue = Queue()
msg_listener = MessageListener(msg_queue, client_connection)
msg_listener.start()

client_ip = msg_queue.get().ip  #first msg from client will contain it's IP
msg_sender = Client((client_ip, port))

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

client_listener.close()
msg_listener.join()