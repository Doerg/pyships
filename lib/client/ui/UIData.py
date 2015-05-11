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
        'question': {
            'relative vertical location': 0.75,
            'height': 3,
            'texts': {
                'exit': 'Connection could not be established! Try again? (y/n)'
            }
        },
        'host list': {
            'relative vertical location': 0.5,
            'max hosts': 9,
            'texts': {
                'top': 'Please join a game (1-9) or host a game yourself (0):',
                'bottom': "Press 'R' to refresh the host list"
            }
        }
    }
}

general_prompt = title['prompts']['common']

input_prompt = title['prompts']['input']
input_prompt['input offset'] = len(
    max(input_prompt['texts'].values(), key=lambda s: len(s))
) + 2*general_prompt['hpadding']
input_prompt['width'] = input_prompt['input offset'] + \
                        input_prompt['input limit'] + \
                        general_prompt['hpadding']

question_prompt = title['prompts']['question']
question_prompt['width'] = len(
    max(question_prompt['texts'].values(), key=lambda s: len(s))
) + 2*general_prompt['hpadding']

host_list = title['prompts']['host list']
host_list['width'] = len(
    max(host_list['texts'].values(), key=lambda s: len(s))
) + 2*general_prompt['hpadding']
host_list['height'] = 2 + host_list['max hosts']+2 + 2 +\
                        2*general_prompt['vpadding']



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
                ('Q', 'Quit')
            ),
            'battle': (
                ('←↑↓→', 'Move cursor'),
                ('Return', 'Fire shot'),
                ('Q', 'Quit')
            )
        }
    },
    'frame': {}
}
battle_map = battle['map']
battle_map['height'] = battle_map['logical size']
battle_map['width'] = 2*battle_map['height'] - 1  #to keep visual symmetry
battle_map['box']['width'] = battle_map['width'] + 2
battle_map['box']['height'] = battle_map['height'] + 2

info_bar = battle['info bar']
info_bar['width'] = 2*battle_map['box']['width'] + \
                    2*battle['window margin'] + 1

frame = battle['frame']
frame['width'] = info_bar['width'] + 2*battle['window margin'] + 2
frame['height'] = 2*info_bar['height'] + battle_map['box']['height'] + \
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