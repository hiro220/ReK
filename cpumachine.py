# coding;utf-8

from machine import Machine
import pygame

class CpuMachine(Machine):
    def __init__(self, hp, x, y, image, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        super().__init__(hp, x, y, image, players)
        self.dx, self.dy = 5, 5
        self.gun_start = pygame.time.get_ticks()
    
class cpu(CpuMachine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5
    
    def update(self):
        self.rect.move_ip(-2.5,0)
        x, y = self.rect.midright
        x -= 90
        if pygame.time.get_ticks() - self.gun_start >= 600:
            super().shoot2(x, y)
            self.gun_start = pygame.time.get_ticks()

class cpu2(CpuMachine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5
        self.count = 0
    
    def update(self):
        if 0 <= self.count <= 14:
            self.rect.move_ip(-2.5,3)
            self.count += 1
        elif 15 <= self.count <= 30:
            self.rect.move_ip(-2.5,-3)
            self.count += 1
            if self.count == 31:
                self.count = 0

class cpu3(CpuMachine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5
        self.count = 0

    def update(self):
        if 0 <= self.count <= 150:
            self.rect.move_ip(-2.5,0)
            self.count += 1 