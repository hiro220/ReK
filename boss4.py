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
        super().__init__(10, x, 287, image, players, score, money)         #superクラス(Boss)を呼び出す
        self.speed = 4
        # 動作の実行中にTrueになる。Falseのときはどの動作も実行していない。
        self.isaction = lambda var:False
        self.isaction_var = [None]
        self.timer_list = []
        self.section = 0
        self.tmp_section = self.section
        self.shield = Shield(90, self)

    def update(self):
        # 現在の状況などから動作を実行
        self.action()
        # 移動する
        self.move(self.dx, self.dy)

    def action(self):
        # 動作を実行する。
        if self.isaction(*self.isaction_var):
            return
        self.section += 1
        if self.section == 1:
            self._first_move()
        elif self.section == 2:
            self._item_creation()
        else:
            self._stop(5000)
            self.section = 1

    def create_item(self, item, flag=False):
        x, y = self.rect.left-10, self.rect.centery
        if flag:
            item(x, y, self.machines, self)
        else:
            item(x, y, self.machines)

    def move2straight(self, x, y):
        # 引数で指定した座標に向かうdx, dyに設定
        nowx, nowy = self.rect.center
        dx = x - nowx
        dy = y - nowy
        d = abs(dx)+abs(dy)
        if d == 0:
            return
        self.dx = self.speed * dx / d
        self.dy = self.speed * dy / d
        
    def _not_arrived(self, x, y):
        # (x, y)に到達していないならTrueが返る
        nx, ny = self.rect.center
        dx, dy = nx - x, ny - y
        if abs(dx)+abs(dy) < self.speed:
            return False
        return True

    def action_cancel(self):
        # 今実行中の動作をキャンセルする。
        # 一定時間行動しない
        self.timer_list.clear()
        self._stop(5000)

    def _first_move(self):
        self.move2straight(900, 300)
        self.isaction = self._not_arrived
        self.isaction_var = [900, 300]

    def _stop(self, millisecond):
        # アクションを一時停止し、millisecondaミリ秒後アクションを再開する。
        self.dx, self.dy = 0, 0
        self.isaction = lambda var:True
        self.isaction_var = [None]
        Timer(millisecond, self._action_start)

    def _action_start(self):
        # 次のアクションを強制的に開始する
        self.isaction = lambda var:False
        self.isaction_var = [None]

    def _item_creation(self):
        self._stop(5000)
        self.create_item(Recovery)
        self.timer_list.append(Timer(1000, self.create_item, ShieldBreakItem, True))
        self.timer_list.append(Timer(4000, self.create_item, ShieldBreakItem, True))

class CancelItem(Item):
    """bossの行動をキャンセルする"""
    def __init__(self, x, y, machine, boss):
        image = 'img/item/recovery.png'
        super().__init__(x, y, image, machine)
        self.boss = boss

    def effect(self, machine):
        self.boss.action_cancel()

class ShieldBreakItem(Item):
    """bossのシールドにダメージを与える"""
    def __init__(self, x, y, machine, boss):
        image = 'img/item/shield_break.png'
        super().__init__(x, y, image, machine)
        self.boss = boss

    def effect(self, machine):
        if self.boss.shield != None:
            self.boss.shield.hit(30)