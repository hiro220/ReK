# coding:utf-8
import pygame
from pygame.locals import *

class ReK_time:
    time = 0
    def __init__(self):
        ReK_time.time = pygame.time.get_ticks()
        self.stoptime = 0

    def get_ticks(self):
        return  pygame.time.get_ticks() - ReK_time.time - self.stoptime

    def stop(self):
        self.stoptime = pygame.time.get_ticks() - ReK_time.time

    def start(self):
        self.stoptime = 0

    def restart(self):
        ReK_time.time = pygame.time.get_ticks()