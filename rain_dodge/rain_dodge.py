import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BG = pygame.transform.scale(pygame.image.load("rain_dodge/bg.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT)) #Pass an image and a size to scale it to
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
PLAYER = pygame.transform.scale(pygame.image.load("rain_dodge/shuttle.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
LASER_WIDTH = 20
LASER_HEIGHT = 40
LASER_VEL = 3
LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("rain_dodge/laser.png"), (LASER_WIDTH, LASER_HEIGHT)), -5)
POINT_WIDTH = 20
POINT_HEIGHT = 30
POINT_VEL = 5
POINT = pygame.transform.scale(pygame.image.load("rain_dodge\coin.png"), (POINT_WIDTH, POINT_HEIGHT))
FONT = pygame.font.Font("rain_dodge\Sprintura Demo.otf", 30) #Font, size
PLAY_AGAIN_BUTTON_WIDTH = 400
PLAY_AGAIN_BUTTON_HEIGHT = 100
CRASH_SOUND = pygame.mixer.Sound("rain_dodge\crash.mp3")
COIN_COLLECT_SOUND = pygame.mixer.Sound("rain_dodge\coin-recieved.mp3")
BACKGROUND_MUSIC = pygame.mixer.Sound("rain_dodge\Background_music.mp3")
pygame.display.set_caption("Space Dodge") #Name of the Window

def draw(player, elapsed_time, lasers, points, score):
    WIN.blit(BG, (0, 0)) #blit takes an image and a starting coordinate and puts it on the window

    time_text = FONT.render(f"Time: {round(elapsed_time)}", 1, "white") #String, antialiasing, color
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (990 - score_text.get_width(), 10))

    WIN.blit(PLAYER, player) #Where to draw it, what color (string or RGB), what rectangle

    for laser in lasers:
        WIN.blit(LASER, laser)
    
    for point in points:
        WIN.blit(POINT, point )

    pygame.display.update() #updates the screen and applys the background


def main():
    run = True
    player = pygame.Rect(200, SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT ) #starting X, starting Y, Rect Width, Rect Height
    clock = pygame.time.Clock()
    laser = pygame.Rect(random.randint(0, SCREEN_WIDTH - LASER_WIDTH), -LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
    point = pygame.Rect(random.randint(0, SCREEN_WIDTH - LASER_WIDTH), -LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
    start_time = time.time()
    elapsed_time = 0
    laser_add_increment = 2000
    laser_count = 0
    lasers = []
    point_add_increment = 2000
    point_count = 0
    points = []
    hit = False
    score = 0



    while run:
        BACKGROUND_MUSIC.play(-1)
        dt = clock.tick(60) #How many times the while loop runs per second needs the clock object to be made
        laser_count += dt
        point_count += dt
        elapsed_time = time.time() - start_time
        buttons = pygame.mouse.get_pressed()

        if laser_count > laser_add_increment:
            for _ in range (3):
                laser_x = random.randint(0, SCREEN_WIDTH - LASER_WIDTH)
                laser = pygame.Rect(laser_x, -LASER_HEIGHT, LASER_WIDTH, LASER_HEIGHT)
                lasers.append(laser)

            laser_add_increment = max(200, laser_add_increment - 50)
            laser_count = 0

        if point_count > point_add_increment:
            point_x = random.randint(0, SCREEN_WIDTH - POINT_WIDTH)
            point = pygame.Rect(point_x, -POINT_HEIGHT, POINT_WIDTH, POINT_HEIGHT)
            points.append(point)
            point_add_increment = max(500, point_add_increment - 50)
            point_count = 0
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_WIDTH + PLAYER_VEL <= SCREEN_WIDTH:
            player.x += PLAYER_VEL

        for laser in lasers[:]: #Colon in the brackets makes a copy of the list, since list will be edited in the loop
            laser.y += LASER_VEL
            if laser.y > SCREEN_HEIGHT:
                lasers.remove(laser)
            elif laser.y + laser.height >= player.y and laser.colliderect(player):
                lasers.remove(laser)
                hit = True
                break

        for point in points[:]:
            point.y += POINT_VEL
            if point.y > SCREEN_HEIGHT:
                points.remove(point)
            elif point.y + point.height >= player.y and point.colliderect(player):
                COIN_COLLECT_SOUND.play()
                points.remove(point)
                score += 1

        if hit:
            CRASH_SOUND.play()
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (SCREEN_WIDTH/2 - lost_text.get_width()/2, SCREEN_HEIGHT/5 - lost_text.get_height()/2))
            play_again_text = FONT.render("Play Again?", 1, "White")
            play_again_button = pygame.Rect(SCREEN_WIDTH/2 - PLAY_AGAIN_BUTTON_WIDTH/2, SCREEN_HEIGHT/1.5 - play_again_text.get_height()/2 - 50, PLAY_AGAIN_BUTTON_WIDTH, PLAY_AGAIN_BUTTON_HEIGHT)
            pygame.draw.rect(WIN, "blue", play_again_button)
            WIN.blit(play_again_text, (SCREEN_WIDTH/2 - play_again_text.get_width()/2, SCREEN_HEIGHT/1.5 - play_again_text.get_height()/2 - 30 + play_again_text.get_height()/2))
            pygame.display.update()
            while hit:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if play_again_button.collidepoint(event.pos):
                                hit = False
                                score = 0
                                lasers.clear()
                                points.clear()
                                player.x = 200
                                player.y = SCREEN_HEIGHT - PLAYER_HEIGHT
                                start_time = time.time()
                                point_add_increment = 2000
                                laser_add_increment = 2000
                                laser_count = 0
                                break
                if event.type == pygame.QUIT:
                    run = False
                    break
                            




        draw(player, elapsed_time, lasers, points, score)

    pygame.quit

if __name__ == "__main__":
    main()