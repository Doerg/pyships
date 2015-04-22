#!/usr/bin/env python3.4

from Message import *
from multiprocessing.connection import Client

conn = Client(('localhost', 12345))
conn.send(PlacementMessage(((1,2),(3,4),(5,6))))
conn.send(ResultMessage(False))
conn.send(ResultMessage(((1,2),(3,4),(5,6))))
conn.send(ExitMessage())
