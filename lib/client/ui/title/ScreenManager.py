from .panels import *
from client.ui import UIData


_panels = {}

def init():
    """
    initializes all the panels of the title screen and displays the background.
    """
    _panels["background"] = Background()
    _panels["name prompt"] = InputPrompt('name')
    _panels["ip prompt"] = InputPrompt('ip', gap=True)
    _panels["retry prompt"] = KeypressPrompt('retry')
    _panels["host list"] = HostList()
    _panels['shutdown info'] = KeypressPrompt('shutdown')

    _panels["background"].update()


def server_logon():
    """
    prompts the user for his name and the ip of the host listing server.
    :return: a tuple containing the player's name and the server ip
    """
    _show_only("name prompt", "ip prompt")
    return _panels["name prompt"].get_input(), _panels["ip prompt"].get_input()


def select_host(query_hosts):
    """
    lets the user select a host from the host list or choose to host a game
    himself.
    :param query_hosts: callable to obtain the most recent host list
    :return: the ip of the selected host, or None if the player wants to host
    """
    _show_only("host list")

    keys = UIData.key_codes

    while True:
        available_hosts = [ #query_hosts()
            {'ip': '1.1.1.1', 'name': 'host1'},
            {'ip': '192.168.10.59', 'name': '123456789012345'}
        ]
        _panels["host list"].fill_hosts(available_hosts)
        _panels["host list"].update()

        key = _panels["host list"].select_host()
        if key == UIData.key_codes['refresh']:
            pass
        if key == 0: # player wants to host a game
            return None
        if key <= len(available_hosts):
            return available_hosts[key-1]['ip']


def ask_connection_retry():
    """
    asks the user if he wants to retry connecting to the server / game host.
    :return: True if the user wants to retry connecting, False otherwise
    """
    _show_only("retry prompt")

    while True:
        answer = _panels["retry prompt"].get_key()
        if answer == UIData.key_codes['yes']:
            return True
        elif answer == UIData.key_codes['no']:
            return False


def shutdown_info():
    """
    informs the user that the server has shut down. waits for an acknowledging
    keypress.
    """
    _show_only('shutdown info')
    while shutdown_info.get_key() != UIData.key_codes['exit']:
        pass


def _show_only(*panels_to_show):
    """
    shows the given panels, hides all others.
    :param panels_to_show: the panels to show
    """
    for name, panel in _panels.items():
        if not name in panels_to_show and not name == 'background':
            panel.hide()
    _panels["background"].update() # to undisplay now hidden panels
    for name in panels_to_show:
        _panels[name].show()


def uninit():
    """
    free all title screen resources.
    """
    global _panels
    _panels["background"].clear()
    _panels["background"].update()
    _panels = None