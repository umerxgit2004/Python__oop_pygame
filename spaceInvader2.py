import pygame as pg
import random as rd
import math as math
from pygame import mixer

# Initialize Pygame
pg.init()

# Set up the screen
screen_width, screen_height = 600, 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Space Mission")
icon = pg.image.load("startup.png")
background = pg.image.load("bgnew.jpg")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

pg.display.set_icon(icon)

# Score
score = 0
font = pg.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


class Player:
    def __init__(self, x, y, img, x_change):
        self.img = img
        self.x = x
        self.y = y
        self.x_change = x_change

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.x_change
        if keys[pg.K_RIGHT]:
            self.x += self.x_change
        self.x = max(0, min(self.x, screen_width - 64))

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, img, x_change, y_change):
        self.img = img
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def move(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= screen_width - 64:
            self.x_change = -self.x_change
            self.y += self.y_change

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, img, y_change):
        self.img = img
        self.x = x
        self.y = y
        self.y_change = y_change
        self.state = "ready"

    def fire(self):
        self.state = "fire"
        screen.blit(self.img, (self.x + 16, self.y + 10))
        mixer.Sound('laser.wav').play()

    def move(self):
        if self.y <= 0:
            self.y = 500
            self.state = "ready"
        if self.state == "fire":
            self.fire()
            self.y -= self.y_change


# Instantiate objects
player = Player(250, 500, pg.image.load("spaceship.png"), 0.5)
enemies = [Enemy(rd.randint(0, 530), rd.randint(50, 150), pg.image.load("space-invaders.png"), 0.3, 2) for _ in
           range(6)]
bullet = Bullet(0, 500, pg.image.load("bullet.png"), 0.4)

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if bullet.state == "ready":
                bullet.x = player.x
                bullet.fire()

    player.move()
    player.draw()

    for enemy in enemies:
        enemy.move()
        if bullet.state == "fire" and math.sqrt(
                math.pow(enemy.x - bullet.x, 2) + math.pow(enemy.y - bullet.y, 2)) < 27:
            mixer.Sound('explosion.wav').play()
            bullet.y = 500
            bullet.state = "ready"
            score += 1
            print(score)
            enemy.x = rd.randint(0, screen_width - 64)
            enemy.y = rd.randint(50, 150)

        enemy.draw()

    bullet.move()
    ShowScore(textX, textY)

    # Game Over Condition
    if any(enemy.y > 440 for enemy in enemies):
        for enemy in enemies:
            enemy.y = 2000
        game_over_text()
        break

    pg.display.update()
