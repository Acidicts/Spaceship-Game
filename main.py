import pygame
from game import Game
from random import randint
from sys import exit

pygame.init()

font = pygame.font.Font("images/Oxanium-Bold.ttf", 100)
win = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

ship = pygame.image.load('images/player.png')
ship = pygame.transform.rotate(ship, 270)

pos = -100

while True:
    clock.tick(60)
    win.fill('darkgray')
    text = font.render("Press any key to start", True, 'white')
    win.blit(text, (640 - text.get_width() // 2, 360 - text.get_height() // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            font = pygame.font.Font("images/Oxanium-Bold.ttf", 48)
            game = Game(win, font)
            game.run()

    win.blit(ship, (pos, 100))
    pos += 10
    win.blit(pygame.transform.rotate(ship, 180), (1180 - pos, 500))

    if pos > 1280:
        pos = -100

    pygame.display.update()
