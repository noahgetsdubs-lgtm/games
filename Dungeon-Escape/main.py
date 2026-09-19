from game import Game

def main():
    game = Game()

    running = True
    while running:
        game.draw_map()
        running = game.play_turn()

    print("Game Over")

if __name__ == "__main__":
    main()
