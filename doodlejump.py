import pygame
from pygame.locals import *
import sys
import random
pygame.init()

sound1 = pygame.mixer.Sound('assets/springshoes.caf')
sound2 = pygame.mixer.Sound('assets/win.mp3')
sound3 = pygame.mixer.Sound('assets/jump.wav')
sound4 = pygame.mixer.Sound('assets/end.mp3')


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.bs = [0]
        self.score = 0
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.click = pygame.image.load("assets/click.png").convert_alpha()
        self.esc = pygame.image.load("assets/esc.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0

    def updatePlayer(self):
        if self.score % 10000 == 0 and self.score != 0:
            sound2.set_volume(0.1)
            sound2.play()
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                    sound3.set_volume(0.5)
                    sound3.play()
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))

        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(
                    pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(),
                                self.playerRight.get_height())):
                self.jump = 25
                sound1.play()
                self.cameray -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (800, x * 12))


    def besscore(self):
        if self.score > self.bs[-1]:
            self.bs.append(self.score)

    def end(self):
        sound4.set_volume(0.35)
        sound4.play()
        self.besscore()
        clock = pygame.time.Clock()
        FPS = 50
        self.screen.fill((255, 255, 255))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                    sys.exit()
        self.drawGrid()
        self.screen.blit(self.click, (50, 400))
        self.screen.blit(self.esc, (45, 500))
        f1 = pygame.font.SysFont('comicsansms', 64)
        text1 = f1.render('Вы проиграли!', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (190, 10))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('Ваш счет:', True,
                          (pygame.Color('red')))
        self.screen.blit(text1, (20, 100))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('Ваш лучший счет:', True,
                          (pygame.Color('red')))
        self.screen.blit(text1, (20, 200))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('    Попробуйте еще раз и побейте ваш рекорд!', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (20, 300))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('- продолжить игру', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (115, 408))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('- выйти из игры', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (115, 501))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render(f'{self.score}', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (200, 100))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render(f'{self.score}', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (200, 100))
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render(f'{self.bs[-1]}', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (325, 200))
        f1 = pygame.font.SysFont('comicsansms', 16)
        text1 = f1.render(f'(в текущей сесии)', True,
                          (pygame.Color('red')))
        self.screen.blit(text1, (95, 235))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cameray = 0
                    self.score = 0
                    self.springs = []
                    self.platforms = [[400, 500, 0, 0]]
                    self.generatePlatforms()
                    self.playerx = 400
                    self.playery = 400
                    self.run()
            pygame.display.flip()
            clock.tick(FPS)
            pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 700:
                self.end()
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()


DoodleJump().run()

