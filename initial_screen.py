import pygame
from pygame.locals import *
import sys
from define import *

class Initial_Screen:
    def __init__(self):
        title_font = pygame.font.Font("freesansbold.ttf", 55)
        font = pygame.font.Font("freesansbold.ttf", 25)
        self.title_text = title_font.render("ReK", True, (255,255,255))        #タイトルテキストReK
        self.game_text = font.render("START GAME", True, (255,255,255))   #テキストSTART_GAME
        self.help_text = font.render("Help", True, (255,255,255))         #テキストHelp
        self.end_text = font.render("End", True, (255, 255, 255))          #テキストEnd
        self.choice_text = font.render("->", True, (255,255,255))       #選択矢印->
        self.select_num = START_GAME        #現在選択しているモード


    def draw(self, screen):
        while True:
            screen.blit(self.title_text, [530, 200])     # タイトルReKを描画
            screen.blit(self.game_text, [530, 300])      # START GAMEを描画
            screen.blit(self.help_text, [530, 330])      # Helpを描画
            screen.blit(self.end_text, [530, 360])
            self.Draw_Key(screen)        #選択矢印を描画

            pygame.display.update()     #画面更新

            for event in pygame.event.get():
                if event.type == KEYDOWN:  
                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN:
                        return self.select_num
                elif event.type == QUIT:         #閉じるボタンが押されたならゲームを終了する
                    return EXIT

            screen.fill((0,0,0))       #画面を黒で塗りつぶす

    def Draw_Key(self, screen):
         if self.select_num == START_GAME:                         
            screen.blit(self.choice_text, [505, 300])    #選択矢印->をSTART GAMEの横へ描画
         elif self.select_num == Help:                       
            screen.blit(self.choice_text, [505, 330])    #選択矢印->をHelpの横へ描画
         elif self.select_num == End:
            screen.blit(self.choice_text, [505, 360])    #選択矢印->をEndの横へ描画

    def Key_Event(self, event):     
            if event.key == K_UP:       #↑が押されたとき選択矢印->を上方向に移動（但し、一番上なら一番下に移動）
                if self.select_num == START_GAME:
                    self.select_num = End
                else:
                    self.select_num -= 1     
            if event.key == K_DOWN:     #↓が押されたとき選択矢印->を下方向に移動（但し、一番下なら一番上に移動）
                if self.select_num == End:
                    self.select_num  = START_GAME
                else:
                    self.select_num += 1