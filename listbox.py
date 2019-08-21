import pygame
from pygame.locals import *

class ListBox:

    def __init__(self, screen, x, y, width, height, data_list=[], bg=(255,255,255), outline=3, \
                 outline_color=(155,155,155), target=False, font_size=20, title="", title_size=40):
        """リストボックスを作成する。
        Rect(x, y, width, height)で背景色bg(初期値では白)、外枠の大きさがoutline(初期値3)の描画領域を作成。
        その描画領域内に、data_listに指定したテキストのリストを縦にリストアップする。
        その際、フォントサイズはfont_size(初期値20)に設定される。
        targetは、このリストボックスにキー入力による選択の移動、Enterキーによる選択要素の返却を受け付けるかどうかを指定する。
        """
        # 描画領域の設定
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.bg = bg
        self.outline = outline
        self.outline_color = outline_color
        # キー入力受付の可否
        self.target = target
        # 選択要素、描画要素の初期化
        self.selected = 0
        self.top_id = 0
        self.left = 0
        # テキストのフォント
        self.font_size = font_size
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.title_size = title_size
        self.title = pygame.font.Font("freesansbold.ttf", title_size).render(title, True, (255,255,255))
        # 一度に描画する要素数
        self.draw_num = height // (font_size+10)
        # 要素の保持
        self.list = data_list
        self.selectable = [False for _ in self.list]
        self.color_reset()
        self.list_size = len(self.list)

    def draw(self, scroll=True):
        """self.screenで指定される画面にリストボックスを描画する。"""
        # 背景を塗りつぶす
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線を描画
        pygame.draw.rect(self.screen, self.outline_color, self.rect, self.outline)
        # titleの描画
        x, y = self.rect.left, self.rect.top - self.title_size
        self.screen.blit(self.title, [x, y])
        if scroll:
            # スクロールバーの枠を描画
            rect = Rect(self.rect.right-18, self.rect.top+3, 15, self.rect.bottom-self.rect.top-6)
            pygame.draw.rect(self.screen, (80,80,80), rect, 3)
            # スクロールバーを描画
            par = self.list_size<=self.draw_num or self.draw_num / self.list_size
            size = (rect.bottom-rect.top-6)
            height = size * par
            par = int(self.list_size == 0) or 1 - self.top_id / self.list_size
            top = rect.top + 3 + size * (1-par)
            rect = Rect(rect.left+3, top, 9, height)
            pygame.draw.rect(self.screen, (100,100,100), rect)
        scroll = scroll * 20
        self.left += 1

        # 表示する範囲のデータを抽出
        s, l = self.top_id, self.top_id+self.draw_num
        text_list = self.list[s:l]
        colors = self.color_list[s:l]
        # 描画位置、サイズなどの設定
        x, y = self.rect.left, self.rect.top
        i = 0
        for text, color in zip(text_list, colors):
            # テキストを描画範囲に収まるように描画
            size = (0,0,self.rect.right-self.rect.left-10-self.outline-scroll, self.font_size)
            draw_text = self.font.render(text, True, color)
            rect = draw_text.get_rect()
            # 選択中の要素に枠線を描画する
            if self.selected == self.top_id+i and self.target:
                # 描画範囲を超える大きさなら、収まるように調整
                self.left = self.left * (rect.right-self.left+10 > self.rect.right-self.rect.left-5-self.outline-scroll)
                if rect.right > self.rect.right-self.rect.left-5-self.outline-scroll:
                    size = (self.left,0,self.rect.right-self.rect.left-15-self.outline-scroll, self.font_size)
                    rect = Rect(0,0,self.rect.right-self.rect.left-5-self.outline-scroll, rect.bottom)
                rect.move_ip(x+5, y+5+(self.font_size+10)*i)
                # 描画
                pygame.draw.rect(self.screen, (255,0,0), rect, 2)
            self.screen.blit(draw_text, [x+5, y+5+(self.font_size+10)*i], size)
            i += 1

    def process(self, event):
        """pygameでの処理を行う。引数のeventには、pygame.event.get()で得られる要素を与える。"""
        # このListBoxがターゲットされていないなら処理はなし
        if not self.target or self.list_size == 0:
            return None
        if event.type == KEYDOWN:
            self.left = 0
            if event.key == K_UP:
                self.selected -= 1
            elif event.key == K_DOWN:
                self.selected += 1
            elif event.key == K_RETURN:
                if self.selectable[self.selected]:
                    self.target = False
                    return self.selected
            else:
                # 上下キー、Enterキー以外の入力があったとき、キー入力の受付をやめる
                self.target = False
            # 選択がリストボックスのid外になったなら収まるようにする
            self.selected = (self.selected+self.list_size) % self.list_size
            # 描画する要素の一番上のidを更新する
            self.top_id = (self.top_id <= self.selected <= self.top_id+self.draw_num-1) * self.top_id or \
                          (self.top_id+self.draw_num-1 < self.selected) * (self.selected-self.draw_num+1) or \
                          (self.top_id > self.selected) * (self.selected)

    def get_list(self):
        """保持しているテキストリストを返す。"""
        return self.list

    def set_selectable(self, selectable_list):
        """リストボックス内の要素が選択可能か指定する。
        引数のselectable_listはTrue、Falseのリストで、サイズはリストボックスのサイズと同じにしなければならない。"""
        color_list = []
        for tf, color in zip(selectable_list, self.color_list):
            if color in ((0,0,0), (100,100,100)):
                color_list.append((0,0,0)*tf or (100,100,100))
            else:
                color_list.append(color)
        self.color_list = color_list
        self.selectable = selectable_list

    def set_color(self, id_list, color):
        """引数id_listにリストとして指定したidの要素の色をcolorに設定する。
        ただし、idはすべて自然数で指定する。(リストの後ろから指定することができない)"""
        for i in id_list:
            if i < 0:
                continue
            self.color_list[i] = color

    def color_reset(self):
        """テキストの色を選択可能かで黒色と灰色のどちらかに初期化する。"""
        self.color_list = [(0,0,0)*tf or (100,100,100) for tf in self.selectable]

    def __call__(self):
        """呼ぶことで、このリストボックスがキー入力を受け付ける。"""
        self.target = True

    def __len__(self):
        """ len()で呼ばれたとき、保持しているテキストのリストのサイズを返す。"""
        return self.list_size

    def __iadd__(self, others_list):
        """ +=演算子が用いられたとき、右辺のリストをself.listに結合する。"""
        self.list += others_list
        self.list_size += len(others_list)
        self.selectable += [False for i in others_list]
        self.color_reset()
        return self