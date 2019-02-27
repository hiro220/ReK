#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from bullet import Bullet
from playermachine import PlayerMachine
from cpumachine import *
from define import *

class Stage:

    def __init__(self, screen, filename):
        """screenは描画対象。filenameはステージ内容を記述したテキストファイル"""
        self.image = pygame.image.load("img/star.jpg").convert_alpha()              # 背景画像
        self.sub_image = pygame.image.load("img/star2.jpg").convert_alpha()         # 背景画像を左右反転させた、背景画像（自然につなげるため）
        self.rect = self.image.get_rect()       # 画像のrect情報
        self.screen = screen                    # 描画対象
        self.x = 0                              # 背景画像の左上の位置
        self.width, _ = self.rect.midright      # 背景画像のサイズ、_は使わない部分の値
        self.speed = 1                          # 背景の移動速度
        
        self.initGroup()

        self.readStage(filename)

        self.player = PlayerMachine(PLAYER_X, PLAYER_Y, self.cpus)    # プレイヤーのマシンを生成する

        self.clock = pygame.time.Clock()        # 時間管理用

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
            if not result == CONTINUE:
                break            
        return result

    def process(self):
        # 1フレームごとの処理
        self.createCpu()
        self.moveStage()
        self.player.move(HEIGHT, WIDTH)  # 入力に応じてプレイヤーの機体を動かす
        self.group.update()         # groupに割り当てられたすべてのスプライトを更新する
        for event in pygame.event.get():
            if event.type == QUIT:      # 「閉じるボタン」を押したとき
                return EXIT
            if event.type == KEYDOWN:   # キー入力があった時
                self.player.shoot(event.key)    # 押したキーに応じて弾を発射する
        return CONTINUE

    def moveStage(self):
        if self.x - 1 >= self.size:
            return
        self.x += self.speed                # ステージの位置を移動させる
        if self.x - 1 >= self.width:        # 画像が端までいったとき、背景画像と反転画像を入れ替えて、位置を初期化する
            self.x = 0
            tmp = self.image
            self.image = self.sub_image
            self.sub_image = tmp

    def draw(self):
        # 描画処理
        self.screen.blit(self.image, (-self.x, 0))                      # 背景画像の描画
        self.screen.blit(self.sub_image, (-self.x+self.width, 0))       # 対になる背景画像を繋げて描画

        self.group.draw(self.screen)        # groupに割り当てられたすべてのスプライトを描画する(スプライトにself.imageがないとエラーが発生する)
        pygame.display.update()             # 画面を更新する

    def readStage(self, file):
        with open(file, 'r', encoding="utf-8") as fp:
            key = 0
            self.dic = {}
            for line in fp.readlines():
                line = line.strip('\n').split()
                if len(line) == 1:
                    key = int(line[0])
                    self.dic[key] = []
                    continue
                if len(line) == 2:
                    if line[0] == 'size':
                        self.size = int(line[1])
                    else:
                        self.dic[key].append([line[0], line[1]])

    def createCpu(self):
        if self.x in self.dic:
            x = self.x + WIDTH
            for cpu in self.dic[self.x]:
                name = cpu[0]
                y = int(cpu[1])
                self.createOneCpu(name, x, y)

    def createOneCpu(self, name, x, y):
        if name == CPU1:
            CpuMachine(x, y, self.players)