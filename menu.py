import pygame
from pygame.locals import *
from define import *
from equipment import Equipment
from listbox import ListBox
from popupwindow import PopupWindow
from messagebox import MessageBox

class Menu:
    
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data

        self.stage_num = 1
        self.select_num = 0
        self.option_num = 0
        
        StageSelect_font = pygame.font.Font("font/freesansbold.ttf", 55)
        Arrow_font = pygame.font.Font("font/freesansbold.ttf", 100)
        Stage_font = pygame.font.Font("font/freesansbold.ttf", 45)

        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255)) 
        self.RightArrow_text = Arrow_font.render(">", True, (255,255,255))
        self.LeftArrow_text = Arrow_font.render("<", True, (255,255,255))
        self.RightArrow_text = pygame.transform.rotate(self.RightArrow_text, 90)
        self.LeftArrow_text = pygame.transform.rotate(self.LeftArrow_text, 90)
        # ステージのテキスト情報をリストにする
        self.stage_text = []
        for i in range(3):
            text = "Stage" + str(i+1)
            self.stage_text.append(Stage_font.render(text, True, (255,255,255)))

        # リストボックスの設定
        self.option_listbox = ListBox(self.screen, 50, 80, 250, 200, ['Back', 'Shop', 'Equip'], font_size=55, title="Menu")
        self.option_listbox.set_selectable([True, True, True])
        self.file_listbox = ListBox(self.screen, 950, 80, 100, 400, ["Stage1"], title="File")
        self.file_listbox.set_selectable([True])
        self.file_listbox()
        self.file_id = None

        # メッセージボックスの設定
        self.messagebox = MessageBox(self.screen, 130, 540, 900,  outline_color=(180,180,180), select='random')
        with open('data/message.txt', 'r') as fp:
            self.messagebox += fp.readlines()

        self.clock = pygame.time.Clock()

    def draw(self):
        while True:
            self.clock.tick(30)
            # リストボックスの描画
            self.option_listbox.draw(False)
            self.file_listbox.draw()
            self.Select_Stage(self.file_id)     #ステージ選択処理
            self.messagebox.draw()
            pygame.display.update()
            for event in pygame.event.get():
                # リストボックスに入力
                file_id = self.file_listbox.process(event)
                option_num = self.option_listbox.process(event)
                if event.type == KEYDOWN:
                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN and self.select_num == 1 and self.file_id != None:
                        return self.Return_Stage()
                if event.type == QUIT:
                    return EXIT, None

                if file_id != None:
                    # ファイルが選択されたとき
                    self.file_id = file_id
                    self.select_num += 1
                    # file_listboxからターゲットを外す
                    self.file_listbox.process(event)

                if option_num != None:
                    # オプションが選択されたとき
                    if option_num == 0:
                        return None, '0'
                    elif option_num == 1:
                        return None, '1'
                    elif option_num == 2:
                        if Equipment(self.screen, self.data).do() == EXIT:
                            return EXIT, None
                        break
                
            self.screen.fill((0,0,0))
            
    
    def Select_Stage(self, file_id):
        #選択しているステージを描画
        color = (self.select_num==1)*(255,100,100) or (100,100,100)
        pygame.draw.rect(self.screen,color,Rect(350,80,550,450))
        self.screen.blit(self.StageSelect_text, [350, 20])     #テキストStageSelectを描画
        # ステージファイルが選択されていないとき、ステージを表示しない
        if file_id != None:
            color = [(0,0,255),(0,255,0), (255,0,0)]
            self.screen.blit(self.stage_text[self.stage_num-1], [410, 190])
            pygame.draw.rect(self.screen,color[self.stage_num-1],Rect(400,180,450,250),5)
            self.screen.blit(self.RightArrow_text, [575, 120])  #テキスト ＞ を描画
            self.screen.blit(self.LeftArrow_text, [575, 430])     #テキスト ＞ を描画
    
    def Key_Event(self,event):
        # 左右キーで大枠の選択
        if event.key == K_RIGHT:
            self.select_num -= 1
        elif event.key == K_LEFT:
            self.select_num += 1
        self.select_num = (self.select_num+3) % 3
        # リストボックスが選択されているとき、ターゲットする
        if self.select_num == 0:
            self.file_listbox()
        elif self.select_num == 2:
            self.option_listbox()
        # ステージ選択のとき、上下キーでステージ選択の移動
        if event.key == K_UP:
            self.stage_num += (self.select_num==1)
        elif event.key == K_DOWN:
            self.stage_num -= (self.select_num==1)
        stage_size = len(self.stage_text)
        self.stage_num = (self.stage_num+stage_size) % stage_size
    
    def Return_Stage(self):
        stage = [Stage1, Stage2, Stage3]
        return self.stage_num, stage[self.stage_num-1]