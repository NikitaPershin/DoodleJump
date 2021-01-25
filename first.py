import pygame
from pygame.locals import *
pygame.init()

pygame.mixer.music.load('assets/start.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.red_1 = pygame.image.load("assets/13.png").convert_alpha()


    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (800, x * 12))

    def run(self):
        clock = pygame.time.Clock()
        FPS = 50
        self.screen.fill((255, 255, 255))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                    ys.exit()
        intro_text = ["     ", "",
                        "     Правила игры:",
                        "Прыгайте как можно", ''
                        "выше и дольше чем", ''
                        'выше, тем больше',
                        'очков']
        f1 = pygame.font.SysFont('comicsansms', 32)
        text1 = f1.render('     Нажмите любую кнопку чтобы начать игру', True,
                          (pygame.Color('black')))
        self.drawGrid()
        self.screen.blit(self.red_1, (20, 200))
        self.screen.blit(text1, (20, 525))
        f1 = pygame.font.SysFont('comicsansms', 64)
        text1 = f1.render(f'Doodle Jump', True,
                          (pygame.Color('black')))
        self.screen.blit(text1, (210, 5))
        font = pygame.font.SysFont('comicsansms', 32)
        text_coord = 25
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 450
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    import doodlejump.py
            pygame.display.flip()
            clock.tick(FPS)
            pygame.display.flip()

DoodleJump().run()