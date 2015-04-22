from multiprocessing.connection import Listener
import socket
from threading import Thread
from queue import Queue


class MessageListener(Thread):
    def __init__(self, msg_queue, conn):
        self._msg_queue = msg_queue
        self._conn = conn
        Thread.__init__(self)

    def run(self):
        for _ in range(4):
            self._msg_queue.put(self._conn.recv())


def establish():
    global msg_queue, msg_listener
    the_socket = Listener(('localhost', 12345))
    conn = the_socket.accept()
    msg_queue = Queue()
    msg_listener = MessageListener(msg_queue, conn)
    msg_listener.start()


def next_message():
    msg = msg_queue.get()
    msg_queue.task_done()
    return msg


def tear_down():
    msg_queue.join()
    msg_listener.join()
