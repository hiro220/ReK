#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from stage import *
from initial_screen import *
from menu import *
from  score import *
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
  
                while True:
                    menu = Menu(self.screen)    #メニュー画面の描画
                    stageTxt = menu.draw()
                    if stageTxt == "0":
                        break
                    self.Stage_draw(stageTxt)                
            elif init_num == Help:      #選択したモードがHelpならHelp画面に移動
                print("help menu")
            elif init_num == End:
                pygame.quit()
                sys.exit()

    def Stage_draw(self, stageTxt):
        stage = Stage(self.screen, "stage/" + stageTxt)
        pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
        pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
        result = stage.loop()
        if result[0] == EXIT:
            pygame.quit()
            sys.exit()
        elif result[0] == RETIRE:
            return
        select_num = self.StageResult_draw(result)
        return

    def StageResult_draw(self, result):
        """ステージ結果画面を描画する"""
        self.screen.fill((0,0,0))

        Score_font = pygame.font.Font("freesansbold.ttf", 50)
        Enter_font = pygame.font.Font("freesansbold.ttf", 20)

        Score_text = Score_font.render("SCORE: " + str(result[1]), True, (255,255,255))
        Enter_text = Enter_font.render("ENTER:RETURN", True, (255,255,255))

        self.screen.blit(Score_text, [360, 470])
        self.screen.blit(Enter_text, [5, 5])

        if result[0] ==  GAMECLEAR:
            image = pygame.image.load("img/gameclear.jpg").convert_alpha()
            self.screen.blit(image, [155, 50])    
        elif result[0] == GAMEOVER:
            image = pygame.image.load("img/gameover.jpg").convert_alpha()
            self.screen.blit(image, [170, 10])

        while True:
            pygame.display.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return 
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


if __name__=='__main__':

    game = Main()
    game.do()
