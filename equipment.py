import pygame
from pygame.locals import *
from define import *
from listbox import ListBox
from popupwindow import PopupWindow

class Equipment:

    def __init__(self, screen, data):
        self.gun_data = data["gun_data"]
        self.equipment = data["equip"]
        self.chip_data = data["chip_data"]
        self.chip = data["chip"]
        self.screen = screen
        self.change_gun = 0             # 現在選択している装備場所
        self.change_chip = 0
        self.back = False               # 一つ前の画面にもどるか
        self.screen_info = pygame.font.Font("font/freesansbold.ttf" ,70).render("Equip", True, (255,255,255))
        self.back_info = pygame.font.Font("font/freesansbold.ttf" ,50).render("'Q' : Back", True, (255,255,255))
        self.listbox_id = 0
        texts = [data["name"] for data in self.gun_data.values()]
        equip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Gun", title_size=60)
        equip_listbox.set_selectable([data["own"]==1 for data in self.gun_data.values()])
        texts = [data['name'] for data in self.chip_data.values()]
        chip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Chip", title_size=60)
        chip_listbox.set_selectable([data["num"] > 0 for data in self.chip_data.values()])
        self.listboxes = [equip_listbox, chip_listbox]
        self.listbox = self.listboxes[self.listbox_id]
        self.clock = pygame.time.Clock()
    
    def do(self):
        while True:
            self.clock.tick(30)
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
                if self.listbox_id == 0:
                    self.equip_key(event.key)
                elif self.listbox_id == 1:
                    self.chip_key(event.key)
                if event.key == K_q:
                    return BACK
                elif event.key == K_c:
                    self.listbox_id ^= 1
                    self.listbox = self.listboxes[self.listbox_id]
                
        return CONTINUE

    def equip_key(self, key):
        if key == K_RIGHT:
            self.change_gun += 1
        elif key == K_LEFT:
            self.change_gun -= 1
        self.change_gun = (self.change_gun + 3) % 3

    def chip_key(self, key):
        if key == K_RIGHT:
            self.change_chip += 1
        elif key == K_LEFT:
            self.change_chip -= 1
        self.change_chip = (self.change_chip + 6) % 6

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [WIDTH-self.back_info.get_rect().right-20, 20])
        
        self.listbox.color_reset()
        if self.listbox_id == 0:
            self.listbox.set_color(self.equipment, (105,105,255))
        elif self.listbox_id == 1:
            self.listbox.set_color(self.chip, (105, 105, 255))
        self.listbox.draw()

        if self.listbox_id == 0:
            self.draw_equip()
        elif self.listbox_id == 1:
            self.draw_chip()

        pygame.display.update()

    def draw_equip(self):
        # 装備中の銃情報の表示
        pygame.draw.rect(self.screen, (255,255,255), Rect(700, HEIGHT-150, 340, 100))
        for i, data in enumerate(self.equipment):
            color = (255,0,0) * (i == self.change_gun) or (0,)*3
            pygame.draw.rect(self.screen, color, [730+95*i, HEIGHT-145, 90, 90], 2+(i==self.change_gun))
            if data == -1:
                continue
            text = pygame.font.Font("font/freesansbold.ttf", 80).render(str(data), True, (0,0,0))
            self.screen.blit(text, [755+95*i, HEIGHT-135])

    def draw_chip(self):
        pygame.draw.rect(self.screen, (255,255,255), Rect(500, HEIGHT-150, 625, 100))
        for i, data, in enumerate(self.chip):
            color = (255,0,0) * (i == self.change_chip) or (0,)*3
            pygame.draw.rect(self.screen, color, [530+95*i, HEIGHT-145, 90, 90], 2+(i==self.change_chip))
            if data == -1:
                continue
            text = pygame.font.Font("font/freesansbold.ttf", 80).render(str(data), True, (0,0,0))
            self.screen.blit(text, [755+95*i, HEIGHT-135])


    def check(self, select):
        # 装備変更確認
        for i, gun in enumerate(self.equipment):
            if gun == select:
                if i == 0:
                    return False
                while True:
                    if PopupWindow(self.screen, "すでに装備している枠から変更しますか？", \
                                   ["変更する", "変更しない"]).loop() == 0:
                        break
                    else:
                        return False
                self.equipment[i] = -1
        return True

    def chip_chack(self, select):
        chip_data = self.chip_data[select]
        # 空いている枠の数を取得
        empty_num = self.chip.count(-1)
        # 装備する枠が残っているか
        if chip_data['equip_size'] > empty_num:
            return False
        # 装備可能上限まで装備しているか
        equip_num = self.chip.count(select)
        if chip_data['equip_max'] == equip_num:
            return False
        return True

    def equip(self, select):
        # 選択した銃を装備する。
        if self.check(select):
            equipment = self.equipment
            equipment[self.change_gun] = select

    def set_chip(self, select):
        if self.chip_chack(select):
            self.chip[self.change_chip] = select