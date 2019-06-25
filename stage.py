#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
from bullet import Bullet
from beam import Beam
from playermachine import PlayerMachine
from cpumachine import *
from item import *
from define import *
from out_range import *
from timer import Timer
from score import *
from money import *
import pygame.mixer

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

        self.creatRange()                       #範囲を設定する
        self.creatRange2()                      #
        
        font = pygame.font.Font("freesansbold.ttf", 60)
        menu_font = pygame.font.Font("freesansbold.ttf", 25)
        self.pause_text = font.render("PAUSE", True, (255,255,255))
        self.retire_text = menu_font.render("- Retire : Q", True, (255,255,255))
        self.restart_text = menu_font.render("- Restart : Space", True, (255,255,255))

        self.score = Score(10, 10)
        self.money = Money(10, 30)
        self.player = PlayerMachine(PLAYER_X, PLAYER_Y, self.cpus, Score(20, 20), Money(20, 20))    # プレイヤーのマシンを生成する

        self.clock = pygame.time.Clock()        # 時間管理用
        R_time.restart()

        self.process = self.stage_process
        self.draw = self.stage_draw
        

    def initGroup(self):
        self.group = pygame.sprite.RenderUpdates()  # 描画する機体や弾用のグループ
        self.players = pygame.sprite.Group()        # playerの機体用グループ
        self.cpus = pygame.sprite.Group()           # cpuの機体用グループ
        self.bullets = pygame.sprite.Group()        # bulletのグループ
        self.beams = pygame.sprite.Group()          # beamのグループ
        self.ranges = pygame.sprite.Group()         # 画面の範囲外のspriteを格納したグループ
        self.ranges2 = pygame.sprite.Group()        # 画面の範囲外のspriteを格納したグループ
        self.timers = pygame.sprite.Group()

        PlayerMachine.containers = self.group, self.players     # プレイヤーマシンにグループを割り当てる
        CpuMachine.containers = self.group, self.cpus           # cpuマシンにグループを割り当てる
        Bullet.containers = self.group                          # 弾にグループを割り当てる
        Item.containers = self.group
        Bullet.containers = self.group, self.bullets            # 弾にグループを割り当てる
        Beam.containers = self.group, self.beams
        Range.containers = self.ranges                          # 範囲にグループを割り当てる
        Range2.containers = self.ranges2                        # 範囲にグループを割り当てる
        Timer.containers = self.timers

    def loop(self):
        while True:
            self.clock.tick(30)         # フレームレート(30fps)
            result = self.process()
            self.draw()
            if not result == CONTINUE:
                break            
        return result

    def stage_process(self):
        # 1フレームごとの処理
        self.createCpu()                    # cpuの生成を行う
        self.moveStage()                    # ステージを動かす
        self.player.move(HEIGHT, WIDTH)     # 入力に応じてプレイヤーの機体を動かす
        self.group.update()                 # groupに割り当てられたすべてのスプライトを更新する
        self.timers.update()

        pygame.sprite.groupcollide(self.cpus, self.ranges, True, False) # 画面外にでるとグループから削除される
        pygame.sprite.groupcollide(self.bullets, self.ranges2, True, False) # 画面外にでるとグループから削除される

        if self.isGameOver():
            pygame.mixer.music.stop()
            return GAMEOVER                 # ゲームオーバー条件が満たされた
        if self.isClear():
            pygame.mixer.music.stop()
            return GAMECLEAR                # ゲームクリア条件が満たされた
        for event in pygame.event.get():
            if event.type == QUIT:          # 「閉じるボタン」を押したとき
                return EXIT
            if event.type == KEYDOWN:       # キー入力があった時
                if event.key == K_SPACE:
                    R_time.stop()
                    pygame.mixer.music.pause()
                    self.process, self.draw = self.pause_process, self.pause_draw
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

    def stage_draw(self):
        # 描画処理
        self.screen.blit(self.image, (-self.x, 0))                      # 背景画像の描画
        self.screen.blit(self.sub_image, (-self.x+self.width, 0))       # 対になる背景画像を繋げて描画

        self.group.draw(self.screen)        # groupに割り当てられたすべてのスプライトを描画する(スプライトにself.imageがないとエラーが発生する)
        self.score.draw(self.screen)
        self.money.draw(self.screen)
        pygame.display.update()             # 画面を更新する

    def pause_process(self):
        for event in pygame.event.get():
            if event.type == QUIT:          # 「閉じるボタン」を押したとき
                return EXIT
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.mixer.music.unpause()
                    R_time.restart()
                    self.process, self.draw = self.stage_process, self.stage_draw
                elif event.key == K_q:
                    return RETIRE
        return CONTINUE

    def pause_draw(self):
        self.screen.blit(self.pause_text, [WIDTH/2-80, HEIGHT/4])
        self.screen.blit(self.restart_text, [WIDTH/2-80, HEIGHT/4+100])
        self.screen.blit(self.retire_text, [WIDTH/2-80, HEIGHT/4+150])
        pygame.display.update()

    def readStage(self, file):
        """引数に指定したテキストファイルからステージ情報を読み込み、cpu情報をx座標がkeyとなる辞書型に格納する。（同様にアイテムの読み込みもできるはず）
        画面サイズがテキストファイルに記述されていない場合、初期値として0が代入される"""
        with open(file, 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く
            self.size = key = 0                         # 画面サイズと、辞書のkeyを0に初期化する
            self.dic = {}                               # 辞書を定義する
            self.setRule(NORMAL)                        # ステージルールをNORMALに設定する。
            for line in fp.readlines():                 # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                line = line.strip('\n').split()         # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                if len(line) == 1:                      # リストの要素数が1のとき、keyとなるx座標が記述されている
                    key = int(line[0])                  # 文字列をintに変換
                    self.dic[key] = []                  # 辞書にkeyを追加し、その値をリストとして初期化しておく
                    continue
                if len(line) == 2:                      # リストの要素数が2のとき、ステージサイズかcpu情報が記述されている(ここにアイテム追加も可)
                    if line[0] == 'size':               # 要素の一つ目がsizeのとき、二つ目の要素にステージサイズが記述されている
                        self.size = int(line[1])
                    elif line[0] == 'rule':             # 要素の一つ目がruleのとき、二つ目の要素にルールを示す定数が記述されている
                        self.setRule(line[1])           # ルールをセットする
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
        # 辞書の定義。キーに定数、値にクラス名を指定する。（キー:値）

        # CPUの種類を指す辞書
        cpu_dic = {CPU1:cpu, CPU2:cpu2, CPU3:cpu3, CPU0:cpu0}
        # アイテムの種類を指す辞書
        item_dic = {RECOVERY:Recovery, SHIELD:ShieldItem, SPEEDDOWN:SpeedDownItem, SCOREGET:ScoreGetItem}
        sub = name.split('_')

        if sub[0] == 'CPU' and sub[1] in item_dic:      # CPU_〇〇という呼ばれ方をしたアイテムか
            # CPU用のアイテム生成
            cpu_item = item_dic[sub[1]]
            cpu_item(x, y, self.cpus)
        if name in cpu_dic:                             # 辞書にキーnameがあるか
            create_cpu = cpu_dic[name]                      # 変数createにクラス名を代入。
            create_cpu(x, y, self.players, self.score, self.money)              # 変数createに代入されているクラスを呼び出す。
        if name in item_dic:
            create_item = item_dic[name]
            create_item(x, y, self.players)
    
    def creatRange(self):
        """ここでは範囲外を判定するための範囲を作成する"""
        Range(-100,-100,10,HEIGHT+50)
        #Range(0,-10,WIDTH,10)
        #Range(0,HEIGHT,WIDTH,10)
    
    def creatRange2(self):
        """ここでは範囲外を判定するための範囲を作成する"""
        Range2(-20,0,10,HEIGHT)
        Range2(-10,-20,WIDTH+20,10)
        Range2(-10,HEIGHT+10,WIDTH+20,10)
        Range2(WIDTH+10,0,10,HEIGHT)

    def setRule(self, name):
        """nameに指定したdefine.pyに定義のある定数に応じてルールの設定を行う。
        辞書型リストのキーに定数、値に関数名のリストを設定しておく。リストは[クリア条件, 失敗条件]に相当する関数を指定する。
        指定する関数は、引数なし、bool型の返却値を取る"""
        dic = {NORMAL:[self.normalRule, self.playerBreak]}
        if name in dic:
            ruleList = dic[name]
            self.isClear = ruleList[0]
            self.isGameOver = ruleList[1]

    def normalRule(self):
        """ステージが画面端まで移動し、画面に残っている敵機をすべて破壊すればTrueが返る"""
        isCpuRemain = bool(self.cpus)                           # cpuが画面内に残っているか
        return not isCpuRemain and self.keyx > self.size        # 上記条件かつ、ステージが最後に達しているか

    def playerBreak(self):
        """プレイヤーの機体が破壊されるとTrueが返る"""
        return self.player.isGameOver()