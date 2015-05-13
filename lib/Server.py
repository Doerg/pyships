from multiprocessing.connection import Listener
from threading import Thread, Lock
from Messages import *
import logging


_listener_port = 12346

def run():
    """
    entry point for server. listens for incoming client connections and starts
    a ConnectionHandler-thread for each of these connections.
    """
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
    """
    handles all communication with one connected client. each handler reads and
    manipulates a host list that is shared among all connection handlers.
    """
    server_shutdown = False

    def __init__(self, client_connection, client_ip, hosts):
        """
        sets up a handler for a client connection.
        :param client_connection: a connection to a client
        :param client_ip: the ip of the client this handler is responsible for
        :param hosts: a list of all current game hosts. this is shared among
        and manipulated by all connection handler threads
        """
        Thread.__init__(self)
        self._client_connection = client_connection
        self._client_ip = client_ip
        self._game_hosts = hosts
        self._host_list_entry = None  # set once client becomes a game host


    def run(self):
        """
        starts this connection handler. loops until server shutdown and handles
        all incoming client messages.
        """
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
        """
        sends a list containing all current game hosts to the client.
        """
        with Lock():
            self._client_connection.send(HostsInfoMessage(self._game_hosts))
        self._log_with_ip('client (%s) queried the host list')


    def _handle_host_registering(self, msg):
        """
        handles a game hosting request by a client. this request is only
        accepted if the host list is not full and there is no host using the
        same ip as the requesting client.
        :param msg: the hosting request message, containing the client's name
        """
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
        """
        handles a message informing about the game start of a client.
        """
        if self._host_list_entry:
            self._game_hosts.remove(self._host_list_entry)
            self._log_with_ip('hosting client (%s) started a game')
        else:
            self._log_with_ip('client (%s) joined a game')


    def _handle_client_exit(self):
        """
        handles a message informing about the termination of a client.
        """
        if self._host_list_entry:
            self._game_hosts.remove(self._host_list_entry)
            self._log_with_ip('hosting client (%s) exited')
        else:
            self._log_with_ip('client (%s) exited')


    def _log_with_ip(self, log_msg):
        """
        inserts this client's ip into the given format string and logs the
        resulting message as an info log.
        :param log_msg: the message string to be formatted and logged
        """
        logging.info(log_msg % self._client_ip)