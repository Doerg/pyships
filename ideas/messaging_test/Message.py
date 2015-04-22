class ResultMessage(object):
    def __init__(self, result):
        self.result = result

class ExitMessage(object):
    pass

class PlacementMessage(object):
    def __init__(self, coords):
        self.coords = coords
