#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys

class Money:
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 20)
        self.money = 0
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render("MONEY:" + str(self.money), True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))

    def add_money(self, x):
        self.money += x 
    