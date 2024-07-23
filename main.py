import sys

import pygame
from sys import exit
from random import randint


class Player:
    def __init__(self, parent):
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (parent.width // 2, parent.height // 2)
        self.direction = pygame.math.Vector2(1, 1)

        self.speed = 20

    def controls(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    def update(self, win):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.controls()
        self.draw(win)


class Meteor:
    def __init__(self):
        self.image = pygame.image.load('images/meteor.png')
        self.rect = self.image.get_rect()

    def draw(self, win):
        self.rect.y += 10
        win.blit(self.image, self.rect.topleft)


class Star:
    def __init__(self, location):
        self.image = pygame.image.load('images/star.png')
        self.pos = location

    def draw(self, win):
        win.blit(self.image, self.pos)


class Laser:
    def __init__(self, pos):
        self.image = pygame.image.load('images/laser.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, win):
        self.rect.y -= 5
        win.blit(self.image, self.rect.topleft)


class Game:
    def __init__(self):
        pygame.init()

        self.width = 1280
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))

        self.mixer = pygame.mixer

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.player = Player(self)

        self.meteors = []
        self.stars = [Star((randint(0, self.width), randint(0, self.height))) for _ in range(10)]
        self.laser = None

        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(60)
            self.win.fill('darkgray')

            for star in self.stars:
                star.draw(self.win)

            if self.laser is not None:
                if self.laser.rect.y < 0:
                    self.laser = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.laser:
                        self.laser = Laser(self.player.rect.center)

            if self.laser:
                self.laser.draw(self.win)

            self.player.update(self.win)

            pygame.display.flip()


game = Game()
game.run()
