import pygame
from pygame.locals import *
from define import EXIT
import numpy

class ListBox:

    def __init__(self, screen, x, y, width, height, data_list=[], bg=(255,255,255), outline=3, target=False, font_size=20):
        """リストボックスを作成する。
        Rect(x, y, width, height)で背景色bg(初期値では白)、外枠の大きさがoutline(初期値3)の描画領域を作成。
        その描画領域内に、data_listに指定したテキストのリストを縦にリストアップする。その際、フォントサイズはfont_size(初期値20)に設定される。
        targetは、このリストボックスにキー入力による選択の移動、Enterキーによる選択要素の返却を受け付けるかどうかをしていする。
        """
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.list = data_list
        self.bg = bg
        self.outline = outline
        self.target = target
        self.selected = 0
        self.top_id = 0
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.draw_num = height // (font_size+10)
        self.font_size = font_size
        self.list_size = len(self.list)

    def draw(self):
        """self.screenで指定される画面にリストボックスを描画する。"""
        pygame.draw.rect(self.screen, self.bg, self.rect)
        pygame.draw.rect(self.screen, (0,0,0), self.rect, self.outline)
        text_list = self.list[self.top_id:self.top_id+self.draw_num]
        x, y = self.rect.left, self.rect.top
        for i, text in enumerate(text_list):
            color = (0,0,0)
            draw_text = self.font.render(text, True, color)
            self.screen.blit(draw_text, [x+5, y+(self.font_size+10)*i])
            if self.selected == self.top_id+i:
                rect = draw_text.get_rect()
                rect.move_ip(x+5, y+(self.font_size+10)*i)
                pygame.draw.rect(self.screen, (255,0,0), rect, 2)


    def process(self, event):
        """pygameでの処理を行う。引数のeventには、pygame.event.get()で得られる要素を与える。"""
        # このListBoxがターゲットされていないなら処理はなし
        if not self.target:
            return
        if event.type == QUIT:
            return EXIT
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected -= 1
            elif event.key == K_DOWN:
                self.selected += 1
            elif event.key == K_RETURN:
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
        pass

    def __call__(self):
        self.target ^= True

    def __len__(self):
        """ len()で呼ばれたとき、保持しているテキストのリストのサイズを返す。"""
        return self.list_size

    def __iadd__(self, others_list):
        """ +=演算子が用いられたとき、右辺のリストをself.listに結合する。"""
        self.list += others_list
        self.list_size += len(others_list)
        return self