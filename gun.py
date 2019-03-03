#!/usr/bin/env python
# coding:utf-8
from bullet import *
import pygame
from pygame.locals import *
import math

class Gun:

    def __init__(self, machines, max=-1):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.rect = Rect(0,0,960,600)

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        Bullet(x, y, 10, 0, self.machines)      # 弾を生成する(BulletクラスはMainクラスでグループ化されているため、返却する必要はない)
    
    
class Gun2(Gun):

    def __init__(self, machines, max=-1):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.rect = Rect(0,0,960,600)

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        play_list = self.machines.sprites()
        for play in play_list:   
            distance = math.sqrt((play.rect.centerx-x)**2+(play.rect.centery-y)**2)
            angle = distance / 10
            Bullet(x, y, (play.rect.centerx-x)/angle,(play.rect.centery-y)/angle, self.machines)


class Gun3(Gun):

    def __init__(self, machines, max=-1):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.rect = Rect(0,0,960,600)

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        Bullet(x, y, -10, 0, self.machines)
        
class Gun4(Gun):

    def __init__(self, machines, max=-1):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines
        self.rect = Rect(0,0,960,600)

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        Bullet2(x, y, -10, 0, self.machines)

