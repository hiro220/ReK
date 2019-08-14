import pygame
import random

class MessageBox:

    def __init__(self, screen, x, y, width, message_list=[], bg=(255,255,255), font_size=30, \
                 outline_color=(100,100,100), select="standard"):
        """
        x, y, height, widthの範囲にメッセージ表示枠を作成する。背景色bg, フォントサイズfont_size, 枠線の色outline_color。
        message_listで指定した文章を、一つずつ作成した枠内に表示する。
        selectでは、('standard', 'random')から選び、指定する。
        """

        assert select in ('standard', 'random'), "selectに指定できるキーワード。'standard', 'random'"
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, font_size+20)
        self.message_list = message_list
        self.bg = bg
        self.font_size = font_size
        self.font = pygame.font.Font("freesansbold.ttf", font_size)
        self.outline_color = outline_color
        self.select = select
        self.i = 0
        self.chenge_message = True

    def draw(self):
        # 背景の塗りつぶし
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 5)
        if self.chenge_message:
            self.select_message()
        mask = (self.x, 0, self.rect.right-self.rect.left-10, self.font_size)
        color = (0,0,0)
        draw_message = self.font.render(self.message, True, color)
        x, y = self.rect.left+5, self.rect.top + 10
        self.screen.blit(draw_message, [x, y], mask)
        self.x += 3
        rect = draw_message.get_rect()
        self.chenge_message = (rect.right+50 < self.x)

    def select_message(self):
        if self.select == 'random':
            self.message = random.choice(self.message_list)
        elif self.select == 'standard':
            self.message = self.message_list[self.i]
        size = len(self.message_list)
        self.i = (self.i + size + 1) % size
        self.x = -self.rect.right+self.rect.left+10

    def __iadd__(self, message_list):
        self.message_list += message_list
        return self