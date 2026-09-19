from player import Player
from map_data import generate_map

class Game:
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.map = generate_map(width, height)
        self.player = Player(0,0)

    def draw_map(self):
        for y in range (self.height):
            row = ""
            for x in range(self.width):
                room = self.map[y][x]
                if self.player.x == x and self.player.y == y:
                    row += "p "
                elif room.visited:
                    row += "o "
                else:
                    row += ". "
            print(row)
        print()

    def play_turn(self):
        command = input("Move (n/s/e/w or q to quit): ").lower()
        if command == "q":
            return False
        moves = {"n" : (0, -1), "s": (0, 1), "e": (1, 0), "w": (-1, 0)}
        if command in moves:
            dx, dy = moves[command]
            moved = self.player.move(dx, dy, self.width, self.height)
            if moved:
                room = self.map[self.player.y][self.player.x]
                room.enter()
                print(f"Location: ({self.player.x}, {self.player.y})")
            if room.room_type == "exit":
                print("You escaped the Dungeon! Congratulations!")
                return False
        else:
            print("Invalid Command!")
        
        return True
