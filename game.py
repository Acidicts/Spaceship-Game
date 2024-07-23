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

    def death(self, parent):
        explosions = [pygame.image.load(f'images/explosion/{i}.png') for i in range(1, 20)]
        for explosion in explosions:
            parent.win.blit(explosion, (self.rect.centerx - explosion.get_rect().centerx, self.rect.centery))
            parent.clock.tick(10)
            pygame.display.flip()

            parent.running = False


class Meteor:
    def __init__(self):
        self.image = pygame.image.load('images/meteor.png')
        self.rect = self.image.get_rect()
        self.rect.center = (randint(0, 1280), -100)

    def draw(self, win):
        self.rect.y += 2
        win.blit(self.image, self.rect.topleft)


class Star:
    def __init__(self, location):
        self.image = pygame.image.load('images/star.png')
        self.pos = location

    def draw(self, win):
        self.pos = (self.pos[0], self.pos[1] + 1)
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
    def __init__(self, win, font):
        self.width = 1280
        self.height = 720
        self.win = win

        self.mixer = pygame.mixer
        self.font = font

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.player = Player(self)

        self.meteors = []
        self.stars = [Star((randint(0, self.width), randint(-1000, self.height))) for _ in range(10)]
        self.laser = None

        self.score = 0

        self.running = False
        self.intro = 10

    def circle(self, rad):
        surf = pygame.Surface((self.width, self.height))
        surf.fill('black')
        pygame.draw.circle(surf, 'white', self.player.rect.center, rad * 5)
        surf.set_colorkey('white')
        return surf

    def run(self):
        self.running = True

        self.mixer.music.set_volume(0.5)
        self.mixer.music.load('audio/game_music.wav')
        self.mixer.music.play(-1)

        self.mixer.music.set_volume(1)

        while self.running:
            self.clock.tick(60)
            self.win.fill('darkgray')

            for star in self.stars:
                if star.pos[1] > 720:
                    star.pos = (randint(0, self.width), randint(-1000, 0))
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

                        self.mixer.Sound('audio/laser.wav').play()

            mouse = pygame.mouse.get_pressed()
            mi = min(self.player.rect.centerx, pygame.mouse.get_pos()[0])
            ma = max(self.player.rect.centerx, pygame.mouse.get_pos()[0])
            diff = ma - mi
            if diff > 5 or diff < -5:
                if mouse[0]:
                    if self.player.rect.centerx < pygame.mouse.get_pos()[0]:
                        self.player.rect.x += 5
                    else:
                        self.player.rect.x -= 5

            if len(self.meteors) < 2 and randint(0, 100) < 10:
                self.meteors.append(Meteor())

            if self.laser:
                self.laser.draw(self.win)

            self.player.update(self.win)

            for meteor in self.meteors:
                meteor.draw(self.win)
                if meteor.rect.colliderect(self.player.rect):
                    self.mixer.Sound('audio/explosion.wav').play()
                    self.mixer.music.set_volume(0.5)
                    self.player.death(self)
                    self.running = False

                if self.laser:
                    if self.laser.rect.colliderect(meteor.rect):
                        laser = self.mixer.Sound('audio/damage.ogg')
                        laser.play()
                        self.meteors.remove(meteor)
                        self.laser = None
                        self.score += 1

                if meteor.rect.y > 720:
                    self.meteors.remove(meteor)

            if self.score > 0:
                text = self.font.render(f"Score: {self.score}", True, 'lightblue')
                self.win.blit(text, (10, 10))

            self.win.blit(self.circle(self.intro), (0, 0))
            self.intro += 1

            pygame.display.flip()

        self.end()

        while not self.running:
            self.win.fill('black')
            text = self.font.render(f"Score: {self.score}", True, 'lightblue')
            self.win.blit(text, (10, 10))
            text = self.font.render("Game Over", True, 'lightblue')
            self.win.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
            text = self.font.render("Press Space to play again", True, 'lightblue')
            self.win.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 + text.get_height() // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                        self.run()
