from machine import Machine
import pygame
from define import *
from gun import *

class Boss(Machine):
    def __init__(self, hp, x, y, image, players, score):
        super().__init__(hp, x, y, image, players, score) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()               #Bossが呼ばれた時のクロック数を入力

class Stage1_boss(Boss):                                 #ボス本体の機体
    def __init__(self, x, y, players, score):
        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(1, x, y, image, players, score)         #superクラス(Boss)を呼び出す
        self.stage1_flag = 0

    def update(self):
        self.move(-1, 0)
        if R_time.get_ticks() - self.gun_start >= 600 and self.stage1_flag == 0:
            for sub_number in range(5):
                Stage1_sub(self.x, self.y, self.machines, self.score, sub_number)
            self.stage1_flag = 1

class Stage1_sub(Boss):                                  #ボス付属品の機体
    def __init__(self, x, y, players, score, sub_number):              
        image = pygame.image.load("img/boss1_sub.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.sub_number = sub_number                     #付属品のID

    def update(self):
        self.move(-2, 0)