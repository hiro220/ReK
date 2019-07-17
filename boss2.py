from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import *
import random
import math

class Stage2_boss(Boss):
    def __init__(self, hp, x, y, image, players, score, money):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, y, image, players, score, money)         #superクラス(Boss)を呼び出す
    
    def update(self):
        print("update")


class Stage1_sub(Boss):
    def __init__(self, x, y, players, score, sub_number, boss, money):              
        image = pygame.image.load("img/boss1_sub.png").convert_alpha()
        super().__init__(5, x, y, image, players, score, money)
    
    def update(self):
        print("sub_update")