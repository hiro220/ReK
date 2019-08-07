import pygame
from pygame.locals import *
from define import *
from equipment import Equipment

class Menu:
    
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data

        self.stage_num = 1
        self.select_num = 0
        self.option_num = 0


        StageSelect_font = pygame.font.Font("freesansbold.ttf", 55)
        Arrow_font = pygame.font.Font("freesansbold.ttf", 150)
        Stage_font = pygame.font.Font("freesansbold.ttf", 45)
        option_font = pygame.font.Font("freesansbold.ttf", 55)

        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255)) 
        self.RightArrow_text = Arrow_font.render(">", True, (255,255,255))
        self.LeftArrow_text = Arrow_font.render("<", True, (255,255,255))
        # ステージのテキスト情報をリストにする
        self.stage_text = []
        for i in range(3):
            text = "Stage" + str(i+1)
            self.stage_text.append(Stage_font.render(text, True, (255,255,255)))
        # オプションのテキスト情報をリストにする
        self.oprion_text = []
        for i, option in enumerate(("Back", "Shop", "Equip")):
            self.oprion_text.append(option_font.render(option, True, (255,255,255)))

    def draw(self):

        while True:

            self.screen.blit(self.StageSelect_text, [105, 5])     #テキストStageSelectを描画
            self.screen.blit(self.RightArrow_text, [965, 220])  #テキスト ＞ を描画
            self.screen.blit(self.LeftArrow_text, [105, 220])     #テキスト ＞ を描画
            for i, option in enumerate(self.oprion_text):
                self.screen.blit(option,[900-200*i, 5])

            self.Select_Stage()     #ステージ選択処理

            # オプションが選択状態のとき、選択中のテキストに応じた枠を作成する
            if self.option_num:
                text_size = self.oprion_text[self.option_num-1].get_rect().right
                pygame.draw.rect(self.screen,(255,255,0),Rect(890-(self.option_num-1)*200,3,text_size+20,60),5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN:
                        if self.option_num == 1:
                            return None, None
                        elif self.option_num == 2:
                            pass
                            break
                        elif self.option_num == 3:
                            Equipment(self.screen, self.data).do()
                            break
                        return self.Return_Stage()
                if event.type == QUIT:
                    return EXIT, None
            
            self.screen.fill((0,0,0))
            
    
    def Select_Stage(self):
        #選択しているステージを描画
        color = [(0,0,255),(0,255,0), (255,0,0)]
        self.screen.blit(self.stage_text[self.stage_num-1], [210, 80])
        pygame.draw.rect(self.screen,color[self.stage_num-1],Rect(200,70,760,460),5)
    
    def Key_Event(self,event):
        if event.key == K_RIGHT:        #→が押されたなら次のステージへ移動
            if self.option_num:
                self.option_num -= (1 < self.option_num <= 3)
            elif self.stage_num != 3:
                self.stage_num += 1
        elif event.key == K_LEFT:       #←矢印が押されたなら前のステージへ移動
            if self.option_num:
                self.option_num += (1<=self.option_num<3)
            elif self.stage_num != 1:
                self.stage_num -= 1
        if event.key == K_UP:
            self.option_num = int(self.option_num==0)
        elif event.key == K_DOWN:
            self.option_num = 0
    
    def Return_Stage(self):
        stage = [Stage1, Stage2, Stage3]
        return self.stage_num, stage[self.stage_num-1]