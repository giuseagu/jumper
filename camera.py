from constants import HEIGHT


class Camera:
    def __init__(self):
        self.offset = 0.0

    def update(self, player_y):
        # Move camera up when player is in the upper half
        target = player_y - HEIGHT * 0.4
        if target < self.offset:
            self.offset = target
