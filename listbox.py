import pygame
from pygame.locals import *
from define import EXIT
import numpy as np

class ListBox:

    def __init__(self, screen, x, y, width, height, data_list=[], bg=(255,255,255), outline=3, \
                 outline_color=(155,155,155),target=False, font_size=20):
        """リストボックスを作成する。
        Rect(x, y, width, height)で背景色bg(初期値では白)、外枠の大きさがoutline(初期値3)の描画領域を作成。
        その描画領域内に、data_listに指定したテキストのリストを縦にリストアップする。
        その際、フォントサイズはfont_size(初期値20)に設定される。
        targetは、このリストボックスにキー入力による選択の移動、Enterキーによる選択要素の返却を受け付けるかどうかを指定する。
        """
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.list = data_list
        self.bg = bg
        self.outline = outline
        self.outline_color = outline_color
        self.target = target
        self.selected = 0
        self.top_id = 0
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.draw_num = height // (font_size+10)
        self.font_size = font_size
        self.list_size = len(self.list)
        self.selectable = [False for _ in self.list]
        self.color_list = [(0,0,0) for _ in self.list]

    def draw(self):
        """self.screenで指定される画面にリストボックスを描画する。"""
        # 背景を塗りつぶす
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線を描画
        pygame.draw.rect(self.screen, self.outline_color, self.rect, self.outline)
        # スクロールバーの枠を描画
        rect = Rect(self.rect.right-15, self.rect.top, 15, self.rect.bottom-self.rect.top)
        pygame.draw.rect(self.screen, (80,80,80), rect, 3)
        # スクロールバーを描画
        par = self.draw_num / self.list_size
        size = (self.rect.bottom-self.rect.top-6)
        height = size * par
        par = self.top_id / self.list_size
        top = self.rect.top + 3 + size * par
        rect = Rect(rect.left+3, top, 9, height)
        pygame.draw.rect(self.screen, (100,100,100), rect)
        
        # 表示する範囲のデータを抽出
        s, l = self.top_id, self.top_id+self.draw_num
        text_list = self.list[s:l]
        colors = self.color_list[s:l]
        # 描画位置、サイズなどの設定
        x, y = self.rect.left, self.rect.top
        size = (0,0,self.rect.right-self.rect.left-25-self.outline, self.font_size)
        i = 0
        for text, color in zip(text_list, colors):
            # テキストを描画範囲に収まるように描画
            draw_text = self.font.render(text, True, color)
            self.screen.blit(draw_text, [x+5, y+5+(self.font_size+10)*i], size)
            # 選択中の要素に枠線を描画する
            if self.selected == self.top_id+i:
                rect = draw_text.get_rect()
                # 描画範囲を超える大きさなら、収まるように調整
                if rect.right > self.rect.right-self.rect.left-20-self.outline:
                    rect = Rect(0,0,self.rect.right-self.rect.left-20-self.outline, rect.bottom)
                rect.move_ip(x+5, y+5+(self.font_size+10)*i)
                # 描画
                pygame.draw.rect(self.screen, (255,0,0), rect, 2)
            i += 1


    def process(self, event):
        """pygameでの処理を行う。引数のeventには、pygame.event.get()で得られる要素を与える。"""
        # このListBoxがターゲットされていないなら処理はなし
        if not self.target:
            return None
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected -= 1
            elif event.key == K_DOWN:
                self.selected += 1
            elif event.key == K_RETURN:
                if self.selectable[self.selected]:
                    self.target = False
                    return self.selected
            else:
                self.target = False
            self.selected = (self.selected+self.list_size) % self.list_size
            self.top_id = (self.top_id <= self.selected <= self.top_id+self.draw_num-1) * self.top_id or \
                          (self.top_id+self.draw_num-1 < self.selected) * (self.selected-self.draw_num+1) or \
                          (self.top_id > self.selected) * (self.selected)

    def get_list(self):
        """保持しているテキストリストを返す。"""
        return self.list

    def set_selectable(self, selectable_list):
        color_list = []
        for tf, color in zip(selectable_list, self.color_list):
            if color in ((0,0,0), (100,100,100)):
                color_list.append((0,0,0)*tf or (100,100,100))
            else:
                color_list.append(color)
        self.color_list = color_list
        self.selectable = selectable_list

    def set_color(self, id_list, color):
        for i in id_list:
            if i == -1:
                continue
            self.color_list[i] = color

    def color_reset(self):
        self.color_list = [(0,0,0)*tf or (100,100,100) for tf in self.selectable]

    def __call__(self):
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