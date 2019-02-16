#!/usr/bin/env python
# coding:utf:-8

import pygame
from pygame.locals import *
from gun import Gun

class Machine(pygame.sprite.Sprite):

    def __init__(self, hp, x, y, img, machines):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.hp = hp
        self.img = img
        self.rect = img.get_rect()
        self.rect.move_ip(x, y)
        self.gun = Gun(machines)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def shoot(self):
        if self.gun.isBulletZero():
            return False
        x, y = self.rect.midright
        return self.gun.shoot(x, y)

    def update(self):
        pass