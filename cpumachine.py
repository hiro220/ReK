# coding;utf-8

from machine import Machine
import pygame
from define import *
from gun import *
from cpumove import *

img_path = "img/cpu/"

#comment
class CpuMachine(Machine):
    killed_count = 0
    def __init__(self, hp, x, y, image, players, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        super().__init__(hp, x, y, image, players, score, money, data) #superクラス(machine)を呼び出す
        self.dx, self.dy = 5, 5                           #bulletの移動量を指定する
        self.x, self.y = x, y                             #機体自身の位置を入力
        self.gun_start = R_time.get_ticks()          #createCPUが呼ばれた時のクロック数を入力

    def death(self):
        CpuMachine.killed_count += 1

#これはデバック用のCPUです。
class cpu0(CpuMachine): 
    def __init__(self, x, y, players, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load(img_path+"cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(1, x, y, image, players, score, money, data)         #superクラス(CpuMachine)を呼び出す
        self.dx, self.dy = 5, 5                                  #機体自身の位置を入力　　
        self.gun = Beam_Gun(self.machines, self, -1, 270)          #machineクラスのself.gunを上書きする
        self.count = 0                                           #このクラスupdataが呼ばれた回数を保存する
    
    def update(self):
        if 0 <= self.count <= 150:
            self.dx, self.dy = -2.5, 0
            self.rect.move_ip(self.dx, self.dy)                  #機体の移動方向と速度を入力
            self.count += 1
        x, y = self.rect.midleft                                 #機体自身の位置を入力
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load(img_path+"cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = 5, 5
        self.Sample1 = Sample1()
        self.gun = Beam_Gun(self.machines, self, -1, 0)
    
    def update(self):
        self.dx, self.dy = Sample1.move()
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu2(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load(img_path+"cpu2.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = 5, 5
        self.Sample2 = Sample2()
        self.gun = Reflection_Gun(self.machines, self, 10)
    
    def update(self):
        self.dx, self.dy = self.Sample2.move()
        self.rect.move_ip(self.dx,self.dy)
        x, y = self.rect.midleft
        
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks() 

class cpu3(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load(img_path+"cpu3.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = 5, 5
        self. count = 0
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


class cpu4(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu4.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -1, 0
        self.Sample3 = Sample3()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample3.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu5(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu5.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -5, -2
        self.Sample4 = Sample4()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample4.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu6(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu6.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -2, 0
        self.Sample5 = Sample5()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample5.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu7(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu6.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -2, 0
        self.Sample6 = Sample6()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample6.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu8(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu6.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -2, 0
        self.Sample7 = Sample7()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample7.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu9(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu6.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -2, 0
        self.Sample8 = Sample8()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample8.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()

class cpu10(CpuMachine):
    def __init__(self, x, y, players, score, money, data):
        image = pygame.image.load(img_path+"cpu6.png").convert_alpha()
        super().__init__(1, x, y, image, players, score, money, data)
        self.dx, self.dy = -2, 0
        self.Sample9 = Sample9()
        self.gun = Opposite_Gun(self.machines, self, 10)

    def update(self):
        self.dx, self.dy = self.Sample9.move(self.dx, self.dy)
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if R_time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = R_time.get_ticks()