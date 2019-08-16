import pygame
from pygame.locals import *
from define import *
from listbox import ListBox

class Equipment:

    def __init__(self, screen, data):
        self.gun_data = data["gun_data"]
        self.equipment = data["equip"]
        self.screen = screen
        self.change_gun = 0             # 現在選択している装備場所
        self.back = False               # 一つ前の画面にもどるか
        self.screen_info = pygame.font.Font("freesansbold.ttf" ,70).render("Equip", True, (255,255,255))
        self.back_info = pygame.font.Font("freesansbold.ttf" ,50).render("'Q' : Back", True, (255,255,255))
        texts = [data["name"] for data in self.gun_data.values()]
        self.listbox = ListBox(self.screen, 80, 150, 300, 250, texts, font_size=40, target=True)
        self.listbox.set_selectable([data["own"]==1 for data in self.gun_data.values()])
    
    def do(self):
        while True:
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        # 内部処理
        self.listbox()
        for event in pygame.event.get():
            select = self.listbox.process(event)
            if select != None:
                self.equip(select)
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.change_gun += 1
                elif event.key == K_LEFT:
                    self.change_gun -= 1
                elif event.key == K_q:
                    return BACK
                self.change_gun = (self.change_gun + 3) % 3
                
        return CONTINUE

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [WIDTH-self.back_info.get_rect().right-20, 20])
        pygame.draw.rect(self.screen, (255,255,255), Rect(700, HEIGHT-150, 350, 100))
        
        self.listbox.color_reset()
        self.listbox.set_color(self.equipment, (105,105,255))
        self.listbox.draw()

        # 装備中の銃情報の表示
        for i, data in enumerate(self.equipment):
            color = (255,0,0) * (i == self.change_gun) or (0,)*3
            pygame.draw.rect(self.screen, color, [730+95*i, HEIGHT-145, 90, 90], 2+(i==self.change_gun))
            if data == -1:
                continue
            text = pygame.font.Font("freesansbold.ttf", 80).render(str(data), True, (0,0,0))
            self.screen.blit(text, [755+95*i, HEIGHT-135])
        pygame.display.update()

    def check(self, select):
        # 装備変更確認
        for i, gun in enumerate(self.equipment):
            if gun == select:
                if i == 0:
                    return False
                self.equipment[i] = -1
        return True

    def equip(self, select):
        # 選択した銃を装備する。
        if self.check(select):
            equipment = self.equipment
            equipment[self.change_gun] = select