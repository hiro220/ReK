#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Range(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = (x,y,dx,dy)

class Range2(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = (x,y,dx,dy)