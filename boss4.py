from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import Timer

img_path = "img/cpu/"

class Stage4_Boss(Boss):

    def __init__(self, x, y, players, score, money):
        image = pygame.image.load(img_path+"cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, 300, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.dx, self.dy = -2, 0
        # 動作の実行中にTrueになる。Falseのときはどの動作も実行していない。
        self.action_flag = False

    def update(self):
        # 動作を選択する
        select = self.select_actions()
        # 選択された動作を実行
        self.action(select)
        # 移動する
        self.move(self.dx, self.dy)

    def select_actions(self):
        # 現在の状況などから、行動の選択、移動(self.dx, self.dy)の変更を行う
        action = None
        return action

    def action(self, select):
        # select_actionで選択された動作を実行する。
        pass

    def create_item(self):
        pass

    def move2straight(self, x, y):
        nowx, nowy = self.rect.center
        x = x - nowx
        y = y - nowy
        d = self.dx+self.dy
        self.dx = d * x / (x+y)
        self.dy = d * y / (x+y)

    def action_cancel(self):
        # 今実行中の動作をキャンセルする。
        # 一定時間行動しない
        pass

class CancelItem(Item):

    def __init__(self, x, y, machine, boss):
        image = 'img/item/recovery.png'
        super().__init__(x, y, image, machine)
        self.boss = boss

    def effect(self, machine):
        self.boss.action_cancel()
