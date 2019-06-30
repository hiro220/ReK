#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys

class Score:
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont(None, 20)
        self.score = 0
        (self.x, self.y) = (x, y)

    def draw(self, screen):
        img = self.sysfont.render("SCORE:" + str(self.score), True, (255, 255, 255))
        screen.blit(img, (self.x, self.y))

    def add_score(self, x):
        self.score += x 
    
    def return_score(self):
        return self.score