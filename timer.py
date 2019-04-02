# coding:utf-8

import pygame
from pygame.locals import *

class Timer(pygame.sprite.Sprite):

    def __init__(self, time, method):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.process = method
        self.time = time
        self.init_time = pygame.time.get_ticks()

    def update(self):
        print(pygame.time.get_ticks(), self.init_time)
        if pygame.time.get_ticks() - self.init_time >= self.time:
            self.process
            self.kill()