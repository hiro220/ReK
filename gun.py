#!/usr/bin/env python
# coding:utf-8
from bullet import Bullet

class Gun:

    def __init__(self, machines, max=-1):
        """引数に指定するmaxは、弾の上限値"""
        self.max = max
        self.num = max
        self.machines = machines

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""

        return self.num == 0

    def shoot(self, x, y):
        return Bullet(x, y, 10, 0, self.machines)