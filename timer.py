# coding:utf-8

import pygame
from define import R_time

class Timer(pygame.sprite.Sprite):

    def __init__(self, millisecond, process, *args):
        """millisecondミリ秒経過後、processを実行する。
        Timer(2500, sample)のように使う。processには関数名を記述する。
        引数が必要な関数(def sample(a, b)みたいなの)を指定したとき、Timer(2500, sample, 10, 2)のように記述する。
        このとき、sample(10, 2)で実行される。
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.process = process                                  # 関数processをインスタンス変数に
        self.time = millisecond                                 # 時間計測
        self.args = args
        self.init_time = R_time.get_ticks()                # 作成時の時間を保持
        self.value = None

    def update(self):
        if R_time.get_ticks() - self.init_time >= self.time:       # このインスタンスが生成されたときからの経過時間が設定した時間より長い
            self.value = self.process(*self.args)                                      # processを実行
            self.kill()                                         # このスプライトをグループから削除

class FlagTimer(Timer):

    def __init__(self, process, *args, flag=False):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.process = process
        self.args = args
        self.flag = flag

    def update(self):
        if self.flag:
            self.flag = False
        else:
            self.process(*self.args)
            self.kill()