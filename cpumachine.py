# coding;utf-8

from machine import Machine
import pygame

class CpuMachine(Machine):
    def __init__(self, x, y, players):
        """引数は、初期位置(x, y)、弾の当たり判定対象となるプレイヤーの機体グループ"""
        
        image = pygame.image.load("img/cpu.png").convert_alpha()
        super().__init__(1, x, y, image, players)
        self.dx, self.dy = 5, 5