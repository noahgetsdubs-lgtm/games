#Added Score, collectible, movement boundaries, other obstacle and difficulty scaling

import tkinter as tk
import random
import time

#Declare CONSTANTS

SCREEN_WIDTH = 400
SCREEN_HEIGHT = SCREEN_WIDTH * 0.75
PLAYER_SIZE = 30
ENEMY_SIZE = 20
COIN_SIZE = 20

#Build Window
root = tk.Tk()
root.title("Avoid the Blocks")

canvas = tk.Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, bg = "black")
canvas.pack()



#Make the Player
player = canvas.create_rectangle(180, 250, 180 + PLAYER_SIZE, 250 + PLAYER_SIZE, fill = "magenta")


#Make a list to hold enemies
enemies = []
coins = []

#make an alive bool
alive = True
enemies_spawned = 0
score = 0
side_bar_count = 0 
left_side_bar = 0
right_side_bar = 0 
score_text = canvas.create_text(10, 10, anchor = "nw", text = f"Score: {score}", fill = "white")

#Movement functions

def move_left(event):
    if canvas.coords(player)[0] - 20 > 0:
        canvas.move(player, -20, 0)
    else:
        canvas.moveto(player, 0)
def move_right(event):
    if canvas.coords(player)[2] + 20 < SCREEN_WIDTH:
        canvas.move(player, 20, 0)
    else:
        canvas.moveto(player, SCREEN_WIDTH - PLAYER_SIZE)


#Binding Buttons
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)


#Enemies
def spawn_enemy():
    global enemies_spawned
    x = random.randint(side_bar_count * 20, SCREEN_WIDTH - ENEMY_SIZE - side_bar_count * 20)
    enemy = canvas.create_rectangle(x, 0, x + ENEMY_SIZE, ENEMY_SIZE, fill = "red")
    enemies.append(enemy)
    enemies_spawned += 1

def drop_bars():
    if canvas.coords(right_side_bar)[3] != SCREEN_HEIGHT and canvas.coords(left_side_bar)[3] != SCREEN_HEIGHT:
        canvas.move(right_side_bar, 0, 10)
        canvas.move(left_side_bar, 0, 10)
        canvas.after(30, drop_bars)

def spawn_coin():
    x = random.randint(side_bar_count * 20, SCREEN_WIDTH - ENEMY_SIZE - side_bar_count * 20)
    coin = canvas.create_rectangle(x, 0, x + COIN_SIZE, COIN_SIZE, fill = "gold")
    coins.append(coin)

def run_game():
    global alive
    global score
    global enemies_spawned
    global right_side_bar
    global left_side_bar
    #start_time = time.time()

    if not alive:
        canvas.create_text(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, text = "GAME OVER", fill = "white")
        return
    else:
        #elapsed_time = time.time() - start_time
        #time_text = tk.Label(root,   text = str(elapsed_time), height=10, width= 50 )
        #time_text.pack()
        pass

    
    if random.randint(1, 20) == 1:
        spawn_enemy()
        
    
    if random.randint(1, 50) == 1:
        spawn_coin()
    
    for enemy in enemies:
        canvas.move(enemy, 0, min(max(enemies_spawned, 10), 30))

        if canvas.bbox(enemy) and canvas.bbox(player):
            ex1, ey1, ex2, ey2 = canvas.bbox(enemy)
            px1, py1, px2, py2 = canvas.bbox(player)

            if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1:
                alive = False
            
    if enemies_spawned % 10 == 9:
        global score_text
        global side_bar_count
        left_side_bar = canvas.create_rectangle(0, -SCREEN_HEIGHT, side_bar_count * 20 +20, 0, fill = "red")
        right_side_bar = canvas.create_rectangle((SCREEN_WIDTH-side_bar_count * 20)-20, -SCREEN_HEIGHT, SCREEN_WIDTH, 0, fill = "red")
        side_bar_count += 1
        drop_bars()
        canvas.delete(score_text)
        score_text = canvas.create_text(10, 10, anchor = "nw", text = f"Score: {score}", fill = "white")
        spawn_enemy()

    
    for coin in coins:
        canvas.move(coin, 0, 10)

        if canvas.bbox(coin) and canvas.bbox(player):
            ex1, ey1, ex2, ey2 = canvas.bbox(coin)
            px1, py1, px2, py2 = canvas.bbox(player)

            if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1:
                canvas.delete(coin)
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
        
    if canvas.bbox(right_side_bar) and canvas.bbox(player):
            ex1, ey1, ex2, ey2 = canvas.bbox(right_side_bar)
            px1, py1, px2, py2 = canvas.bbox(player)

            if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1:
                alive = False
    if canvas.bbox(left_side_bar) and canvas.bbox(player):
            ex1, ey1, ex2, ey2 = canvas.bbox(left_side_bar)
            px1, py1, px2, py2 = canvas.bbox(player)

            if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1:
                alive = False



    root.after(50, run_game)
run_game()
root.mainloop()

