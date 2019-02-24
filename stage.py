#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from bullet import Bullet
from playermachine import PlayerMachine
from cpumachine import *
from define import *

class Stage:

    def __init__(self, screen):
        self.screen = screen
        self.initGroup()
        self.player = PlayerMachine(PLAYER_X, PLAYER_Y, self.cpus)    # プレイヤーのマシンを生成する

        self.clock = pygame.time.Clock()        # 時間管理用

        CpuMachine(900, 300, self.players)      # cpuの機体を生成
        CpuMachine(900, 400, self.players)
        CpuMachine(900, 100, self.players)
        self.loop()

    def initGroup(self):
        self.group = pygame.sprite.RenderUpdates()  # 描画する機体や弾用のグループ
        self.players = pygame.sprite.Group()        # playerの機体用グループ
        self.cpus = pygame.sprite.Group()           # cpuの機体用グループ

        PlayerMachine.containers = self.group, self.players     # プレイヤーマシンにグループを割り当てる
        CpuMachine.containers = self.group, self.cpus           # cpuマシンにグループを割り当てる
        Bullet.containers = self.group                          # 弾にグループを割り当てる

    def loop(self):
        while True:
            self.clock.tick(30)         # フレームレート(30fps)
            result = self.process()
            self.draw()
            if result:
                break

    def process(self):
        # 1フレームごとの処理
        self.player.move(HEIGHT, WIDTH)  # 入力に応じてプレイヤーの機体を動かす
        self.group.update()         # groupに割り当てられたすべてのスプライトを更新する
        for event in pygame.event.get():
            if event.type == QUIT:      # 「閉じるボタン」を押したとき
                return True
            if event.type == KEYDOWN:   # キー入力があった時
                self.player.shoot(event.key)    # 押したキーに応じて弾を発射する
        return False

    def draw(self):
        # 描画処理
        # 画面を白に塗りつぶし
        self.screen.fill((255, 255, 255))   # 画面を塗りつぶす
        self.group.draw(self.screen)        # groupに割り当てられたすべてのスプライトを描画する(スプライトにself.imageがないとエラーが発生する)
        pygame.display.update()             # 画面を更新する