#!/usr/bin/env python3.4

from Message import MyMessage
import pickle

with open('data', 'rb') as f:
    msg = pickle.load(f)

print(isinstance(msg, MyMessage))
print(msg.msg)
