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
        self.back_info = pygame.font.Font("font/ShipporiMincho-TTF-Regular.ttf" ,50).render("'Q' : 戻る", True, (255,255,255))
        self.change_info = pygame.font.Font("font/ShipporiMincho-TTF-Regular.ttf" ,50).render("'C' : 切り替え", True, (255,255,255))
        self.listbox_id = 0
        texts = [data["name"] for data in self.gun_data.values()]
        equip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Gun", title_size=60)
        equip_listbox.set_selectable([data["own"]==1 for data in self.gun_data.values()])
        texts = [data['name'] for data in self.chip_data.values()]
        chip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Chip", title_size=60)
        chip_listbox += ['remove', 'remove ALL']
        self.listboxes = [equip_listbox, chip_listbox]
        self.listbox = self.listboxes[self.listbox_id]
        self.clock = pygame.time.Clock()
    
    def do(self):
        while True:
            self.clock.tick(30)
            request = self.process()
            self.listbox()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        # 内部処理
        select = [data["num"] > 0 for data in self.chip_data.values()] \
                    + [self.chip[self.change_chip]!=-1, self.chip!=[-1]*6]
        self.listboxes[1].set_selectable(select)
        for event in pygame.event.get():
            select = self.listbox.process(event)
            if select != None:
                if self.listbox_id == 0:
                    self.equip(select)
                else:
                    self.set_chip(select)
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if self.listbox_id == 0:
                    self.equip_key(event.key)
                else:
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
        self.screen.blit(self.back_info, [850, 20])
        self.screen.blit(self.change_info, [850, 90])
        
        self.listbox.color_reset()
        if self.listbox_id == 0:
            self.listbox.set_color(self.equipment, (105,105,255))
        self.listbox.draw()

        if self.listbox_id == 0:
            self.draw_equip()
        else:
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
            self.screen.blit(text, [555+95*i, HEIGHT-135])


    def check(self, select):
        # 装備変更確認
        for i, gun in enumerate(self.equipment):
            if gun == select:
                if i == 0:
                    PopupWindow(self.screen, "1番目に装備されています。\n場所の変更ができません。", ["OK"]).loop()
                    return False
                if i == self.change_gun:
                    return False
                while True:
                    if PopupWindow(self.screen, "すでに装備しています。\n場所を変更しますか？", \
                                   ["変更する", "変更しない"]).loop() == 0:
                        break
                    else:
                        return False
                self.equipment[i] = -1
        return True

    def _set_chip(self, select, size):
        i = self.change_chip
        self.chip_data[select]['num'] -= 1
        for j in range(size):
            self.chip[i+j] = select
        
    def _remove_chip(self, i, size, chip_id_list):
        # 装備済みのチップを外す
        for j in range(i,i+size):
            chip = self.chip[j]
            if chip == -1:
                continue
            data = self.chip_data[chip]
            chip_size = data['equip_size']
            data['num'] += 1
            j -= chip_id_list[j]
            for k in range(j, j+chip_size):
                self.chip[k] = -1

    def equip(self, select):
        # 選択した銃を装備する。
        if self.check(select):
            equipment = self.equipment
            equipment[self.change_gun] = select

    def set_chip(self, select):
        # チップの枠がサイズ何番目が保存されているのかを保持
        chip_id_list = []
        i = 0
        while i < 6:
            chip = self.chip[i]
            if chip == -1:
                size = 1
            else:
                size = self.chip_data[chip]['equip_size']
            chip_id_list += [j for j in range(size)]
            i += size
        # removeを選択したとき
        if select == len(self.listbox)-2:
            PopupWindow(self.screen, "選択したチップを外します。", ['OK']).loop()
            self._remove_chip(self.change_chip, 1, chip_id_list)
            return
        # remove ALLを選択したとき
        if select == len(self.listbox)-1:
            PopupWindow(self.screen, "すべてのチップを外します。", ['OK']).loop()
            for i in range(6):
                self._remove_chip(i, 1, chip_id_list)
            return
            
        chip_data = self.chip_data[select]
        # チップのサイズ
        size = chip_data['equip_size']
        i = self.change_chip
        # 装備可能上限まで装備しているか
        equip_num = self.chip.count(select)
        if i + size > 6:
            PopupWindow(self.screen, "装備可能な枠に収まりません。", ['OK']).loop()
            return
        if chip_data['equip_max'] == equip_num / size:
            PopupWindow(self.screen, "装備できる上限に達しています。", ['OK']).loop()
            return
        # 選択中の枠にそのチップを装備しているか
        if self.chip[i] == select and chip_id_list[i] == 0:
            PopupWindow(self.screen, 'すでにそのチップをこの枠に装備しています。', ['OK']).loop()
            return
        # 選択中の枠にチップが装備されているか
        count = self.chip[i:i+size].count(-1)    # -1が空枠
        if count != size:
            if PopupWindow(self.screen, "必要な枠に装備されているチップをすべて外し、装備します。", ['OK', 'NO']).loop() == 1:
                return
        self._remove_chip(i, size, chip_id_list)
        # チップを装備する
        self._set_chip(select, size)