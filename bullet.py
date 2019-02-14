#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("img/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.dx, self.dy = dx, dy
        
        # updateで呼ばれるメソッドをmoveに設定する。
        self.update = self.move

    def show(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect)

    def move(self):
        self.rect.move_ip(self.dx, self.dy)

    def isHit(self, rect):
        """当たり判定の計算。"""
        if self.rect.collidelist([rect]) == -1:
            return False
        return True

    def getHitJudge(self):
        return self.rect