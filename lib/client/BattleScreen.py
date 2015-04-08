from client import BattleWindows


def init(player_name):
    global _background_win, _key_win, _player_win, _enemy_win, _message_win

    _frame_win = BattleWindows.ContentFrame(player_name)
    _key_win = BattleWindows.KeyLegend()
    _player_win = BattleWindows.BattleGround()
    _enemy_win = BattleWindows.BattleGround(opponent=True)
    _message_win = BattleWindows.MessageBar()

    _frame_win.refresh()
    _key_win.refresh()
    _player_win.refresh()
    _enemy_win.refresh()
    _message_win.refresh()

    _message_win._win.getch() #remove me