from .panels import *


def init():
    """
    initializes all the panels of the title screen and displays the background.
    """
    global _background, _name_prompt, _ip_prompt, _exit_prompt

    _background = Background()
    _name_prompt = InputPrompt('name')
    _ip_prompt = InputPrompt('ip', gap=True)
    _exit_prompt = QuestionPrompt('exit')

    _background.update()


def server_logon():
    """
    prompts the user for his name and the ip of the host listing server.
    :return: a tuple containing the player's name and the server ip
    """
    _name_prompt.show()
    _ip_prompt.show()
    return _name_prompt.get_input(), _ip_prompt.get_input()


def ask_connection_retry():
    """
    asks the user if he wants to retry connecting to the server / game host.
    :return: True if the user wants to retry connecting, False otherwise
    """
    _name_prompt.hide()
    _ip_prompt.hide()
    _background.update()     #to undisplay now hidden logon prompt
    _exit_prompt.show()
    return _exit_prompt.get_answer()


def uninit():
    """
    free all title screen resources.
    """
    global _background, _name_prompt, _ip_prompt, _exit_prompt
    _background.clear()
    _background.update()
    _background = _name_prompt = _ip_prompt = _exit_prompt = None