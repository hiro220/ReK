#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from playermachine import PlayerMachine
from cpumachine import *
from bullet import Bullet

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化
        self.group = pygame.sprite.RenderUpdates()  # 描画する機体や弾用のグループ
        self.players = pygame.sprite.Group()        # playerの機体用グループ
        self.cpus = pygame.sprite.Group()           # cpuの機体用グループ

        PlayerMachine.containers = self.group, self.players     # プレイヤーマシンにグループを割り当てる
        CpuMachine.containers = self.group, self.cpus           # cpuマシンにグループを割り当てる
        Bullet.containers = self.group                          # 弾にグループを割り当てる

        self.screen = pygame.display.set_mode((960, 600))   # ウィンドウを960×600で作成する
        self.player = PlayerMachine(100, 300, self.cpus)    # プレイヤーのマシンを生成する

        cpu(900, 300, self.players)      # cpuの機体を生成
        cpu(900, 400, self.players)
        cpu(900, 100, self.players)

        cpu2(1500, 300, self.players)      # cpuの機体を生成
        cpu2(1500, 400, self.players)
        cpu2(1500, 100, self.players)

        cpu3(1000, 300, self.players)      # cpuの機体を生成
        cpu3(1000, 400, self.players)
        cpu3(1000, 100, self.players)

        self.clock = pygame.time.Clock()        # 時間管理用

        play_list = self.players.sprites()
        #print(play_list[1])


    def do(self):
        # メインループ
        while True:
            self.clock.tick(30)         # フレームレート(30fps)
            isClose = self.process()    # 内部処理
            self.draw()                 # 表示処理
            if isClose:     # もし内部処理で画面右上の「閉じるボタン」を押していた時、ループを抜ける
                break
        pygame.quit()       # 画面を閉じる
        sys.exit()          # システムを終了する

    def process(self):
        # 1フレームごとの処理
        self.player.move(600, 960)  # 入力に応じてプレイヤーの機体を動かす
        self.group.update()         # groupに割り当てられたすべてのスプライトを更新する

        if self.player.isGameOver():    # プレイヤーの機体が残っていない
            return True

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


if __name__=='__main__':

    game = Main()
    game.do()