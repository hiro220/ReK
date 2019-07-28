import pygame
from pygame.locals import *
from define import *

class Equipment:

    def __init__(self, screen, data):
        self.data = data
        self.screen = screen
        self.selected = 0               # 現在選択している銃
        self.change_gun = 0             # 現在選択している装備場所
        self.top_draw = 0               # 現在表示している一番上の銃
        self.guns_num = len(self.data['gun_data'])
        self.back = False               # 一つ前の画面にもどるか
        self.screen_info = pygame.font.Font("freesansbold.ttf" ,70).render("Equip", True, (255,255,255))
        self.back_info = pygame.font.Font("freesansbold.ttf" ,50).render("'Q' : Back", True, (255,255,255))
    
    def do(self):
        while True:
            request = self.process()
            self.draw()
            if request != CONTINUE:
                return request

    def process(self):
        # 内部処理
        for event in pygame.event.get():
            if event.type == QUIT:
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.selected -= 1
                elif event.key == K_DOWN:
                    self.selected += 1
                elif event.key == K_RIGHT:
                    self.change_gun += 1
                elif event.key == K_LEFT:
                    self.change_gun -= 1
                elif event.key == K_q:
                    return BACK
                elif event.key == K_RETURN:
                    self.equip()
                self.change_gun = (self.change_gun + 3) % 3
                self.selected = (self.selected+self.guns_num) % self.guns_num
                
                # 選択している銃が、表示している銃でないなら、表示する銃を調整する
                # 選択中の銃が画面内にあれば、そのまま
                self.top_draw = (self.top_draw <= self.selected <= self.top_draw+4) * self.top_draw or \
                                (self.top_draw+4 < self.selected) * (self.selected-4) or \
                                (self.top_draw > self.selected) * (self.selected)
        return CONTINUE

    def draw(self):
        # 画面描画
        self.screen.fill((0,0,0))
        self.screen.blit(self.screen_info, [150, 20])
        self.screen.blit(self.back_info, [WIDTH-self.back_info.get_rect().right-20, 20])

        # 銃一覧の表示
        for i in range(5):
            gun_id = i+self.top_draw
            gun = self.data['gun_data'][gun_id]
            gun_text = gun['name']
            color = (105, 105, 255)*(gun_id in self.data['equip']) or (150+105*gun['own'],)*3
            draw_text = pygame.font.Font("freesansbold.ttf", 40).render(gun_text, True, color)
            self.screen.blit(draw_text, [80, 150+50*i])
            if self.selected == gun_id:
                width = draw_text.get_rect().right
                height = draw_text.get_rect().bottom
                color = (255,0,0)
                pygame.draw.rect(self.screen, color, Rect(75, 145+50*i, width+10, height+10), 2)
        pygame.display.update()

    def check(self):
        # 装備変更確認
        gun = self.data['gun_data'][self.selected]
        if gun['own'] == 0:
            return False
        for i, gun in enumerate(self.data['equip']):
            if gun == self.selected:
                if i == 0:
                    return False
                self.data['equip'][i] = -1
        return True

    def equip(self):
        # 選択した銃を装備する。
        if self.check():
            equipment = self.data['equip']
            equipment[self.change_gun] = self.selected