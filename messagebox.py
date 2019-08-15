import pygame
import random

class MessageBox:

    def __init__(self, screen, x, y, width, message_list=[], bg=(255,255,255), font_size=30, \
                 outline_color=(100,100,100), select="standard", scroll=True):
        """
        x, y, height, widthの範囲にメッセージ表示枠を作成する。背景色bg, フォントサイズfont_size, 枠線の色outline_color。
        message_listで指定した文章を、一つずつ作成した枠内に表示する。
        selectでは、('standard', 'random')から選び、指定する。
        """

        # selectに指定できるキーワード以外を指定したときエラーを出す。
        assert select in ('standard', 'random'), "selectに指定できるキーワード。'standard', 'random'"
        # 描画画面の設定
        self.screen = screen
        # 描画枠の設定
        self.rect = pygame.Rect(x, y, width, font_size+20)
        self.bg = bg
        self.outline_color = outline_color
        # メッセージリストの設定
        self.message_list = message_list
        # フォントの設定
        self.font_size = font_size
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        # メッセージの取得方法の設定
        self.select = select
        # 最初に表示するメッセージの設定
        self.i = 0
        self.chenge_message = True
        self.scroll = scroll

    def draw(self):
        # 背景の塗りつぶし
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 5)
        if self.chenge_message:
            self.select_message()
        # 枠ないにメッセージが収まるサイズ
        mask = (self.x * self.scroll, 0, self.rect.right-self.rect.left-10, self.font_size)
        color = (0,0,0)
        draw_message = self.font.render(self.message, True, color)
        x, y = self.rect.left+5, self.rect.top + 10
        # メッセージの表示
        self.screen.blit(draw_message, [x, y], mask)
        # メッセージ移動
        self.x += 3
        rect = draw_message.get_rect()
        # メッセージが左端に消えて50pixel分移動したなら、次のメッセージへ
        self.chenge_message = (rect.right+50 < self.x)

    def select_message(self):
        # 選択している取得方法から、メッセージリストのメッセージを一つ選ぶ。
        if self.select == 'random':
            self.message = random.choice(self.message_list)
        elif self.select == 'standard':
            self.message = self.message_list[self.i]
        size = len(self.message_list)
        # 選んだindexを更新
        self.i = (self.i + size + 1) % size
        # maskの座標を更新
        self.x = -self.rect.right+self.rect.left+10

    def __iadd__(self, message_list):
        """メッセージの追加"""
        self.message_list += message_list
        return self