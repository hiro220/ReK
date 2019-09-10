import pygame
from pygame.locals import *
from define import *
from listbox import ListBox
from popupwindow import PopupWindow
from image_box import ImageBox

class Equipment:

    def __init__(self, screen, data):
        # データを保持
        self.gun_data = data["gun_data"]
        self.equipment = data["equip"]
        self.chip_data = data["chip_data"]
        self.chip = data["chip"]
        # スクリーンの保持
        self.screen = screen
        # 選択の初期値
        self.change_gun = 0             # 現在選択している装備場所
        self.change_chip = 0
        self.change_id = 0
        self.back = False               # 一つ前の画面にもどるか
        # 操作の表記
        self.screen_info = pygame.font.Font("font/freesansbold.ttf" ,70).render("Equip", True, (255,255,255))
        self.back_info = pygame.font.Font("font/ShipporiMincho-TTF-Regular.ttf" ,50).render("'Q' : 戻る", True, (255,255,255))
        self.change_info = pygame.font.Font("font/ShipporiMincho-TTF-Regular.ttf" ,50).render("'C' : 切り替え", True, (255,255,255))
        # リストボックスの作成
        # Gun
        texts = [data["name"] for data in self.gun_data.values()]
        equip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Gun", title_size=60)
        equip_listbox.set_selectable([data["own"]==1 for data in self.gun_data.values()])
        # Chip
        texts = [data['name'] for data in self.chip_data.values()]
        chip_listbox = ListBox(self.screen, 80, 200, 300, 250, texts, font_size=40, target=True,\
                                     title="Chip", title_size=60)
        chip_listbox += ['remove', 'remove ALL']
        # 両方をリストに格納し、選択された方を描画
        self.listboxes = [equip_listbox, chip_listbox]
        self.listbox = self.listboxes[self.change_id]
        # 現在の装備状況を描画するイメージボックスの作成
        self.gun_image_box = ImageBox(screen, 700, 450, 90, 90, 3)
        self.chip_image_box = ImageBox(screen, 500, 450, 90, 90, 6)
        # 時間管理
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
        # チップのリストボックスで、選択の可否を設定
        select = [data["num"] > 0 for data in self.chip_data.values()] \
                    + [self.chip[self.change_chip]!=-1, self.chip!=[-1]*6]
        self.listboxes[1].set_selectable(select)
        # 装備状況のターゲット選択
        self.gun_image_box.target = self.change_id==0
        self.chip_image_box.target = self.change_id==1

        # ユーザー入力
        for event in pygame.event.get():
            select = self.listbox.process(event)

            # リストボックスからアイテムが選択された
            if select != None:
                if self.change_id == 0:
                    self.equip(select)
                else:
                    self.set_chip(select)

            # 閉じるボタンが選択された
            if event.type == QUIT:
                # ゲーム終了のコードを返却する
                return EXIT

            # その他のキー入力が行われた
            if event.type == KEYDOWN:
                # イメージボックスの入力処理
                if self.change_id == 0:
                    self.gun_image_box.process(event.key)
                    self.change_gun = self.gun_image_box.select
                else:
                    self.chip_image_box.process(event.key)
                    self.change_chip = self.chip_image_box.select
                # Qキーが入力された
                if event.key == K_q:
                    # 一つ前の画面に戻る
                    return BACK
                # Cキーが入力された
                elif event.key == K_c:
                    self.change_id ^= 1
                    self.listbox = self.listboxes[self.change_id]
        return CONTINUE

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [850, 20])
        self.screen.blit(self.change_info, [850, 90])
        
        # リストボックスのカラー設定
        self.listbox.color_reset()
        if self.change_id == 0:
            self.listbox.set_color(self.equipment, (105,105,255))
        # リストボックスの描画
        self.listbox.draw()

        # 装備情報の描画
        if self.change_id == 0:
            self.draw_equip()
        else:
            self.draw_chip()
        # 画面更新
        pygame.display.update()

    def draw_equip(self):
        # 装備中の銃情報の表示
        data_list = []
        id_list = []
        for data in self.equipment:
            # 装備していない
            if data == -1:
                data_list.append(None)
                id_list.append(0)
            # 画像がある
            elif data == 0:
                data_list.append('img/gun_icon/'+str(data)+'/')
                id_list.append(3)
            # 画像がない
            else:
                data_list.append(data)
                id_list.append(0)
        self.gun_image_box.set_image(data_list, id_list)
        self.gun_image_box.draw()
                

    def draw_chip(self):
        # チップのIDを描画
        pygame.draw.rect(self.screen, (255,255,255), Rect(500, HEIGHT-150, 625, 100))
        self.chip_image_box.set_image([None if data==-1 else data for data in self.chip])
        self.chip_image_box.draw()

    def equip(self, select):
        # 選択した銃を装備する。
        if self.check(select):
            equipment = self.equipment
            equipment[self.change_gun] = select

    def check(self, select):
        # 装備変更確認
        for i, gun in enumerate(self.equipment):
            # 選択した銃がすでに装備済み
            if gun == select:
                # その場所が1番目(リストでの0番目)
                if i == 0:
                    PopupWindow(self.screen, "1番目に装備されています。\n場所の変更ができません。", ["OK"]).loop()
                    return False
                # その位置に選択した銃がすでに装備されている
                if i == self.change_gun:
                    return False
                # 変更可能な位置に装備している
                while True:
                    if PopupWindow(self.screen, "すでに装備しています。\n場所を変更しますか？", \
                                   ["変更する", "変更しない"]).loop() == 0:
                        break
                    else:
                        return False
                # 装備していた銃を外す
                self.equipment[i] = -1
        return True

    def _set_chip(self, i, select, size):
        # チップ装備処理
        self.chip_data[select]['num'] -= 1
        # チップが要するサイズ分セット
        for j in range(size):
            self.chip[i+j] = select
        
    def _remove_chip(self, i, size, chip_id_list):
        # 装備済みのチップを外す
        for j in range(i,i+size):
            chip = self.chip[j]
            if chip == -1:
                continue
            # 外したチップの情報
            data = self.chip_data[chip]
            chip_size = data['equip_size']
            # 所持数を1増やす
            data['num'] += 1
            # チップを装備から外す
            j -= chip_id_list[j]
            for k in range(j, j+chip_size):
                self.chip[k] = -1

    def set_chip(self, select):
        # チップが要する枠のサイズごとに番号をつける(3枠のチップなら、[0,1,2]と番号をつける)
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
        # 装備する場所にすでに装備されているチップを外す
        self._remove_chip(i, size, chip_id_list)
        # チップを装備する
        self._set_chip(i, select, size)