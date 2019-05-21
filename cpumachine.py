# coding;utf-8

from machine import Machine
import pygame
from gun import *


#comment
class CpuMachine(Machine):
    def __init__(self, hp, x, y, image, players, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        super().__init__(hp, x, y, image, players, score)
        self.dx, self.dy = 5, 5
        self.x, self.y = x, y
        self.gun_start = pygame.time.get_ticks()

#これはデバック用のCPUです。
class cpu0(CpuMachine): 
    def __init__(self, x, y, players, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.dx, self.dy = 5, 5
        self.gun = Beam_Gun(self.machines, self.rect, 1)
        self.count = 0
    
    def update(self):
        if 0 <= self.count <= 150:
            self.dx, self.dy = -2.5, 0
            self.rect.move_ip(self.dx, self.dy)
            self.count += 1
        x, y = self.rect.midleft
        super().shoot(x, y)

    
class cpu(CpuMachine):
    def __init__(self, x, y, players, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.dx, self.dy = 5, 5
        self.gun = Opposite_Gun(self.machines, self.rect, 10)
    
    def update(self):
        self.dx, self.dy = -2.5, 0
        self.rect.move_ip(self.dx, self.dy)
        x, y = self.rect.midleft
        if pygame.time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = pygame.time.get_ticks()

class cpu2(CpuMachine):
    def __init__(self, x, y, players, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.dx, self.dy = 5, 5
        self.count = 0
        self.gun = Reflection_Gun(self.machines, self.rect, 10)
    
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
        if pygame.time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = pygame.time.get_ticks() 

class cpu3(CpuMachine):
    def __init__(self, x, y, players, score):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players, score)
        self.dx, self.dy = 5, 5
        self.count = 0
        self.gun = Tracking_Gun(self.machines, self.rect, 10)

    def update(self):
        if 0 <= self.count <= 150:
            self.dx, self.dy = -2.5, 0
            self.rect.move_ip(self.dx, self.dy)
            self.count += 1

        x, y = self.rect.midleft
        if pygame.time.get_ticks() - self.gun_start >= 1200:
            super().shoot(x, y)
            self.gun_start = pygame.time.get_ticks() 
