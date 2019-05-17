# coding:utf-8
import pygame
from pygame.locals import *

class ReK_time:
    def __init__(self):
        self.stop_time = 0
        self.pause_time = 0

    def get_ticks(self):
        return pygame.time.get_ticks() - self.pause_time

    def stop(self):
        self.stop_time = pygame.time.get_ticks()
    
    def restart(self):
        self.pause_time += pygame.time.get_ticks() - self.stop_time