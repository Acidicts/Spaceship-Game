import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 1280, 720

pygame.display.set_caption("Game")
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

player = pygame.image.load("images/player.png").convert_alpha()
player_rect = player.get_rect(center=(WIDTH/2, HEIGHT/2))

stars = pygame.image.load('images/star.png').convert_alpha()
star_pos = [(randint(0, WIDTH), randint(0, HEIGHT)) for _ in range(20)]

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= 5
    if keys[pygame.K_d]:
        player_rect.x += 5

    win.fill('darkgray')
    for star in star_pos:
        win.blit(stars, star)

    win.blit(player, (player_rect))

    pygame.display.update()
