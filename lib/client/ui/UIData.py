import curses


### KEY CODES ###
key_codes = {
    'up': 65,    #curses returns these codes for arrow keys. like wtf?
    'down': 66,
    'left': 68,
    'right': 67,
    'rotate': ord(' '),
    'place ship': 10,   #enter
    'fire': 10,         #enter
    'exit': ord('q'),
    'yes': ord('y'),
    'no': ord('n'),
    'refresh': ord('r'),
    'hosts': range(ord('0'), ord('9')+1)
}



### TOKEN DATA ###
tokens = {
    'ocean': '~∽',
    'hit': '❃',
    'miss': '◎',
    'ship': {
        'horizontal': {
            'front': '◀',
            'back': '▶'
        },
        'vertical': {
            'front': '▲',
            'back': '▼'
        },
        'center': '▣'
    }
}



### TITLE SCREEN DATA ###
title = {
    'logo': {
        'hpadding': 1,
        'vpadding': 3,
        'relative vertical location': 0.1
    },
    'prompts': {
        'common': {
            'hpadding': 3,
            'vpadding': 1
        },
        'input': {
            'relative vertical location': 0.7,
            'height': 3,
            'input limit': 15,
            'gap height': 6,
            'texts': {
                'name': 'Your name:',
                'ip': 'Server IP:'
            },
        },
        'keypress': {
            'relative vertical location': 0.75,
            'height': 3,
            'texts': {
                'retry': ('Connection could not be established!'
                            ' Try again? (y/n)'),
                'join fail': ('Failed to join your selected host!'
                                ' Press any key to return to host list'),
                'host fail': ('Failed to host a game!'
                                ' Press any key to return to host list'),
                'direct p2p fail': ('Failed to connect to the game host!'
                                " Please press 'q' to exit"),
                'shutdown': "Server has shut down! Please press 'q' to exit"
            }
        },
        'host list': {
            'relative vertical location': 0.5,
            'max hosts': 9,
            'texts': {
                'top1': 'Press numbers 1-9 to join or 0 to host a game.',
                'top2': 'Hosting a game requires at least one free slot.',
                'bottom': "Press 'r' to refresh the host list"
            }
        }
    }
}

_general_prompt = title['prompts']['common']

_input_prompt = title['prompts']['input']
_input_prompt['input offset'] = len(
    max(_input_prompt['texts'].values(), key=lambda s: len(s))
) + 2*_general_prompt['hpadding']
_input_prompt['width'] = _input_prompt['input offset'] + \
                        _input_prompt['input limit'] + \
                        _general_prompt['hpadding']

_keypress_prompt = title['prompts']['keypress']
_keypress_prompt['width'] = len(
    max(_keypress_prompt['texts'].values(), key=lambda s: len(s))
) + 2*_general_prompt['hpadding']

_host_list = title['prompts']['host list']
_host_list['width'] = len(
    max(_host_list['texts'].values(), key=lambda s: len(s))
) + 2*_general_prompt['hpadding']
_host_list['height'] = 2*_general_prompt['vpadding'] + \
                        _host_list['max hosts']+2 + \
                        len(_host_list['texts']) + 2



### BATTLE SCREEN DATA ###
battle = {
    'window margin': 1,
    'map': {
        'logical size': 24,
        'box': {}
    },
    'info bar': {   # common data for both key legend and message bar
        'padding': 4,
        'height': 3,
        'legend keys': {
            'ship placement': (
                ('←↑↓→', 'Move cursor'),
                ('Space', 'Rotate ship'),
                ('Return', 'Place ship'),
                ('q', 'Quit')
            ),
            'battle': (
                ('←↑↓→', 'Move cursor'),
                ('Return', 'Fire shot'),
                ('q', 'Quit')
            )
        }
    },
    'frame': {}
}
_battle_map = battle['map']
_battle_map['height'] = _battle_map['logical size']
_battle_map['width'] = 2*_battle_map['height'] - 1  #to keep visual symmetry
_battle_map['box']['width'] = _battle_map['width'] + 2
_battle_map['box']['height'] = _battle_map['height'] + 2

_info_bar = battle['info bar']
_info_bar['width'] = 2*_battle_map['box']['width'] + \
                    2*battle['window margin'] + 1

_frame = battle['frame']
_frame['width'] = _info_bar['width'] + 2*battle['window margin'] + 2
_frame['height'] = 2*_info_bar['height'] + _battle_map['box']['height'] + \
                  2*battle['window margin'] + 2



### COLORS ###
colors = {}     # to be initialized using init_colors

def init_colors():
    """
    initialises user defined color pairs for curses, using descriptive
    constants. curses color pairs can only be set after curses.initscr() has
    been executed. therefore this method has to be called after the fact.
    """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(14, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(15, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(16, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(17, curses.COLOR_WHITE, curses.COLOR_BLACK)

    colors['clear'] = curses.color_pair(1)
    colors['ocean'] = curses.color_pair(2)
    colors['ship'] = curses.color_pair(3)
    colors['logo box'] = curses.color_pair(4)
    colors['prompt box'] = curses.color_pair(5)
    colors['content frame'] = curses.color_pair(6)
    colors['player name'] = curses.color_pair(7)
    colors['opponent name'] = curses.color_pair(8)
    colors['legend'] = curses.color_pair(9)
    colors['legend entry'] = curses.color_pair(10)
    colors['message'] = curses.color_pair(11)
    colors['battle frame'] = curses.color_pair(12)
    colors['placeable ship'] = curses.color_pair(13)
    colors['blocked ship'] = curses.color_pair(14)
    colors['hit'] = curses.color_pair(15)
    colors['miss'] = curses.color_pair(16)
    colors['host list'] = curses.color_pair(17)