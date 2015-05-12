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
                logging.info(
                    'client with ip %s logged on' %
                    connection_listener.last_accepted[0]
                )
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
                        'client with ip %s queried the host list' %
                        self._client_ip
                    )

                elif isinstance(msg, NameMessage):
                    if len(self._game_hosts) < 9:
                        with Lock():
                            self._game_hosts.append(
                                {'ip': self._client_ip, 'name': msg.player_name}
                            )
                        self._client_is_host = True
                        log_msg = 'client with ip %s registered as host'
                    else:
                        log_msg = ('client with ip %s was denied'
                                    ' registering as host (slots full)')

                    self._client_connection.send(
                        AcknowledgementMessage(self._client_is_host)
                    )
                    logging.info(log_msg % self._client_ip)

                elif isinstance(msg, AcknowledgementMessage):
                    with Lock():
                        for host in self._game_hosts:
                            if host['ip'] == self._client_ip:
                                self._game_hosts.remove(host)

                    self._client_connection.close()
                    logging.info(
                        'client host with ip %s closed the connection'
                        ' and is starting a game' % self._client_ip
                    )
                    break

                elif isinstance(msg, ExitMessage):
                    if self._client_is_host:
                        with Lock():
                            for host in self._game_hosts:
                                if host['ip'] == self._client_ip:
                                    self._game_hosts.remove(host)
                        log_msg = ('client host with ip %s aborted hosting and'
                                    ' closed the connection')
                    else:
                        log_msg = 'client with ip %s closed the connection'

                    self._client_connection.close()
                    logging.info(log_msg % self._client_ip)
                    break
