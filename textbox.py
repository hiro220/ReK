import pygame
from pygame.locals import Rect
import unicodedata

class TextBox:
    def __init__(self, screen, x, y, width, height, text='', bg=(255,255,255), text_color=(0,0,0), font_size=20, \
                 outline_color=(150,150,150), full_font=None, half_font='freesansbold.ttd'):
        self.screen = screen
        self.rect = Rect(x, y, width, height)
        self.bg = bg
        self.text_color = text_color
        self.font_size = font_size
        self.outline_color = outline_color
        texts = self.separate_text(text)
        self.texts = self.create_text(texts, full_font, half_font)

    def separate_text(self, text):
        texts = []
        one_text = ''
        char_type = self.isfull_size(text[0])
        for char in text:
            isfull = self.isfull_size(char)
            if char_type * isfull:
                one_text += char
            else:
                texts.append([char_type, one_text])
                char_type = isfull
                one_text = char
        texts.append([char_type, one_text])
        return texts

    def create_text(self, texts, full_font, half_font):
        full_font = pygame.font.Font(full_font, self.font_size)
        half_font = pygame.font.Font(half_font, self.font_size)
        font_texts = []
        width = 0
        frame_width = self.rect.right - self.rect.right - 10
        for char_type, text in texts:

            text = char_type * full_font.render(text, True, self.text_color) or \
                   half_font.render(text, True, self.text_color)
        return font_texts

    def isfull_size(self, char):
        return unicodedata.east_asian_width(char) in ('F', 'W', 'A')