import pygame
from pygame.locals import *
from glob import glob

class ImageBox:

    def __init__(self, screen, x, y, image_width, image_height, frame_num, bg=(255,255,255), outline_color=(150,150,150),\
                 outline_size=2, change_speed=3, target=False):
        self.screen = screen
        width = 30 + (image_width + 5) * frame_num + 25 + outline_size*2
        height = image_height + 10 + outline_size*2
        self.rect = Rect(x, y, width, height)
        self.image_width, self.image_height = image_width, image_height
        self.frame_num = frame_num
        self.change_speed = change_speed
        self.image_list = [None for _ in range(frame_num)]
        self.bg = bg
        self.outline_color = outline_color
        self.outline_size = outline_size
        self.target = target
        self.select = 0
        self.count_time = 0

    def draw(self):
        # 描画領域の描画
        self.count_time += 1 / self.change_speed
        pygame.draw.rect(self.screen, self.bg, self.rect)
        pygame.draw.rect(self.screen, self.outline_color, self.rect, self.outline_size)
        x = self.rect.left + self.outline_size + 30
        y = self.rect.top + self.outline_size + 5
        for i, data in enumerate(self.image_list):
            j, data = data
            if type(data) == list:
                if self.select == i:
                    j = (int(self.count_time)+len(data)) % len(data)
                data = data[j]
            # 画像の描画
            if type(data) == str:
                # 画像のパスを表す
                image = pygame.image.load(data).convert_alpha()
                self.screen.blit(image, [x, y])
            elif type(data) == int:
                # 数字を枠内に描画する
                text = pygame.font.Font("font/freesansbold.ttf", 80).render(str(data), True, (0,0,0))
                rect = text.get_rect()
                width, height = rect.right, rect.bottom
                tx, ty = x+self.image_width/2-width/2, y+self.image_height/2-height*3/7
                self.screen.blit(text, [tx, ty])
            # 枠の描画
            color = (0,)*3 * (self.select != i) or (255,0,0)
            size = 2 + (self.select==i) * 2
            pygame.draw.rect(self.screen, color, Rect(x, y, self.image_width, self.image_height), size)
            x += self.image_width + 5

    def process(self, event_key):
        if event_key == K_LEFT:
            self.select -= 1
            self.count_time = 0
        elif event_key == K_RIGHT:
            self.select += 1
            self.count_time = 0
        elif event_key == K_RETURN:
            return self.select
        self.select = (self.select + self.frame_num) % self.frame_num
        
    def set_image(self, image_path_list, init_list=[]):
        """枠内に表示したい画像のパスをリストにして引数に渡す。 image_path_listの要素数はコンストラクタで指定したframe_numと同じにする。
        要素には、画像へのパス、画像が入ったフォルダへのパス('/'で終える)、int型の数字のいずれかが指定できる。それぞれ、次のように動作する。
        画像へのパス：指定した画像が描画される。
        フォルダへのパス：指定したフォルダ内にある画像を一定間隔で切り替えて描画する。
        int型の数字：指定した数字が枠内に描画される。
        画像はpng拡張子のみ受け付ける。"""
        assert len(image_path_list) == self.frame_num, "引数に指定されたリストの要素数が正しくありません。"
        self.image_list = []
        if init_list == []:
            init_list = [0 for _ in range(self.frame_num)]
        for i, path in zip(init_list, image_path_list):
            if type(path) == str and path[-1] == '/':
                # フォルダが指定された。
                path = glob(path+'*.png')
                path.sort()
            self.image_list.append([i, path])
            