import curses
from client import ColorDefinitions as Colors


### UI data ###

# margin between windows
margin = 1

# battlefield pair
logical_map_size = 24
map_height = logical_map_size
map_width = 2*map_height - 1  #almost twice as big to keep symmetry
map_box_height = map_height + 2
map_box_width = map_width + 2

# top/bottom info bars
legend_width = message_width = 2*map_box_width + 2*margin + 1
legend_height = 3
message_height = 3
info_padding = 4

# main content frame
frame_width = legend_width + 2*margin + 2
frame_height = legend_height + map_box_height + message_height + 2*margin + 2



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
        self._win.box() #all windows on this screen are boxed


    def update(self):
        """
        redraw the window.
        """
        self._win.refresh()


    def get_key(self):
        return self._win.getch()



class ContentFrame(Window):
    """
    the outermost frame of the battle screen. this frame is centralized and
    contains all sub-windows.
    """
    def __init__(self, player_name):
        """
        draws the frame and writes player names.
        :param player_name: the name of the player
        """
        super().__init__(frame_height, frame_width, 0, 0)

        curses.noecho()
        curses.curs_set(False)

        self._win.bkgd(' ', Colors.CONTENT_FRAME | curses.A_BOLD)
        self._win.vline(
            legend_height + 1, frame_width//2,
            curses.ACS_VLINE, map_box_height + 2*margin
        )

        self._win.addstr(
            legend_height + margin,
            margin + map_box_width//2 - len(player_name)//2,
            player_name, Colors.PLAYER_NAME
        )
        self._win.addstr(
            legend_height + margin,
            1 + 3*margin + map_box_width +
            map_box_width//2 - len('Opponent')//2,
            'Opponent', Colors.OPPONENT_NAME
        )



class KeyLegend(Window):
    """
    info bar which contains the currently usable keys, plus their descriptions.
    """
    ship_placement_keys = (
        ('←↑↓→', 'Move cursor'),
        ('Space', 'Rotate ship'),
        ('Return', 'Place ship'),
        ('Q', 'Quit')
    )
    battle_keys = (
        ('←↑↓→', 'Move cursor'),
        ('Return', 'Fire shot'),
        ('Q', 'Quit')
    )

    def __init__(self):
        super().__init__(legend_height, legend_width, 1, 1 + margin)

        self._text_line = legend_height//2

        self._win.bkgd(' ', Colors.LEGEND)
        self._win.bkgdset(' ', curses.A_BOLD)

        self.set_ship_placement_keys()


    def set_ship_placement_keys(self):
        """
        set key descriptions for initial ship placement.
        """
        self._set_keys(self.ship_placement_keys)


    def set_battle_keys(self):
        """
        set key descriptions for battle mode.
        """
        self._set_keys(self.battle_keys)


    def _set_keys(self, keys):
        self._clear_legend()
        self._win.move(self._text_line, 1)

        for key, description in keys:
            self._add_key(key, description)


    def _clear_legend(self):
        self._win.addstr(
            self._text_line, info_padding, ' ' * (legend_width-info_padding-1),
            Colors.LEGEND
        )


    def _add_key(self, key, description):
        self._win.addstr(' ' * info_padding + key + ': ', Colors.LEGEND)
        self._win.addstr('  %s  ' % description, Colors.LEGEND_ENTRY)



class BattleGround(Window):
    """
    square window which displays the battleground of the player or opponent.
    the battle screen contains two of these.
    """
    ship_front_hor = '◀'
    ship_back_hor = '▶'
    ship_front_vert = '▲'
    ship_back_vert = '▼'
    ship_center = '▣'

    def __init__(self, opponent=False):
        """
        draws one of the two battlegrounds of the screen.
        :param opponent: draws the battleground on the right side, if set to
        true. default is left side (false).
        """
        if opponent:
            offset_x = map_box_width + 3*margin + 2
        else:
            offset_x = margin + 1

        super().__init__(
            map_box_height, map_box_width, legend_height + margin + 1, offset_x
        )

        self._ships = []

        self._win.bkgd(' ', Colors.BATTLE_FRAME)
        self._win.bkgdset(' ', Colors.OCEAN)
        self.draw_map()


    def add_ship(self, ship):
        """
        add a ship in order for it to be displayed on this battleground.
        :param ship: the ship to be added
        """
        self._ships.append(ship)


    def draw_map(self, new_ship=None):
        """
        draws the battleground with all ships on it.
        :param new_ship: an extra ship to display for this one drawing
        """
        for row in range(1, map_height+1):
            for col in range(1, map_width+1):
                self._win.addstr(row, col, '~∽'[(row+col) % 2])
        for ship in self._ships:
            self._draw_ship(str(ship), Colors.SHIP)
        if new_ship:
            self._draw_ship(str(new_ship), Colors.NEW_SHIP)


    def _draw_ship(self, ship_string, color):
        if ship.alignment == 'hor':
            front_y, front_x = ship.coords[0]
            self._win.addstr(
                front_y+1, self._scale(front_x), ship_string, color
            )
        else:
            for i in range(ship.size):
                y, x = ship.coords[i]
                self._win.addstr(y+1, self._scale(x), ship_string[i], color)


    def _scale(self, x):
        return x*2 + 1



class MessageBar(Window):
    """
    info bar used for displaying ingame messages to the player. these messages
    include instructions, enemy moves, current state of the game, etc.
    """
    def __init__(self):
        super().__init__(
            message_height, message_width,
            legend_height + map_box_height + 2*margin + 1,
            1 + margin
        )

        self._text_line = legend_height//2

        self._win.bkgd(' ', Colors.MESSAGE)
        self._win.bkgdset(' ', curses.A_BOLD | Colors.MESSAGE)


    def put_message(self, message):
        """
        writes the given message into the message bar.
        :param message: the message to write
        """
        self._clear_bar()
        self._win.addnstr(
            self._text_line, info_padding, message,
            message_width - 2*info_padding
        )


    def _clear_bar(self):
        self._win.addstr(
            self._text_line, info_padding, ' ' * (message_width-info_padding-1)
        )