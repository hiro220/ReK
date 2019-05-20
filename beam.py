#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *

class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, machines, principal, img):
        """Beamの基礎情報"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(img).convert_alpha()   # 相対パスで画像を読み込む
        self.rect = self.image.get_rect()
        self.p_rect = principal
        self.rect.move_ip(x, y)
        self.dx, self.dy = dx, dy       # 移動量
        self.machines = machines
        self.gun_start = pygame.time.get_ticks()
        self.count = 0
        self.flag = 0
        
class Beam_principal(Beam):
    def __init__(self, x, y, dx, dy, machines, principal, img):
        super().__init__(x, y, dx, dy, machines, principal, img)
        Beam_sub(x, y, dx, dy, machines, principal, "img/beam5.png")
        self.image = pygame.transform.smoothscale(self.image, (10,self.rect.height))
        self.rect = self.image.get_rect()
        x = x - self.rect.width
    
    def update(self):
        if pygame.time.get_ticks() - self.gun_start >= 1000 and self.rect.width <= 600:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width+10,self.rect.height))
            self.rect = self.image.get_rect()
        elif self.rect.width >= 600 and self.count == 0:
            self.gun_start = pygame.time.get_ticks()
            self.flag = 1
            self.count = 1
        if pygame.time.get_ticks() - self.gun_start >= 1000 and self.rect.height > 0 and self.flag == 1:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width,self.rect.height-1))
            self.rect = self.image.get_rect()
        x, y = self.p_rect.midleft
        self.rect.midright = (x, y+5)
            
class Beam_sub(Beam):
    def __init__(self, x, y, dx, dy, machines, principal, img):
        super().__init__(x, y, dx, dy, machines, principal, img)
        self.change_image = pygame.image.load("img/beam5.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (9,6))
        self.c_image1 = pygame.transform.smoothscale(self.image, (14,9))
        self.c_image2 = pygame.transform.smoothscale(self.image, (17,12))
        self.c_image3 = pygame.transform.smoothscale(self.image, (20,15))
        self.c_image4 = pygame.transform.smoothscale(self.image, (23,18))
        self.c_image5 = pygame.transform.smoothscale(self.image, (25,23))
        self.c_image9 = pygame.transform.smoothscale(self.change_image, (27,24))
        self.c_data = [self.c_image1,self.c_image2,self.c_image3,self.c_image4,self.c_image5,self.c_image9]
        
        
    def update(self):
        if  self.flag == 0 and self.count < 6:
            self.image = self.c_data[self.count]
            self.count += 1
        elif self.count < 7:
            self.flag = 1 

        if pygame.time.get_ticks() - self.gun_start >= 3900 and self.flag == 1 and self.rect.height > 0:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width-1,self.rect.height-1))
            self.rect = self.image.get_rect()
        
        x, y = self.p_rect.midleft
        self.rect.midright = (x, y+5)
        