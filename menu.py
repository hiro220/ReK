import pygame
from pygame.locals import *
import sys
import time
from define import *

class Menu:
    
    def __init__(self, screen):
        self.screen = screen

        self.stage_num = 1
        self.select_num = 0
        self.back_num = 0
        self.shop_num = 0

        StageSelect_font = pygame.font.Font("freesansbold.ttf", 55)
        LeftArrow_font = pygame.font.Font("freesansbold.ttf", 150)      
        RightArrow_font = pygame.font.Font("freesansbold.ttf", 150)
        Stage1_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage2_font = pygame.font.Font("freesansbold.ttf", 45)
        Stage3_font = pygame.font.Font("freesansbold.ttf", 45)
        back_font = pygame.font.Font("freesansbold.ttf", 55)
        shop_font = pygame.font.Font("freesansbold.ttf", 55)

        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255)) 
        self.RightArrow_text = RightArrow_font.render(">", True, (255,255,255))
        self.LeftArrow_text = LeftArrow_font.render("<", True, (255,255,255))
        self.Stage1_text = Stage1_font.render("Stage1", True, (255,255,255))
        self.Stage2_text = Stage2_font.render("Stage2", True, (255,255,255))
        self.Stage3_text = Stage3_font.render("Stage3", True, (255,255,255))
        self.back_text = back_font.render("Back", True, (255,255,255))
        self.shop_text = shop_font.render("Shop", True, (255,255,255))


    def draw(self):

        while True:

            self.screen.blit(self.StageSelect_text, [105, 5])     #テキストStageSelectを描画
            self.screen.blit(self.RightArrow_text, [965, 220])  #テキスト ＞ を描画
            self.screen.blit(self.LeftArrow_text, [105, 220])     #テキスト ＞ を描画
            self.screen.blit(self.back_text,[900, 5])
            self.screen.blit(self.shop_text,[600, 5])

            self.Select_Stage()     #ステージ選択処理

            if self.back_num == 1:
                pygame.draw.rect(self.screen,(255,255,0),Rect(890,3,155,60),5)
            
            if self.shop_num == 1:
                pygame.draw.rect(self.screen,(255,255,0),Rect(593,3,155,60),5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN:
                        if self.back_num == 1:
                            return None, "0"
                        elif self.shop_num == 1:
                            return None, "1"
                        return self.Return_Stage()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((0,0,0))
            
    
    def Select_Stage(self):         #選択しているステージを描画
        color = [(0,0,255),(0,255,0), (255,0,0)]
        stage = [self.Stage1_text, self.Stage2_text, self.Stage3_text]
        self.screen.blit(stage[self.stage_num-1], [210, 80])
        pygame.draw.rect(self.screen,color[self.stage_num-1],Rect(200,70,760,460),5)
    
    def Key_Event(self,event):
        if self.back_num == 0 and self.shop_num == 0:
            if event.key == K_RIGHT:        #→が押されたなら次のステージへ移動
                if self.stage_num != 3:
                    self.stage_num += 1
            elif event.key == K_LEFT:       #←矢印が押されたなら前のステージへ移動
                if self.stage_num != 1:
                    self.stage_num -= 1
        elif self.back_num == 1:
            if event.key == K_LEFT:
                self.back_num = 0
                self.shop_num = 1
        elif self.shop_num == 1:
            if event.key == K_RIGHT:
                self.shop_num = 0
                self.back_num = 1

        if event.key == K_UP:
            self.shop_num = 1
        elif event.key == K_DOWN:
            self.back_num = 0
            self.shop_num = 0
    
    def Return_Stage(self):
        stage = [Stage1, Stage2, Stage3]
        return self.stage_num, stage[self.stage_num-1]