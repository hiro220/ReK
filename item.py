# coding:utf-8

import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):

    def __init__(self, x, y, img, player):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = img
        self.rect = self.image.get_rect()
        self.player = player
        self.speed = -1
        self.rect.move_ip(x, y)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        collide_list = pygame.sprite.spritecollide(self, self.player, False)
        if collide_list:
            self.kill()
            for player in collide_list:
                self.effect(player)

    def effect(self, player):
        pass

class Recovery(Item):

    def __init__(self, x, y, machine):
        image = pygame.image.load("img/player.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, player):
        player.recover(1)