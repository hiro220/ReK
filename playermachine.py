# coding:utf-8

from machine import Machine
import pygame
from pygame.locals import *

class PlayerMachine(Machine):

    def __init__(self, x, y):
        img = pygame.image.load("img/player.png").convert_alpha()
        self.image = img
        super().__init__(1, x, y, img)
        self.dx, self.dy = 7, 7

    def show(self, screen):
        super().show(screen)

    def move(self, height, width):
        key = pygame.key.get_pressed()
        if key[K_UP]:
            super().move(0, -self.dy)
        if key[K_DOWN]:
            super().move(0, self.dy)
        if key[K_RIGHT]:
            super().move(self.dx, 0)
        if key[K_LEFT]:
            super().move(-self.dx, 0)
        self.rect.clamp_ip(Rect(0, 0, width, height))

    def shoot(self, key):
        if key == K_x:
            return super().shoot()
            