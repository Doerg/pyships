import curses
from client import ColorDefinitions as Colors


### window layout data ###

# margin between windows
margin = 1

# battlefield pair
battle_height = 30
battle_width = 2*battle_height - 1
battle_box_height = battle_height + 2
battle_box_width = battle_width + 2

# top/bottom info bars
ship_placement_keys = (
    ('←↑↓→', 'Move cursor'),
    ('Space', 'Rotate ship'),
    ('Return', 'Place ship'),
    ('Q', 'Exit')
)
battle_keys = (
    ('←↑↓→', 'Move cursor'),
    ('Return', 'Fire shot'),
    ('Q', 'Exit')
)
legend_width = message_width = 2*battle_box_width + 2*margin + 1
legend_height = 3
message_height = 3
info_padding = 5

# main content frame
frame_width = legend_width + 2*margin + 2
frame_height = legend_height + battle_box_height + message_height + 2*margin + 2



### classes ###

class Window(object):
    """
    base class for all window objects.
    """
    def __init__(self, height, width, y, x):
        """
        initialiser for all windows. the y and x values are interpreted as
        offsets from the upper left corner of the central frame window.
        """
        frame_y = curses.LINES//2 - frame_height//2
        frame_x = curses.COLS//2 - frame_width//2
        self._win = curses.newwin(height, width, frame_y + y, frame_x + x)
        self._win.box() #all windows are boxed on this screen


    def refresh(self):
        """
        redraw the window.
        """
        self._win.refresh()
        self._win.getch()



class ContentFrame(Window):
    def __init__(self, player_name):
        super().__init__(frame_height, frame_width, 0, 0)

        self._win.bkgd(' ', Colors.CONTENT_FRAME | curses.A_BOLD)
        self._win.vline(
            legend_height + 1, frame_width//2,
            curses.ACS_VLINE, battle_box_height + 2*margin
        )

        self._win.addstr(
            legend_height + margin,
            margin + battle_box_width//2 - len(player_name)//2,
            player_name, Colors.PLAYER_NAME
        )
        self._win.addstr(
            legend_height + margin,
            1 + 3*margin + battle_box_width +
            battle_box_width//2 - len('Opponent')//2,
            'Opponent', Colors.OPPONENT_NAME
        )



class KeyLegend(Window):
    def __init__(self):
        super().__init__(legend_height, legend_width, 1, 1 + margin)

        self._win.bkgd(' ', Colors.LEGEND)
        self._text_line = legend_height//2

        self.set_ship_placement_keys()


    def set_ship_placement_keys(self):
        self._set_keys(ship_placement_keys)


    def set_battle_keys(self):
        self._set_keys(battle_keys)


    def _set_keys(self, keys):
        self._clear()
        self._win.move(self._text_line, 1)
        for key, description in keys:
            self._add_key(key, description)


    def _clear(self):
        self._win.addstr(
            self._text_line, info_padding, ' ' * (legend_width-info_padding-1)
        )


    def _add_key(self, key, description):
        self._win.addstr(
            ' ' * info_padding + key + ': ', curses.A_BOLD | Colors.LEGEND
        )
        self._win.addstr(
            '   %s   ' % description, curses.A_BOLD | Colors.LEGEND_ENTRY
        )



class BattleGround(Window):
    def __init__(self, opponent=False):
        if opponent:
            offset_x = battle_box_width + 3*margin + 2
        else:
            offset_x = margin + 1

        super().__init__(
            battle_box_height, battle_box_width,
            legend_height + margin + 1, offset_x
        )

        self._win.bkgd(' ', Colors.BATTLE_FRAME)



class MessageBar(Window):
    def __init__(self):
        super().__init__(
            message_height, message_width,
            legend_height + battle_box_height + 2*margin + 1,
            1 + margin
        )

        self._win.bkgd(' ', Colors.MESSAGE)