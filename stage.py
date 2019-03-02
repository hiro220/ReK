#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from bullet import Bullet
from playermachine import PlayerMachine
from cpumachine import *
from define import *
from out_range import *

class Stage:

    def __init__(self, screen, filename):
        """screenは描画対象。filenameはステージ内容を記述したテキストファイル"""
        self.image = pygame.image.load("img/star.jpg").convert_alpha()              # 背景画像
        self.sub_image = pygame.image.load("img/star2.jpg").convert_alpha()         # 背景画像を左右反転させた、背景画像（自然につなげるため）
        self.rect = self.image.get_rect()       # 画像のrect情報
        self.screen = screen                    # 描画対象
        self.x = self.keyx = 0                  # 背景画像の左上の位置、ステージの進行度
        self.width, _ = self.rect.midright      # 背景画像のサイズ、_は使わない部分の値
        self.speed = 1                          # 背景の移動速度
        
        self.initGroup()                        # グループを初期化する

        self.readStage(filename)                # ステージ情報を読み込む

        self.crateRange()                       #範囲を設定する

        self.player = PlayerMachine(PLAYER_X, PLAYER_Y, self.cpus)    # プレイヤーのマシンを生成する

        self.clock = pygame.time.Clock()        # 時間管理用

    def initGroup(self):
        self.group = pygame.sprite.RenderUpdates()  # 描画する機体や弾用のグループ
        self.players = pygame.sprite.Group()        # playerの機体用グループ
        self.cpus = pygame.sprite.Group()           # cpuの機体用グループ
        self.ranges = pygame.sprite.Group()         # 画面の範囲外のspriteを格納したグループ

        PlayerMachine.containers = self.group, self.players     # プレイヤーマシンにグループを割り当てる
        CpuMachine.containers = self.group, self.cpus           # cpuマシンにグループを割り当てる
        Bullet.containers = self.group                          # 弾にグループを割り当てる
        Range.containers = self.ranges                          # 範囲にグループを割り当てる

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
        self.createCpu()                    # cpuの生成を行う
        self.moveStage()                    # ステージを動かす
        self.player.move(HEIGHT, WIDTH)     # 入力に応じてプレイヤーの機体を動かす
        self.group.update()                 # groupに割り当てられたすべてのスプライトを更新する

        pygame.sprite.groupcollide(self.group, self.ranges, True, False) # 画面外にできとグループから削除される

        if self.player.isGameOver():        # プレイヤーの機体が破壊されたとき
            print("GAMEOVER")
            return GAMEOVER

        if not bool(self.cpus) and self.keyx > self.size:
            print("GAMECLEAR")
            return GAMECLEAR                # グループcpusにあるすべてのcpuが破壊され、ステージ最後まで到達している

        for event in pygame.event.get():
            if event.type == QUIT:          # 「閉じるボタン」を押したとき
                return EXIT
            if event.type == KEYDOWN:       # キー入力があった時
                self.player.shoot(event.key)    # 押したキーに応じて弾を発射する
        return CONTINUE

    def moveStage(self):
        self.keyx += self.speed
        if self.keyx > self.size:         # 画面がステージサイズ分移動しているなら早期リターン
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
        """引数に指定したテキストファイルからステージ情報を読み込み、cpu情報をx座標がkeyとなる辞書型に格納する。（同様にアイテムの読み込みもできるはず）
        画面サイズがテキストファイルに記述されていない場合、初期値として0が代入される"""
        with open(file, 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く
            self.size = key = 0                         # 画面サイズと、辞書のkeyを0に初期化する
            self.dic = {}                               # 辞書を定義する
            for line in fp.readlines():                 # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                line = line.strip('\n').split()         # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                if len(line) == 1:                      # リストの要素数が1のとき、keyとなるx座標が記述されている
                    key = int(line[0])                  # 文字列をintに変換
                    self.dic[key] = []                  # 辞書にkeyを追加し、その値をリストとして初期化しておく
                    continue
                if len(line) == 2:                      # リストの要素数が2のとき、ステージサイズかcpu情報が記述されている(ここにアイテム追加も可)
                    if line[0] == 'size':               # 要素の一つ目がsizeのとき、二つ目の要素にステージサイズが記述されている
                        self.size = int(line[1])
                    else:                               # sizeでない場合はcpu(アイテム)なので、名前とy座標をリストにして辞書に追加
                        self.dic[key].append([line[0], int(line[1])])

    def createCpu(self):
        """現在のステージ位置にcpu(アイテム)があるならすべて生成する"""
        if self.keyx in self.dic:               # 辞書にself.xの値がキーになっている要素があるか
            x = WIDTH                           # あるとき、生成位置xを設定する
            for cpu in self.dic[self.keyx]:     # キーself.xにある要素を取り出す
                name = cpu[0]                   # 名前を設定
                y = cpu[1]                      # y座標を設定
                self.createOneCpu(name, x, y)   # 一つだけ生成

    def createOneCpu(self, name, x, y):
        """nameで指定されるcpu(アイテム)を(x, y)に生成。なお、nameはdefine.pyに定義された定数から選択"""
        if name == CPU1:
            cpu(x, y, self.players)
            return
        if name == CPU2:
            cpu2(x, y, self.players)
            return
        if name == CPU3:
            cpu3(x, y, self.players)
            return
    
    def crateRange(self):
        """ここでは範囲外を判定するための範囲を作成する"""
        Range(-10,0,10,600)
        Range(0,-10,960,10)
        Range(0,600,960,10)