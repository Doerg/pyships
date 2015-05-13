from multiprocessing.connection import Listener
from threading import Thread, Lock
from Messages import *
import logging


_listener_port = 12346

def run():
    hosts = []
    logging.info('Listening for connections...')

    try:
        while True:
            with Listener(('', _listener_port)) as connection_listener:
                client_connection = connection_listener.accept()
                client_ip = connection_listener.last_accepted[0]
                logging.info('client (%s) logged on' % client_ip)
                ConnectionHandler(client_connection, client_ip, hosts).start()

    except KeyboardInterrupt:
        ConnectionHandler.server_shutdown = True
        logging.info('shutting down')
        # forces all threads to close their connections and terminate



class ConnectionHandler(Thread):
    server_shutdown = False

    def __init__(self, client_connection, client_ip, hosts):
        Thread.__init__(self)
        self._client_connection = client_connection
        self._client_ip = client_ip
        self._game_hosts = hosts
        self._client_is_host = False


    def run(self):
        while True:
            if ConnectionHandler.server_shutdown:
                self._client_connection.send(ShutdownMessage())
                self._client_connection.close()
                break

            if self._client_connection.poll():
                msg = self._client_connection.recv()

                if isinstance(msg, HostsInfoMessage):
                    with Lock():
                        self._client_connection.send(
                            HostsInfoMessage(self._game_hosts)
                        )
                    logging.info(
                        'client (%s) queried the host list' %
                        self._client_ip
                    )

                elif isinstance(msg, NameMessage):
                    if (not [host for host in self._game_hosts
                        if host['ip'] == self._client_ip] and
                        len(self._game_hosts) < 9):

                        with Lock():
                            self._game_hosts.append(
                                {'ip': self._client_ip, 'name': msg.player_name}
                            )
                        self._client_is_host = True
                        log_msg = 'client (%s) registered as host'
                    else:
                        log_msg = 'client (%s) was denied registering as host'

                    self._client_connection.send(
                        AcknowledgementMessage(self._client_is_host)
                    )
                    logging.info(log_msg % self._client_ip)

                elif isinstance(msg, GameStartMessage):
                    with Lock():
                        for host in self._game_hosts:
                            if host['ip'] == self._client_ip:
                                self._game_hosts.remove(host)

                    self._client_connection.close()
                    if msg.as_host:
                        log_msg = 'hosting client (%s) started a game'
                    else:
                        log_msg = 'client (%s) joined a game'
                    logging.info(log_msg % self._client_ip)
                    break

                elif isinstance(msg, ExitMessage):
                    if self._client_is_host:
                        with Lock():
                            for host in self._game_hosts:
                                if host['ip'] == self._client_ip:
                                    self._game_hosts.remove(host)
                        log_msg = 'hosting client (%s) exited'
                    else:
                        log_msg = 'client (%s) exited'

                    self._client_connection.close()
                    logging.info(log_msg % self._client_ip)
                    break

        logging.info(
            'client listener (%s) closed down' % self._client_ip
        )