#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from stage import *
from initial_screen import *
from menu import *
import pygame.mixer

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # ウィンドウを960×600で作成する
        
    def do(self):
         while True:
            init_screen = Initial_Screen()              #初期画面の描画              
            init_num = init_screen.draw(self.screen)    

            if init_num == START_GAME:      #選択したモードがSTART GAMEならメニュー画面に移動

                menu = Menu(self.screen)    #メニュー画面の描画
                stage_num = menu.draw()
                
                if stage_num == 1:                                   #選択したステージでゲームを開始
                    stage = Stage(self.screen, "stage/stage1.txt")
                    pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
                    pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()
                elif stage_num == 2:
                    stage = Stage(self.screen, "stage/stage2.txt")
                    pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
                    pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()
                elif stage_num == 3:
                    stage = Stage(self.screen, "stage/stage3.txt")
                    pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
                    pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
                    result = stage.loop()
                    if result == EXIT:
                        pygame.quit()
                        sys.exit()                    
            elif init_num == Help:      #選択したモードがHelpならHelp画面に移動
                print("help menu")
                
                while  True:
                        menu = Menu(self.screen)    #メニュー画面の描画
                        stageTxt = menu.draw()
                        self.Stage_draw(stageTxt)                       
            elif init_num == Help:
                print("help")

    def Stage_draw(self, stageTxt):
        stage = Stage(self.screen, "stage/" + stageTxt)
        pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
        pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
        result = stage.loop()
        if result == EXIT:
            pygame.quit()
            sys.exit()
            

                
if __name__=='__main__':

    game = Main()
    game.do()