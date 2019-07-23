from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import *
import random
import math

class Stage2_boss(Boss):
    def __init__(self, x, y, players, score, money):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, y, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.dx,self.dy = -2, 0
        self.score = score
        self.money = money
        #self.load_count = True

        Stage2_sub(self.rect.centerx,self.rect.centery-100, players, self.score, 0, self, self.money)
        Stage2_sub(self.rect.centerx,self.rect.centery+100, players, self.score, 1, self, self.money)
        #Stage1_sub(mg.centerx-60, 600, self.machines, self.score, self.load_count, self, self.money)
    
    def update(self):
        if self.rect.centerx <= 400:
            self.dx = 0
        self.move(self.dx,self.dy)
        print("update")


class Stage2_sub(Boss):
    def __init__(self, x, y, players, score, sub_number, boss, money):              
        image = pygame.image.load("img/bot.png").convert_alpha()
        super().__init__(5, x, y, image, players, score, money)
        self.boss = boss
        self.number = sub_number
    
    def update(self):
        self.dx,self.dy = self.boss.dx,self.boss.dy
        self.move(self.dx,self.dy)
        print("sub_update")