# coding:utf-8

import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):

    def __init__(self, x, y, img, player):
        self.x, self.y = x, y
        self.image = img
        self.rect = self.image.get_rect()
        self.player = player
        self.speed = 1

    def update(self):
        self.rect.move_ip(self.speed, 0)
        collide_list = pygame.sprite.spritecollide(self, self.player, False)
        for player in collide_list:
            self.effect(player)

    def effect(self, player):
        pass

        