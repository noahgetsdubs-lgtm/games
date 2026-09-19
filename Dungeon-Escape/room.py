class Room:
    def __init__(self, description = "An Empty Room.", room_type = "Empty"):
        self.description = description
        self.room_type = room_type
        self.visited = False

    def enter(self):
        if not self.visited:
            print(self.description)
            self.visited = True
        else:
            print("You've been here before.")
            
