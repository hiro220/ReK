# coding;utf-8

from machine import Machine
import pygame

class CpuMachine(Machine):
    def __init__(self, hp, x, y, image, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        super().__init__(hp, x, y, image, players)
        self.dx, self.dy = 5, 5
    
class cpu(CpuMachine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""

        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5
    
    def update(self):
        self.rect.move_ip(-2.5,0)

class cpu2(CpuMachine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5
    
    def update(self):
        self.rect.move_ip(-2.5,0)