from .panels import *


def init():
    """
    initializes all the panels of the title screen and displays the background.
    """
    global _background, _name_prompt, _ip_prompt, _host_prompt, _exit_prompt

    _background = Background()
    _name_prompt = InputPrompt('name')
    _ip_prompt = InputPrompt('ip')
    _host_prompt = QuestionPrompt('host')
    _exit_prompt = QuestionPrompt('exit')

    _background.update()


def ask_name():
    """
    prompts the user for his name.
    :return: the user name
    """
    _name_prompt.show()
    return _name_prompt.get_input()


def ask_if_host():
    """
    asks the user if he wants to host a game or connect to a hosted game.
    :return: True if the user wants to host a game, False otherwise
    """
    _name_prompt.hide()
    _background.update()     #to undisplay now hidden name prompt
    _host_prompt.show()
    return _host_prompt.get_answer()


def ask_host_ip():
    """
    prompts the user for the host ip.
    :return: the host ip
    """
    _host_prompt.hide()
    _exit_prompt.hide()
    _background.update()     #to undisplay now hidden host/exit prompt
    _ip_prompt.show()
    return _ip_prompt.get_input()


def ask_connection_retry():
    """
    asks the user if he wants to retry connecting to the server.
    :return: True if the user wants to retry, False otherwise
    """
    _ip_prompt.hide()
    _background.update()     #to undisplay now hidden ip prompt
    _exit_prompt.show()
    return _exit_prompt.get_answer()


def uninit():
    """
    free all title screen resources.
    """
    global _background, _name_prompt, _ip_prompt, _host_prompt, _exit_prompt
    _background.clear()
    _background.update()
    _background = _name_prompt = _ip_prompt = _host_prompt = _exit_prompt = None