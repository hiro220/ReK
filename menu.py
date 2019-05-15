import pygame
from pygame.locals import *
import sys
import time
from define import *

class Menu:
    
    def __init__(self, screen):
        self.screen = screen
        self.stage_num = 1     #現在選択しているステージ

        StageSelect_font = pygame.font.Font("freesansbold.ttf", 55)
        LeftArrow_font = pygame.font.Font("freesansbold.ttf", 150)      
        RightArrow_font = pygame.font.Font("freesansbold.ttf", 150)
        Stage1_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage2_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage3_font = pygame.font.Font("freesansbold.ttf", 45)


        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255))    #テキストStageSelect
        self.RightArrow_text = RightArrow_font.render(">", True, (255,255,255))     #選択矢印 ＞
        self.LeftArrow_text = LeftArrow_font.render("<", True, (255,255,255))       #選択矢印 ＞
        self.Stage1_text = Stage1_font.render("Stage1", True, (255,255,255))    #テキストStage1
        self.Stage2_text = Stage2_font.render("Stage2", True, (255,255,255))    #テキストStage2
        self.Stage3_text = Stage3_font.render("Stage3", True, (255,255,255))    #テキストStage3

    def draw(self):

        while True:
            self.screen.blit(self.StageSelect_text, [5, 5])     #テキストStageSelectを描画
            self.screen.blit(self.RightArrow_text, [865, 220])  #テキスト ＞ を描画
            self.screen.blit(self.LeftArrow_text, [5, 220])     #テキスト ＞ を描画

            self.Select_Stage()     #ステージ選択処理

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN:
                        return self.Return_Stage()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((0,0,0))
    
    def Select_Stage(self):         #選択しているステージを描画
        if self.stage_num == 1:
            self.screen.blit(self.Stage1_text, [110, 80])
            pygame.draw.rect(self.screen,(0,0,255),Rect(100,70,760,460),5)
        elif self.stage_num == 2:
            self.screen.blit(self.Stage2_text, [110, 80])
            pygame.draw.rect(self.screen,(0,255,0),Rect(100,70,760,460),5)
        elif self.stage_num == 3:
            self.screen.blit(self.Stage3_text, [110, 80])
            pygame.draw.rect(self.screen,(255,0,0),Rect(100,70,760,460),5)
    
    def Key_Event(self,event):
        if event.key == K_RIGHT:        #→が押されたなら次のステージへ移動
            if self.stage_num != 3:
                    self.stage_num += 1
        elif event.key == K_LEFT:       #←矢印が押されたなら前のステージへ移動
            if self.stage_num != 1:
                    self.stage_num -= 1
    
    def Return_Stage(self):
        if self.stage_num == 1:
            return Stage1
        elif self.stage_num == 2:
            return Stage2
        elif  self.stage_num == 3:
            return Stage3