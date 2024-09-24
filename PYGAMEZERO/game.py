import pgzrun
import random

WIDTH = 800
HEIGHT = 600
bowl = Actor('basket')
#position the basket
bowl.x = WIDTH // 2
bowl.y = HEIGHT - 40
apple = Actor('apple')
score = 0
game_timer = 10
is_game_over = False

def moveBasket():
    if keyboard.left:
        bowl.x -= 5
    elif keyboard.right:
        bowl.x += 5

def draw():
    screen.clear()
    screen.blit('skybg', (0, 0))
    bowl.draw()
    apple.draw()
    drawScore()

def update():
        global score
        global game_timer
        global is_game_over
        if is_game_over == False:
             game_timer -= 0.017
             moveBasket()
             if apple.y > HEIGHT + 40:
                 position_fruit()
             else:
                 apple.y += 10

        if apple.colliderect(bowl):
             score += 1
             print(score)
             position_fruit()
        if game_timer < 0:
             is_game_over = True

def position_fruit():
        apple.x = random.randint(40, WIDTH - 40)
        apple.y = -100

def drawScore():
     screen.draw.text("score: " + str(score), (45, 30))
     screen.draw.text("Time: " + str(round(game_timer)), (45, 60))
     if is_game_over:
          display_text = "GAME OVER\nFINAL SCORE: " + str((score))
          position = (WIDTH//2)-100, (HEIGHT//2)
          screen.draw.text(display_text, position, fontsize=60, color=(255,255,255))
pgzrun.go()