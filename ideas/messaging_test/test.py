#!/usr/bin/env python3.4

from ClientConnection import Connection
from Messages import *

c = Connection()

if c.establish(input('ip: ')):
    c.send_message(PlacementMessage(((1,2),(3,4),(5,6))))

    while True:
        msg = c.get_message()
        if isinstance(msg, ExitMessage):
            print('Exit Message')
            break
        elif isinstance(msg, ResultMessage):
            print('Result Message: ', msg.result)
        elif isinstance(msg, PlacementMessage):
            print('Placement Message: ', msg.coords)

    c.send_message(ExitMessage())
    c.tear_down()
else:
    print('Could not establish connection!')