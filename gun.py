#!/usr/bin/env python
# coding:utf-8
from bullet import Bullet

class Gun:

    def __init__(self, machines, max=-1):
        """引数は、発射する弾の当たり判定対象となる機体グループ。発射できる弾の上限値max(初期値は無限を意味する-1)"""
        self.max = self.num = max       # インスタンス変数max, numに引数の値をセットする
        self.machines = machines

    def isBulletZero(self):
        """銃弾数が0ならTrue
        そうでないならFalseを返す"""
        return self.num == 0

    def shoot(self, x, y):
        """引数は弾の発射位置(x, y)"""
        Bullet(x, y, 10, 0, self.machines)      # 弾を生成する(BulletクラスはMainクラスでグループ化されているため、返却する必要はない)