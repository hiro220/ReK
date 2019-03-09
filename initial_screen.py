import pygame
from pygame.locals import *
import sys
from define import *

class Initial_Screen:
    def __init__(self):
        title_font = pygame.font.Font("freesansbold.ttf", 55)
        game_font = pygame.font.Font("freesansbold.ttf", 25)
        help_font = pygame.font.Font("freesansbold.ttf", 25)
        choice_font = pygame.font.Font("freesansbold.ttf", 25)
        self.title_text = title_font.render("ReK", True, (255,255,255))        #タイトルテキストReK
        self.game_text = game_font.render("START GAME", True, (255,255,255))   #テキストSTART_GAME
        self.help_text = help_font.render("Help", True, (255,255,255))         #テキストHelp
        self.choice_text = choice_font.render("->", True, (255,255,255))       #選択矢印->


    def draw(self, screen):
        select_num = 0         #現在選択しているモード

        while True:
            screen.blit(self.title_text, [430, 200])     # タイトルReKを描画
            screen.blit(self.game_text, [430, 300])      # START GAMEを描画
            screen.blit(self.help_text, [430, 330])      # Helpを描画

            if select_num == START_GAME:                         
                screen.blit(self.choice_text, [405, 300])    #選択矢印->をSTART GAMEの横へ描画
            elif select_num == Help:                       
                screen.blit(self.choice_text, [405, 330])    #選択矢印->をHelpの横へ描画

            pygame.display.update()     #画面更新

            for event in pygame.event.get():
                if event.type == KEYDOWN:       
                    if event.key == K_UP:       #↑が押されたとき選択矢印->を上方向に移動（但し、一番上なら一番下に移動）
                        if select_num == START_GAME:
                            select_num = Help
                        else:
                            select_num -= 1     
                    if event.key == K_DOWN:     #↓が押されたとき選択矢印->を下方向に移動（但し、一番下なら一番上に移動）
                        if select_num == Help:
                            select_num  = START_GAME
                        else:
                            select_num += 1
                    if event.key == K_SPACE:    #スペースが押されたなら、現在選択しているモードの値を返す
                        return select_num
                    if event.key == K_ESCAPE:   #Escが押されたならゲームを終了する
                        pygame.quit()
                        sys.exit()
                        
            screen.fill((0,0,0))       #画面を黒で塗りつぶす
