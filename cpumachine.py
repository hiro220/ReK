# coding;utf-8

from machine import Machine
import pygame
from define import *
from gun import *


#comment
class CpuMachine(Machine):
    def __init__(self, hp, x, y, image, players, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        super().__init__(hp, x, y, image, players, score, money) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()          #createCPUが呼ばれた時のクロック数を入力
#これはデバック用のCPUです。
class cpu0(CpuMachine): 
    def __init__(self, x, y, players, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(1, x, y, image, players, score, money)         #superクラス(CpuMachine)を呼び出す
        self.dx, self.dy = 5, 5                                  #機体自身の位置を入力　　
        self.gun = Missile_Gun(self.machines, self, 1)             #machineクラスのself.gunを上書きする
        self.count = 0                                           #このクラスupdataが呼ばれた回数を保存する
    
    def update(self):
        if 0 <= self.count <= 150:
            self.dx, self.dy = -2.5, 0
            self.rect.move_ip(self.dx, self.dy)                  #機体の移動方向と速度を入力
            self.count += 1
        x, y = self.rect.midleft                                 #機体自身の位置を入力
        super().shoot(x, y)

    
class cpu(CpuMachine):
    def __init__(self, x, y, players, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money)
        self.dx, self.dy = 5, 5
        self.gun = Opposite_Gun(self.machines, self, 10)
    
    def update(self):
        self.dx, self.dy = -2.5, 0
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu2(CpuMachine):
    def __init__(self, x, y, players, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money)
        self.dx, self.dy = 5, 5
        self.count = 0
        self.gun = Reflection_Gun(self.machines, self, 10)
    
    def update(self):
        if 0 <= self.count <= 14:
            self.dx, self.dy = -2.5, 3
            self.rect.move_ip(self.dx,self.dy)
            self.count += 1
        elif 15 <= self.count <= 30:
            self.dx, self.dy = -2.5, -3
            self.rect.move_ip(self.dx, self.dy)
            self.count += 1
            if self.count == 31:
                self.count = 0

        x, y = self.rect.midleft
        
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks() 

class cpu3(CpuMachine):
    def __init__(self, x, y, players, score, money):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money)
        self.dx, self.dy = 5, 5
        self.count = 0
        self.gun = Tracking_Gun(self.machines, self, 10)

    def update(self):
        if 0 <= self.count <= 150:
            self.dx, self.dy = -2.5, 0
            self.rect.move_ip(self.dx, self.dy)
            self.count += 1

        x, y = self.rect.midleft
        
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks() 