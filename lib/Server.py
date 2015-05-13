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
        # forces all threads to close their connections and terminate
        logging.info('shutting down')



class ConnectionHandler(Thread):
    server_shutdown = False

    def __init__(self, client_connection, client_ip, hosts):
        Thread.__init__(self)
        self._client_connection = client_connection
        self._client_ip = client_ip
        self._game_hosts = hosts
        self._host_list_entry = None  # set once client becomes a game host


    def run(self):
        while True:
            if ConnectionHandler.server_shutdown:
                self._client_connection.send(ShutdownMessage())
                self._client_connection.close()
                break

            if self._client_connection.poll():
                msg = self._client_connection.recv()

                if isinstance(msg, HostsInfoMessage):
                    self._send_host_info()
                elif isinstance(msg, NameMessage):
                    self._handle_host_registering(msg)
                elif isinstance(msg, GameStartMessage):
                    self._handle_game_start()
                    self._client_connection.close()
                    break
                elif isinstance(msg, ExitMessage):
                    self._handle_client_exit()
                    self._client_connection.close()
                    break

        self._log_with_ip('client listener (%s) closing down')


    def _send_host_info(self):
        with Lock():
            self._client_connection.send(HostsInfoMessage(self._game_hosts))
        self._log_with_ip('client (%s) queried the host list')


    def _handle_host_registering(self, msg):
        if not self._host_list_entry and len(self._game_hosts) < 9:
            with Lock():
                self._host_list_entry = {
                    'ip': self._client_ip, 'name': msg.player_name
                }
                self._game_hosts.append(self._host_list_entry)

            hosting_succeeded = True
            self._log_with_ip('client (%s) registered as host')
        else:
            hosting_succeeded = False
            self._log_with_ip('client (%s) was denied registering as host')

        self._client_connection.send(AcknowledgementMessage(hosting_succeeded))


    def _handle_game_start(self):
        if self._host_list_entry:
            self._game_hosts.remove(self._host_list_entry)
            self._log_with_ip('hosting client (%s) started a game')
        else:
            self._log_with_ip('client (%s) joined a game')


    def _handle_client_exit(self):
        if self._host_list_entry:
            self._game_hosts.remove(self._host_list_entry)
            self._log_with_ip('hosting client (%s) exited')
        else:
            self._log_with_ip('client (%s) exited')


    def _log_with_ip(self, msg):
        logging.info(msg % self._client_ip)