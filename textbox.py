import pygame
from pygame.locals import Rect
import unicodedata

class TextBox:
    def __init__(self, screen, x, y, width, height, text='', bg=(255,255,255), text_color=(0,0,0), font_size=20, \
                 outline_color=(150,150,150), full_font="", half_font='freesansbold.ttf'):
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.bg = bg
        self.text_color = text_color
        self.font_size = font_size
        self.outline_color = outline_color
        texts = self.separate_text(text)
        self.texts = self.create_text(texts, full_font, half_font)

    def draw(self):
        # 描画領域の塗りつぶし
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線の描画
        pygame.draw.rect(self.screen, self.outline_color, self.rect, 3)
        for i, oneline in enumerate(self.texts):
            # テキストの表示位置
            x, y = self.rect.left+5, self.rect.top + 5 + self.font_size * i
            # 一行表示
            for text in oneline:
                # 全角と半角で分離されているので、すべて描画
                rect = text.get_rect()
                self.screen.blit(text, [x, y])
                x += rect.right - rect.left

    def separate_text(self, text):
        """入力したテキストを、全角部分と半角部分で分割し、順番はそのままにリストにする。"""
        texts = []
        one_text = ''
        char_type = self.isfull_size(text[0])
        for char in text:
            isfull = self.isfull_size(char)
            if char_type == isfull:
                # 文字が一文字前と同じサイズのとき
                one_text += char
            else:
                # 文字が一文字前と違うサイズ
                texts.append([char_type, one_text])
                char_type = isfull
                one_text = char
        texts.append([char_type, one_text])
        return texts

    def create_text(self, texts, full_font, half_font):
        """枠内に収まるサイズになるよう、全角、半角それぞれのテキストを画像化してリスト(二次元)に格納し、返却する。
        リストは各要素が一行に表示する文字列の画像で、要素の一つ一つが全角、半角ごとでリストにされている。"""
        # 枠内判定に用いるテキストの幅と枠の幅
        width = 0
        frame_width = self.rect.right - self.rect.left - 10
        font_texts = []     # 枠内に表示するすべてのテキスト
        one_line = []       # 一行に表示するテキスト
        # 全角半角ごとに分割したテキスト全てを描画形式に変換
        for char_type, text in texts:
            # このtext幅を加算
            width += len(text) * self.font_size * (1+char_type)
            font = pygame.font.Font(full_font*char_type or half_font, self.font_size)
            if frame_width >= width:
                # 枠内に収まるとき
                draw_text = font.render(text, True, self.text_color)
                one_line.append(draw_text)
            else:
                # 枠内に収まらないとき
                diff = width
                i = 0
                while diff >= 0:
                    # 枠内に収まる範囲のテキストを抽出
                    diff -= frame_width
                    j = diff // (self.font_size * (1+char_type))
                    draw_text = font.render(text[i:-j], True, self.text_color)
                    i = -j
                    # テキストを一行のリストに追加
                    one_line.append(draw_text)
                    # 一行分のリストを全体のリストに追加
                    font_texts.append(one_line)
                    # 次の行へ
                    one_line = []
                # 次の行で使っている幅
                width = -diff
        font_texts.append(one_line)
        return font_texts

    def isfull_size(self, char):
        """引数に入力した1文字が全角文字かどうかを判定。全角文字のときはTreu, 半角文字だとFalseが返却される"""
        return unicodedata.east_asian_width(char) in ('F', 'W', 'A')