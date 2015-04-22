#!/usr/bin/env python3.4

import receiver
from Message import *

receiver.establish()

for _ in range(4):
    msg = receiver.next_message()
    if isinstance(msg, ExitMessage):
        print('Exit Message')
    elif isinstance(msg, ResultMessage):
        print('Result Message: ', msg.result)
    elif isinstance(msg, PlacementMessage):
        print('Placement Message: ', msg.coords)

receiver.tear_down()
