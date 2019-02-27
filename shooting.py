#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from stage import *

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # ウィンドウを960×600で作成する
        
    def do(self):
        stage = Stage(self.screen, 1200)
        result = stage.loop()
        if result == EXIT:
            pygame.quit()

if __name__=='__main__':
    game = Main()
    game.do()