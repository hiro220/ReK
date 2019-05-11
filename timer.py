# coding:utf-8

import pygame
from pygame.locals import *

class Timer(pygame.sprite.Sprite):

    def __init__(self, millisecond, process):
        """millisecondミリ秒経過後、processを実行する。
        Timer(2500, sample)のように使う。processには関数名を記述する。
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.process = process                                  # 関数processをインスタンス変数に
        self.time = millisecond                                 # 時間計測
        self.init_time = pygame.time.get_ticks()                # 作成時の時間を保持

    def update(self):
        if pygame.time.get_ticks() - self.init_time >= self.time:       # このインスタンスが生成されたときからの経過時間が設定した時間より長い
            self.process()                                      # processを実行
            self.kill()                                         # このスプライトをグループから削除