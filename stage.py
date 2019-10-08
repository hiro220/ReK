#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame import gfxdraw
from pygame.locals import *
from bullet import Bullet
from beam import Beam
from playermachine import PlayerMachine
from cpumachine import *
from item import *
from define import *
from out_range import Range, Range2
from timer import Timer
from score import Score
from boss import Stage1_boss
from boss2 import *
from money import Money
from popupwindow import PopupWindow
import pygame.mixer

class Stage:

    def __init__(self, screen, filename, data, continue_num=0):
        """screenは描画対象。filenameはステージ内容を記述したテキストファイル"""
        self.screen = screen                    # 描画対象
        self.speed = 1                          # 背景の移動速度
        self.continue_num = continue_num
        self.data = data

        CpuMachine.killed_count = self.data["kill"]
        Boss.killed_count = 0
        PlayerMachine.killed_count = self.data["death"]
        
        self.initGroup()                        # グループを初期化する

        self.readStage(filename)                # ステージ情報を読み込む

        self.creatRange()                       #範囲を設定する
        self.creatRange2()                      #
        
        font = pygame.font.Font("font/freesansbold.ttf", 60)
        menu_font = pygame.font.Font("font/freesansbold.ttf", 25)
        self.pause_text = font.render("PAUSE", True, (255,255,255))
        self.retire_text = menu_font.render("- Retire : Q", True, (255,255,255))
        self.restart_text = menu_font.render("- Restart : Space", True, (255,255,255))

        self.score = Score(10, 10)
        self.money = Money(10, 30)
        self.clock = pygame.time.Clock()        # 時間管理用
        R_time.restart()

        self.process = self.stage_process
        self.draw = self.stage_draw

        self.player_init()


    def initGroup(self):
        self.group = pygame.sprite.RenderUpdates()  # 描画する機体や弾用のグループ
        self.players = pygame.sprite.Group()        # playerの機体用グループ
        self.cpus = pygame.sprite.Group()           # cpuの機体用グループ
        self.bullets = pygame.sprite.Group()        # bulletのグループ
        self.ranges = pygame.sprite.Group()         # 画面の範囲外のspriteを格納したグループ
        self.ranges2 = pygame.sprite.Group()        # 画面の範囲外のspriteを格納したグループ
        self.timers = pygame.sprite.Group()
        self.cpus2 = pygame.sprite.Group()
        self.players2 = pygame.sprite.Group()
        
        PlayerMachine.containers = self.group, self.players2, self.players     # プレイヤーマシンにグループを割り当てる
        CpuMachine.containers = self.group, self.cpus2, self.cpus           # cpuマシンにグループを割り当てる
        Item.containers = self.group
        Bullet.containers = self.bullets            # 弾にグループを割り当てる
        Beam.containers = self.bullets
        Range.containers = self.ranges                          # 範囲にグループを割り当てる
        Range2.containers = self.ranges2                        # 範囲にグループを割り当てる
        Timer.containers = self.timers
        Boss.containers = self.group, self.cpus2, self.cpus

    def loop(self):
        while True:
            self.clock.tick(30)         # フレームレート(30fps)
            result = self.process()
            self.draw()
            pygame.display.update()     # 画面更新
            if not result == CONTINUE:
                break
        self.data["kill"] = CpuMachine.killed_count + Boss.killed_count
        self.data["death"] = PlayerMachine.killed_count
        return result, self.score.return_score(), self.money.money

    def stage_process(self):
        # 1フレームごとの処理
        self.createCpu()                    # cpuの生成を行う
        self.moveStage()                    # ステージを動かす
        self.player.move()     # 入力に応じてプレイヤーの機体を動かす
        self.group.update()                 # groupに割り当てられたすべてのスプライトを更新する
        self.bullets.update()
        self.timers.update()

        pygame.sprite.groupcollide(self.cpus, self.ranges, True, False) # 画面外にでるとグループから削除される
        pygame.sprite.groupcollide(self.bullets, self.ranges2, True, False) # 画面外にでるとグループから削除される

        # ゲームオーバー条件が満たされた
        if self.isGameOver():

            pygame.mixer.music.pause()
            R_time.stop()
            # コンティニューするか
            if self.select_continued():
                R_time.restart()
                pygame.mixer.music.unpause()
                self.player_init(continued=True)
                self.continue_num -= 1
                self.player.invincible(2000)
            else:
                pygame.mixer.music.stop()
                return GAMEOVER

        # ゲームクリア条件が満たされた
        if self.isClear():
            pygame.mixer.music.stop()
            return GAMECLEAR
          
        for event in pygame.event.get():
            if event.type == QUIT:          # 「閉じるボタン」を押したとき
                return EXIT
            if event.type == KEYDOWN:       # キー入力があった時
                if event.key == K_SPACE:
                    R_time.stop()
                    pygame.mixer.music.pause()
                    self.process, self.draw = self.pause_process, self.pause_draw
                if event.key == K_x or event.key == K_v:
                    self.player.shoot(event.key)    # 押したキーに応じて弾を発射する
                if event.key == K_a or event.key == K_s or event.key == K_d:
                    self.player.change(event.key)
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
        self.bullets.draw(self.screen)
        self.draw_info()

    def draw_info(self):
        # infoエリアの作成
        bg = (60, 60, 60)
        pygame.draw.rect(self.screen, bg, Rect(0,0,INFO_WIDTH, HEIGHT))
        # 枠線描画
        pygame.draw.rect(self.screen, (255,255,255), Rect(0,0,INFO_WIDTH, HEIGHT), 5)
        # 各エリアを分割
        pygame.draw.line(self.screen, (255,255,255), (0,85), (INFO_WIDTH,85))   # scoreエリア:80
        pygame.draw.line(self.screen, (255,255,255), (0,285), (INFO_WIDTH,285)) # HPエリア:200
        pygame.draw.line(self.screen, (255,255,255), (0,535), (INFO_WIDTH,535)) # bulletエリア:250, itemエリア:60

        # scoreエリアに獲得スコアと獲得金額の描画
        self.score.draw(self.screen)
        self.money.draw(self.screen)

        # HPエリアの描画
        cx, cy = 100, 210
        # 体力ゲージの表示割合計算
        hp, maxhp = self.player.hp.hp, self.player.hp.maxhp
        par = hp / maxhp
        rad = (math.pi * 5/4) - par * math.pi * 3/2
        x, y = math.cos(rad)*70+cx, -math.sin(rad)*70+cy
        # HPゲージ
        r = 255*(par<0.5) or int(255*(1-par)*2)
        g = 255*(par>0.5) or int(255*par*2)
        pygame.draw.circle(self.screen, (r,g,0), (cx, cy), 70, 30)
        # 円が内接する四角形の左下座標から右下座標まで、角の座標
        pol_list = [(cx-70,cy+70), (cx-70, cy-70), (cx+70, cy-70), (cx+70, cy+70)]
        # 体力の割合に応じて、必要のない座標をリストから取り除く
        pos = int(par * 6+1) // 2
        del pol_list[:pos]
        # リストに円の中心座標、体力ゲージの表示する部分までの座標を追加
        pol_list.insert(0, (cx, cy))
        pol_list.insert(1, (x, y))
        # ポリゴンで、残HPに応じて円に背景色を上書きする
        pygame.draw.polygon(self.screen, bg, pol_list)
        # HPゲージの枠を描画
        outline = (255, 255, 255)
        pygame.draw.circle(self.screen, outline, (cx, cy), 70, 3)
        pygame.draw.circle(self.screen, outline, (cx, cy), 40, 3)
        pygame.draw.polygon(self.screen, bg, [(cx,cy), (cx+70, cy+70), (cx-70, cy+70)])
        l_rad, r_rad = math.pi * 5/4, -math.pi / 4
        for rad in (l_rad, r_rad):
            pygame.draw.line(self.screen, outline, (math.cos(rad)*67+cx, -math.sin(rad)*67+cy), \
                                                   (math.cos(rad)*37+cx, -math.sin(rad)*37+cy), 4)
        # HP量のメモリ表示
        for i in range(int(maxhp+0.5)):
            rad = (((maxhp-i)/maxhp) * (3/2) - 1/4) * math.pi
            pygame.draw.line(self.screen, outline, (math.cos(rad)*45+cx, -math.sin(rad)*45+cy), \
                                                   (math.cos(rad)*37+cx, -math.sin(rad)*37+cy), 3)
        # 飛行機のシルエット描画
        image = pygame.image.load("img/machine_icon.png").convert_alpha()
        self.screen.blit(image, (10, 90))

        # bulletエリア
        for i in range(3):
            gun = self.player.gun_file[i]
            istarget = (self.player.gun_number-1 == i)
            r_num, max_rnum = self.player.reload_num[i], self.player.reload_max[i]
            if gun == None:
                num, maxnum = 0, 1
            else:
                num, maxnum = gun.num, gun.max
            # 残弾数描画
            par = num / maxnum
            pygame.draw.rect(self.screen, (0,0,155+100*istarget), Rect(15, 340+60*i, 150*par, 20))
            pygame.draw.rect(self.screen, (205+50*istarget,)*3, Rect(15, 340+60*i, 150, 20), 3*istarget or 2)
            for j in range(maxnum):
                x = 15+150*j/maxnum
                pygame.draw.line(self.screen, (205+50*istarget,)*3, (x, 340+60*i), (x, 360+60*i))
            # 残リロード数描画
            par = r_num / (max_rnum or 1)
            pygame.draw.rect(self.screen, (155+100*istarget,0,0), Rect(15, 360+60*i, 140*par, 10))
            pygame.draw.rect(self.screen, (205+50*istarget,)*3, Rect(15, 360+60*i, 140, 10), 2)
            for j in range(max_rnum):
                x = 15+140*j/max_rnum
                pygame.draw.line(self.screen, (205+50*istarget,)*3, (x, 360+60*i), (x, 370+60*i))

    def select_continued(self):
        self.draw()
        pygame.display.update()
        # コンティニューできるか
        if self.continue_num > 0:
            # 表示する文字の設定
            text = "コンティニューしますか?\nあと" + str(int(self.continue_num)) + "回"
            if PopupWindow(self.screen, text, ['はい', 'いいえ'], target=1).loop() == 0:
                return True
            else:
                return False
        else:
            # コンティニューできない
            return False

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

    def readStage(self, file):
        """引数に指定したテキストファイルからステージ情報を読み込み、cpu情報をx座標がkeyとなる辞書型に格納する。（同様にアイテムの読み込みもできるはず）
        画面サイズがテキストファイルに記述されていない場合、初期値として0が代入される"""
        with open(file, 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く
            self.size = key = 0                         # 画面サイズと、辞書のkeyを0に初期化する
            self.dic = {}                               # 辞書を定義する
            # ステージ初期設定
            self.setRule(NORMAL)                        # ステージルールをNORMALに設定する。
            self.set_background(SKY)                    # 背景をSKYに初期化
            # ファイルから情報を抽出し、ステージの形成
            loop_key = line_num = 0
            lines = True                                # ファイルの一行を格納する変数の初期化(while文の条件に使う)
            while lines:
                lines = fp.readline()                   # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                line_num += len(lines)                  # 文字数をカウント(ファイルポインタの移動に使う)
                line = lines.strip('\n').split()        # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                if len(line) == 1:                      # リストの要素数が1のとき、keyとなるx座標が記述されている
                    key = int(line[0]) + loop_key       # 文字列をintに変換
                    self.dic[key] = []                  # 辞書にkeyを追加し、その値をリストとして初期化しておく
                    continue
                if len(line) >= 2:                      # リストの要素数が2のとき、ステージサイズかcpu情報が記述されている(ここにアイテム追加も可)
                    if line[0] == '#':          # コメントアウト
                        pass
                    elif line[0] == 'size':             # 要素の一つ目がsizeのとき、二つ目の要素にステージサイズが記述されている
                        self.size = int(line[1])
                    elif line[0] == 'rule':             # 要素の一つ目がruleのとき、二つ目の要素にルールを示す定数が記述されている
                        self.setRule(*line[1:])         # ルールをセットする
                    elif line[0] == 'bg':
                        self.set_background(line[1])    # 背景画像の設定
                    elif line[0] == 'loop':
                        loop_count = int(line[1])
                        loop_pos = line_num             # この行の次行の位置を保持
                    elif line[0] == 'endloop':
                        loop_count -= 1
                        if loop_count == 0:
                            loop_key = 0
                        else:
                            fp.seek(loop_pos)           # loop行の直後にファイルポインタを移動
                            line_num = loop_pos         # 文字数のカウントをそこまでにリセット
                            loop_key += int(line[1])    # endloopのオプションをx座標に足す
                    else:                               # sizeでない場合はcpu(アイテム)なので、名前とy座標をリストにして辞書に追加
                        if len(line) >= 3:
                            line[1] = random.randrange(int(line[1]), int(line[2])+1)
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
        cpu_dic = {CPU1:cpu, CPU2:cpu2, CPU3:cpu3, CPU4:cpu4, CPU5:cpu5, CPU6:cpu6, CPU7:cpu7, CPU8:cpu8, \
                   CPU9:cpu9, CPU10:cpu10, CPU0:cpu0, BOSS1:Stage1_boss, BOSS2:Stage2_boss}

        # アイテムの種類を指す辞書
        item_dic = {RECOVERY:Recovery, SHIELD:ShieldItem, SPEEDDOWN:SpeedDownItem, SCOREGET:ScoreGetItem, \
                    METEORITE:MeteoriteItem}
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
        Range(INFO_WIDTH-100,-50,20,HEIGHT+100)
        Range(0,-70,WIDTH+200,20)
        Range(0,HEIGHT+50,WIDTH+200,20)
        Range(WIDTH+200,-50,20,HEIGHT+100)
    
    def creatRange2(self):
        """ここでは範囲外を判定するための範囲を作成する"""
        Range2(INFO_WIDTH-WIDTH,-80,50,HEIGHT+160)
        Range2(INFO_WIDTH-WIDTH+10,-80,WIDTH*3-INFO_WIDTH,50)
        Range2(INFO_WIDTH-WIDTH+10,HEIGHT+80,WIDTH*3-INFO_WIDTH,50)
        Range2(WIDTH*2,-80,50,HEIGHT+160)

    def set_background(self, image_id):
        dic = {SKY:"sky.jpg", STAR:"star.jpg"}
        if image_id not in dic:
            return
        path = "img/bg/" + dic[image_id]
        self.image = pygame.image.load(path).convert_alpha()              # 背景画像
        self.sub_image = pygame.transform.flip(self.image, True, False)         # 背景画像を左右反転させた、背景画像（自然につなげるため）
        self.rect = self.image.get_rect()       # 画像のrect情報
        self.x = self.keyx = -20                # 背景画像の左上の位置、ステージの進行度
        self.width, _ = self.rect.midright      # 背景画像のサイズ、_は使わない部分の値

    def setRule(self, name, value=None):
        """nameに指定したdefine.pyに定義のある定数に応じてルールの設定を行う。
        辞書型リストのキーに定数、値に関数名のリストを設定しておく。リストは[クリア条件, 失敗条件]に相当する関数を指定する。
        指定する関数は、引数なし、bool型の返却値を取る"""
        dic = {NORMAL:[self.normalRule, self.playerBreak], SCORE_BASED:[self.scoreWin, self.otherwise]}
        if name in dic:
            ruleList = dic[name]
            self.isClear = ruleList[0]
            self.isGameOver = ruleList[1]
        if value:
            self.rule_value = int(value)

    def normalRule(self):
        """ステージが画面端まで移動し、画面に残っている敵機をすべて破壊すればTrueが返る"""
        isCpuRemain = bool(self.cpus2)                           # cpuが画面内に残っているか
        return not isCpuRemain and self.keyx > self.size        # 上記条件かつ、ステージが最後に達しているか

    def playerBreak(self):
        """プレイヤーの機体が破壊されるとTrueが返る"""
        return self.player.isGameOver()

    def scoreWin(self):
        return self.score.score >= self.rule_value

    def otherwise(self):
        return self.normalRule() or self.playerBreak()

    def player_init(self, continued=False):
        chips = self.data['chip']
        # プレイヤーのマシンを生成する
        self.player = PlayerMachine(PLAYER_X, PLAYER_Y, self.cpus, Score(20, 20), Money(20, 20), self.data)
        i = 0
        for chip in chips:
            if chip < 0:
                continue
            size = self.data['chip_data'][chip]['equip_size']
            chip = self.data['chip_data'][chip]['name']
            i += 1
            if i < size:
                continue
            i = 0
            if chip == 'HP_UP':
                self.player.hp.maxhp += 0.5
                self.player.recover(0.5)
            elif chip == 'CONTINUE' and continued==False:
                # コンティニューは三つ枠を取っているから、三度実行される
                self.continue_num += 1
            elif chip == 'SPEEDUP':
                self.player.dx += 1
                self.player.dy += 1
            elif chip == "SHORT_RELOAD":
                self.player.reload_time -= 150
            elif chip == "SHIELD":
                Shield(3, self.player)
            elif chip == "LONG_INVISIBLE":
                self.player.invincible_time += 100