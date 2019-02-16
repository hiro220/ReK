# coding;utf-8

from machine import Machine
import pygame

class CpuMachine(Machine):
    def __init__(self, x, y, players):
        img = pygame.image.load("img/cpu.png").convert_alpha()
        self.image = img
        super().__init__(1, x, y, img, players)
        self.dx, self.dy = 5, 5