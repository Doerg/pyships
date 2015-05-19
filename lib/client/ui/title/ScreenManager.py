from .panels import *
from client.ui import UIData


_panels = {}

def init():
    """
    initializes all the panels of the title screen and displays the background.
    """
    _panels['background'] = Background()
    _panels['name prompt'] = InputPrompt('name')
    _panels['ip prompt'] = InputPrompt('ip', gap=True)
    _panels['host list'] = HostList()
    _panels['retry prompt'] = KeypressPrompt('retry')
    _panels['wait prompt'] = KeypressPrompt('wait')
    _panels['joining failure'] = KeypressPrompt('join fail')
    _panels['hosting failure'] = KeypressPrompt('host fail')
    _panels['direct p2p failure'] = KeypressPrompt('direct p2p fail')
    _panels['shutdown info'] = KeypressPrompt('shutdown')

    _panels['background'].update()


def server_logon():
    """
    prompts the user for his name and the ip of the host listing server.
    :return: a tuple containing the player's name and the server ip
    """
    _show_only("name prompt", "ip prompt")
    return _panels['name prompt'].get_input(), _panels['ip prompt'].get_input()


def select_host(query_hosts):
    """
    lets the user select a host from the host list or choose to host a game
    himself.
    :param query_hosts: callable to obtain the most recent host list
    :return: the ip of the selected host, or None if the player wants to host
    """
    _show_only('host list')

    keys = UIData.key_codes
    max_hosts = UIData.title['prompts']['host list']['max hosts']

    while True:
        available_hosts = query_hosts()

        _panels['host list'].fill_hosts(available_hosts)
        _panels['host list'].update()

        key = _panels['host list'].select_host()
        if key == UIData.key_codes['refresh']:
            pass
        if key == 0: # player wants to host a game
            if len(available_hosts) < max_hosts:
                return None
        if key <= len(available_hosts):
            return available_hosts[key-1]['ip']


def ask_server_connection_retry():
    """
    asks the user if he wants to retry connecting to the server.
    :return: True if the user wants to retry connecting, False otherwise
    """
    _show_only('retry prompt')

    while True:
        answer = _panels['retry prompt'].get_key()
        if answer == UIData.key_codes['yes']:
            return True
        elif answer == UIData.key_codes['no']:
            return False


def wait_message():
    """
    displays a wait message while listening for an incoming client connection
    as a game host.
    """
    _show_only('wait prompt')


def inform_game_launch_failure(as_host):
    """
    informs the user that he could not join or host a game. returns after any
    keypress by the user.
    :param as_host: True if game hosting failed, False if joining a game failed
    """
    panel_key = 'hosting failure' if as_host else 'joining failure'
    _show_only(panel_key)
    _panels[panel_key].get_key()


def inform_direct_p2p_connection_failure():
    """
    informs the user that he could not join a game host via direct p2p. waits
    for an acknowledging keypress.
    """
    _show_only('direct p2p failure')
    while _panels['direct p2p failure'].get_key() != UIData.key_codes['exit']:
        pass


def shutdown_info():
    """
    informs the user that the server has shut down. waits for an acknowledging
    keypress.
    """
    _show_only('shutdown info')
    while _panels['shutdown info'].get_key() != UIData.key_codes['exit']:
        pass


def _show_only(*panels_to_show):
    """
    shows the given panels, hides all others.
    :param panels_to_show: the panels to show
    """
    for name, panel in _panels.items():
        if not name in panels_to_show and not name == 'background':
            panel.hide()
    _panels['background'].update() # to undisplay now hidden panels
    for name in panels_to_show:
        _panels[name].show()


def uninit():
    """
    free all title screen resources.
    """
    global _panels
    _panels['background'].clear()
    _panels['background'].update()
    _panels = None