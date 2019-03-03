#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from stage import *
from initial_screen import *
from menu import *


class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # ウィンドウを960×600で作成する
        
    def do(self):
        while True:
            init_screen = Initial_Screen()
            init_num = init_screen.draw(self.screen)

            if init_num == START_GAME:
                menu = Menu(self.screen)
                stage_num = menu.draw()
                
                if stage_num == 1:
                    stage = Stage(self.screen, "stage/stage1.txt")
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()
                elif stage_num == 2:
                    stage = Stage(self.screen, "stage/stage1.txt")
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()
                elif stage_num == 3:
                    stage = Stage(self.screen, "stage/stage1.txt")
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()                    
            elif init_num == Help:
                print("help menu")

if __name__=='__main__':

    game = Main()
    game.do()