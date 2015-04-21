#!/usr/bin/env python3.4

from Message import MyMessage
import pickle

msg = MyMessage()
msg.msg = "Duuude!"
with open('data', 'wb') as f:
    pickle.dump(msg, f)
