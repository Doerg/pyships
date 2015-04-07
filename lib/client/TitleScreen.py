from client import TitleWindows, ColorDefinitions


def init():
    """
    initialises all the panels of the title screen and displays the background.
    """
    global _background, _name_prompt, _ip_prompt, _exit_prompt

    ColorDefinitions.init_colors()

    _background = TitleWindows.Background()
    _name_prompt = TitleWindows.NamePrompt()
    _ip_prompt = TitleWindows.IpPrompt()
    _exit_prompt = TitleWindows.ExitPrompt()

    _background.refresh()


def ask_logon_data():
    """
    prompts the user for logon data.
    :return: user name and host ip as strings
    """
    _exit_prompt.hide()
    _background.refresh()   #to undisplay now hidden exit prompt

    _name_prompt.show()
    _ip_prompt.show()

    return _name_prompt.get_input(), _ip_prompt.get_input()


def ask_exit():
    """
    asks the user if he wants to exit the program.
    :return: True if user wants to exit, False otherwise
    """
    _name_prompt.hide()
    _ip_prompt.hide()
    _background.refresh()     #to undisplay now hidden name/ip prompts

    _exit_prompt.show()

    return _exit_prompt.get_answer()
