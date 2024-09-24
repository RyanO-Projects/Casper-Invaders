import pgzrun
import math

ship_x = 800 / 2
ship_y = 600 / 2
ship_angle = 0
ship_speed_x = 0
ship_speed_y = 0
arena_width = 800
arena_height = 600
bullets = []

def on_key_down(key):
    if key == keys.S:
        bullets.append({
            'x': ship_x,
            'y': ship_y,
        })

def update(dt):
    global ship_angle
    global ship_x
    global ship_y
    global ship_speed_x
    global ship_speed_y
    if keyboard.right:
        ship_angle += 10 * dt
    elif keyboard.left:
        ship_angle -= 10 * dt
    ship_angle %= 2 * math.pi
    if keyboard.up:
        ship_speed = 100
        ship_speed_x += math.cos(ship_angle) * ship_speed * dt
        ship_speed_y += math.sin(ship_angle) * ship_speed * dt
    ship_x += ship_speed_x * dt
    ship_y += ship_speed_y * dt
    ship_x %= arena_width
    ship_y %= arena_height

def draw():
    screen.fill((0,0,0))

    for y in range(-1,2):
        for x in range(-1,2):
            offset_x = x * arena_width
            offset_y = y *arena_height

            ship_circle_distance = 20
            screen.draw.filled_circle((
                ship_x + offset_x +
                    math.cos(ship_angle) * ship_circle_distance,
                ship_y + offset_y +
                    math.sin(ship_angle) * ship_circle_distance),
                5, color=(0,255,255)
            )
            for bullet in bullets:
                screen.draw.filled_circle(
                    (bullet['x'] + offset_x, bullet['y'] + offset_y),
                    5, color=(0,255,0)
                )

    screen.draw.filled_circle((800/2, 600/2), 30, color=(0,0,255))

    ship_circle_distance = 20
    screen.draw.filled_circle((
        ship_x + math.cos(ship_angle) * ship_circle_distance,
        ship_y + math.sin(ship_angle) * ship_circle_distance),
        5, color=(0,255,255))

pgzrun.go()