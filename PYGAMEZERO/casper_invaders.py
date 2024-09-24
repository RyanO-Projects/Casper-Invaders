import pgzrun
import random

WIDTH = 1000
HEIGHT = 662

# Setup the player
player = Actor('player')
player.x = WIDTH // 2
player.y = HEIGHT - 40
bolt = Actor('lightning', (-100, 1001))
player_bolt_speed = 8

# Setup enemies
enemies = []
enemy_bolts = []
direction = 'right'
speed = 0

# Set initial conditions
score = 0
timer = 0
game_start = True
is_game_over = False

# Power up
x2_power = Actor('x2', (-250, 0))

# Player controls:
# left arrow to go left
# right arrow to go right
# spacebar to shoot
def player_control():
    if keyboard.left:
        player.x -= 3
    elif keyboard.right:
         player.x += 3
    if keyboard.space and bolt.y < 0:
         player_bolt()

# Display
def draw():
    screen.clear()
    screen.blit('background', (0, 0))
    player.draw()
    for enemy in enemies:
         enemy.draw()
    for enemy_bolt in enemy_bolts:
         enemy_bolt.draw()
    bolt.draw()
    x2_power.draw()
    drawScore()

def update():
     global game_start
     global direction
     global player_bolt_speed
     global timer
     timer += 1

     if game_start:
          position_enemies()
          game_start = False
          
     if len(enemies) == 0:
          restart()
               
     player_control()
          
     if not is_game_over:
          move_enemies(direction, speed)
          enemy_edge_check()
          check_collisions()
          # RNG for enemies to sporadically shoot at player
          for enemy in enemies:
               if random.randint(1, 12000) == 42:
                    enemy_make_bolt(enemy.x, enemy.y)

          move_enemy_bolts()

     move_x2_power()
     if random.randint(1,100) == 50 and x2_power.x == -250:
          x2_power.x = random.randint(80, 920)
          x2_power.y = 100
     ######
     if timer % 600 == 0:
          player_bolt_speed = 8
     # Player's fired bolt movement
     bolt.y -= player_bolt_speed


# Function that controls movement of x2 powerup
def move_x2_power():
     global x2_power
     x2_power.y += 3
     if x2_power.y > 1000:
          x2_power.x = -250
          x2_power.y = 0

# Resets game when all enemies are 
def restart():
     global direction
     global speed
     player.x = WIDTH // 2
     player.y = HEIGHT - 40
     position_enemies()
     direction = 'right'
     speed = 0
     

# Function to check for collisions between player, player bolt and enemies
def check_collisions():
     global is_game_over
     global score
     global timer
     global player_bolt_speed

     if x2_power.colliderect(player):
          sounds.powerup.play()
          player_bolt_speed = 16
          x2_power.x = -250
          timer = 1
     for enemy in enemies:
          if enemy.colliderect(bolt):
               score += 1
               enemies.remove(enemy)
               bolt.y = -100
               
          if enemy.colliderect(player):
               is_game_over = True
               drawScore()


# Dictates movement of enemies.
def move_enemies(direction, horizSpeed):
     global enemies
     for enemy in enemies:
        if direction == 'right':
            enemy.x += (0.8 + horizSpeed)
        elif direction == 'left':
            enemy.x -= (0.8 + horizSpeed)

# Checks to verify that all enemies are on screen,
# if enemy reaches edge of screen direction is reversed
def enemy_edge_check():
    global direction
    global speed
    flag = True
    for enemy in enemies:
        if enemy.x <= 30 and flag:
           direction = 'right'
           decrease_enemy_vertical()
           flag = False
        elif enemy.x >= (WIDTH - 30) and flag:
            direction = 'left'
            decrease_enemy_vertical()
            flag = False

# Upon condition, enemy will 'fire' a bolt at the player
def enemy_make_bolt(x, y):
     global enemy_bolts
     enemy_bolt = Actor('enemy_lightning', (x, y))
     enemy_bolts.append(enemy_bolt)

# Dictates movement of enemy projectiles
def move_enemy_bolts():
     global enemy_bolts
     global is_game_over
     for enemy_bolt in enemy_bolts:
          enemy_bolt.y +=3
          if enemy_bolt.y > 662:
               enemy_bolts.remove(enemy_bolt)
          if enemy_bolt.colliderect(player):
               is_game_over = True

# Upon enemy reaching edge of screen, enemies are moved closer
# to player and have horizontal move speed increased
def decrease_enemy_vertical():
     global enemies
     global speed
     speed += 0.3
     for enemy in enemies:
          enemy.y += 30

# Upon player firing projectile with 'space' the position of the
# projectile is updated to the players current positon
def player_bolt():
     bolt.x = player.x + 35
     bolt.y = player.y -  50
     sounds.pew.play()

# Creates enemies and positions them
def position_enemies():
        generate_enemies(11, 80, 30, 'untitled1')
        generate_enemies(11, 80, 60, 'untitled1')
        generate_enemies(11, 80, 95, 'trex2')
        generate_enemies(11, 80, 135, 'trex2')

# Function to create enemies and store them in array.
# Mainly created to clear up old redundant
# code in position_enemies()
def generate_enemies(numEnem, x, y, enemy_type):
     global enemies
     enemy_x = x
     enemy_y = y
     for i in range(numEnem):
        actor = Actor(enemy_type)
        actor.x = enemy_x
        actor.y = enemy_y
        enemies.append(actor)
        enemy_x += 50

# Game over screen, displays final score
def drawScore():
     screen.draw.text("Score: " + str(score), (45, 30))
     if is_game_over:
          display_text = "GAME OVER\nFINAL SCORE: " + str((score))
          position = (WIDTH//2)-200, (HEIGHT//2)-100
          screen.draw.text(display_text, position, fontsize=60, color=(255,255,255))
          
pgzrun.go()