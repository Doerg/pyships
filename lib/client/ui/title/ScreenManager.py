from .panels import *
from client.ui import UIData


def init():
    """
    initializes all the panels of the title screen and displays the background.
    """
    global _background, _name_prompt, _ip_prompt, _exit_prompt, _host_list

    _background = Background()
    _name_prompt = InputPrompt('name')
    _ip_prompt = InputPrompt('ip', gap=True)
    _exit_prompt = QuestionPrompt('exit')
    _host_list = HostList()

    _background.update()


def server_logon():
    """
    prompts the user for his name and the ip of the host listing server.
    :return: a tuple containing the player's name and the server ip
    """
    _exit_prompt.hide()
    _background.update()     #to undisplay hidden prompts
    _name_prompt.show()
    _ip_prompt.show()
    return _name_prompt.get_input(), _ip_prompt.get_input()


def select_host(query_hosts):
    _name_prompt.hide()
    _ip_prompt.hide()
    _exit_prompt.hide()
    _background.update()     #to undisplay now hidden logon prompt
    _host_list.show()

    keys = UIData.key_codes

    while True:
        available_hosts = [ #REMOVE ME
            {'ip': '1.1.1.1', 'name': 'host1'},
            {'ip': '192.168.10.59', 'name': '123456789012345'}
        ]
        _host_list.fill_hosts(available_hosts)#query_hosts()
        _host_list.update()

        key = _host_list.select_host()
        if key == UIData.key_codes['refresh']:
            pass
        if key == 0: # player wants to host himself
            return None
        if key <= len(available_hosts):
            return available_hosts[key-1]['ip']


def ask_connection_retry():
    """
    asks the user if he wants to retry connecting to the server / game host.
    :return: True if the user wants to retry connecting, False otherwise
    """
    _name_prompt.hide()
    _ip_prompt.hide()
    _host_list.hide()
    _background.update()     #to undisplay hidden prompts
    _exit_prompt.show()
    return _exit_prompt.get_answer()


def uninit():
    """
    free all title screen resources.
    """
    global _background, _name_prompt, _ip_prompt, _exit_prompt, _host_list
    _background.clear()
    _background.update()
    _background = _name_prompt = _ip_prompt = _exit_prompt, _host_list = None