import pygame
from pygame.locals import Rect
import unicodedata

class TextBox:
    def __init__(self, screen, x, y, width, height, text='', bg=(255,255,255), text_color=(0,0,0), font_size=20, \
                 outline_color=(150,150,150), outline_size=3, full_font="", half_font='freesansbold.ttf', \
                 align=('left', 'top')):
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.bg = bg
        self.text_color = text_color
        self.font_size = font_size
        self.outline_size = outline_size
        self.outline_color = outline_color
        texts = self.separate_text(text)
        self.texts = self.create_text(texts, full_font, half_font)
        assert align[0] in ('left', 'center', 'right'), "選択できる横向きのalign属性('left', 'center', 'right')"
        assert align[1] in ('top', 'center', 'bottom'), "選択できる縦向きのalign属性('top', 'center', 'buttom')"
        self.align = align

    def draw(self):
        # 描画領域の塗りつぶし
        pygame.draw.rect(self.screen, self.bg, self.rect)
        # 枠線の描画
        pygame.draw.rect(self.screen, self.outline_color, self.rect, self.outline_size)
        height = len(self.texts) * self.font_size
        for i, oneline in enumerate(self.texts):
            width = oneline[-1]
            # テキストの表示位置
            x = self.rect.left + 5
            y = self.rect.top + self.font_size * i + 3
            frame_width, frame_height = self.rect.right - self.rect.left - 10, self.rect.bottom - self.rect.top - 6
            # 横方向に対する整列
            if self.align[0] == 'center':
                x += (frame_width - width) / 2
            elif self.align[0] == 'right':
                x += frame_width - width
            # 縦方向に対する整列
            if self.align[1] == 'center':
                y += (frame_height - height) / 2
            elif self.align[1] == 'bottom':
                y += frame_height - height
            # 一行表示
            for text in oneline[:-1]:
                # 全角と半角で分離されているので、すべて描画
                rect = text.get_rect()
                self.screen.blit(text, [x, y])
                x += rect.right

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
            # フォント設定
            font = pygame.font.Font(full_font*char_type or half_font, self.font_size)
            # 一文字ごとに描画テキストを作成
            for char in text:
                char = font.render(char, True, self.text_color)
                size = char.get_rect().right
                width += size
                if width <= frame_width:
                    # 枠内に収まる
                    one_line.append(char)
                else:
                    # 枠内に収まらない
                    # 一行分をリストに格納し、次の行を作成
                    one_line.append(width-size)
                    width = size
                    font_texts.append(one_line)
                    one_line = []
                    one_line.append(char)
        one_line.append(width)
        font_texts.append(one_line)
        return font_texts

    def isfull_size(self, char):
        """引数に入力した1文字が全角文字かどうかを判定。全角文字のときはTreu, 半角文字だとFalseが返却される"""
        return unicodedata.east_asian_width(char) in ('F', 'W', 'A')