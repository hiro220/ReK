from boss import Boss
import pygame
from define import *
from item import *
from gun import *
from timer import Timer

img_path = "img/cpu/"

"""
アイテムを利用するボス
--------------------
以下は実装案
-------------
・特定のアイテムを回収することで、ボスのシールド(もしくは無敵など)が解除される。
・銃による攻撃はなし(予定)
・嫌がらせのアイテムを大量に流す。
・通常のCPUを生成する。(別途作成するかについては未定)
・適度にCPU側にもアイテムを流す。
・シールドのアイテムが取れなくなる状態を利用して、シールドアイテムを取ると攻略が難しくなる。(自分からダメージを受けに行く)
-------------
以下は現状利用可能なアイテム
-------------
・Recovery(あまり流さない)
・ShieldItem(アイテムを取れなくする)
・SpeedDownItem(アイテムを取りに行きにくくする)
・SpeedUpItem(細かい移動を制限)
・ScoreGetItem(クリアとは関係なくスコアを伸ばすのもあり?　一定スコアで報酬など？)
・MeteoriteItem(ボスの攻撃手段? ボスへの攻撃手段?)
・PoisonItem(プレイヤーの体力を減らす)
・InvisibleItem(機体が見えなくなる。弾に当たる。アイテムも取れる)
"""

class Stage4_Boss(Boss):

    def __init__(self, x, y, players, score, money):
        image = pygame.image.load(img_path+"cpu.png").convert_alpha() #イメージ画像をロードする
        super().__init__(10, x, 300, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.dx, self.dy = -2, 0
        # 動作の実行中にTrueになる。Falseのときはどの動作も実行していない。
        self.action_flag = False

    def update(self):
        # 動作を選択する
        select = self.select_actions()
        # 選択された動作を実行
        self.action(select)
        # 移動する
        self.move(self.dx, self.dy)

    def select_actions(self):
        # 現在の状況などから、行動の選択、移動(self.dx, self.dy)の変更を行う
        action = None
        return action

    def action(self, select):
        # select_actionで選択された動作を実行する。
        pass

    def create_item(self):
        pass

    def move2straight(self, x, y):
        nowx, nowy = self.rect.center
        x = x - nowx
        y = y - nowy
        d = self.dx+self.dy
        self.dx = d * x / (x+y)
        self.dy = d * y / (x+y)

    def action_cancel(self):
        # 今実行中の動作をキャンセルする。
        # 一定時間行動しない
        pass

class CancelItem(Item):

    def __init__(self, x, y, machine, boss):
        image = 'img/item/recovery.png'
        super().__init__(x, y, image, machine)
        self.boss = boss

    def effect(self, machine):
        self.boss.action_cancel()
