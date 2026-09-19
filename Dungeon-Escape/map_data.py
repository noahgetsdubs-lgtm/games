from room import Room

def generate_map(width, height):
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            if x==0 and y==0:
                row.append(Room("You awaken in a dark cave. There's a tunnel leading forward.", "start"))
            elif x == width - 1 and y == height - 1:
                row.append(Room("You see sunlight! The exit is ahead." "exit"))
            else:
                row.append(Room("A quiet empty stone chamber"))
        grid.append(row)
    return grid