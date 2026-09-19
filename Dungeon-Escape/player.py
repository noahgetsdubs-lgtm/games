class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, dx, dy, map_width, map_height):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            self.x = new_x
            self.y = new_y
            return True
        else:
            print("You can't move that way!")
            return False