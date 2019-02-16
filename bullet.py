#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.dx, self.dy = dx, dy
        self.machines = machines
        
        # updateで呼ばれるメソッドをmoveに設定する。
        self.update = self.move

    def move(self):
        self.rect.move_ip(self.dx, self.dy)
        if pygame.sprite.spritecollide(self, self.machines, True):
            self.kill()
