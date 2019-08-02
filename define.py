# coding:utf-8
from pygame.locals import Rect
from rek_time import ReK_time

"""Rekでの、それぞれのファイルに共通の定数を定義している"""

version = "1.0.1"

# ウィンドウのサイズ
WIDTH = 1160
HEIGHT = 600

# ステージ画面のサイズ
INFO_WIDTH = 200
STAGE_WIDTH = 960

# 初期画面におけるモード選択
START_GAME = 0          #START GAMEを選択した時
Help = 1                #Helpを選択した時
End = 2
BACK = 3

# メニュー画面におけるステージ名
Stage1 = "Stage1.txt"
Stage2 = "Stage2.txt"
Stage3 = "Stage3.txt" 

# 各ステージにおけるプレイヤー機体の初期位置
PLAYER_X = INFO_WIDTH + 100
PLAYER_Y = HEIGHT // 2

# stageにおける処理結果
EXIT = 100            # ウィンドウの「閉じるボタン」を押したとき
CONTINUE = 1        # ステージが続いているとき
GAMEOVER = 2        # ゲームオーバーになったとき
GAMECLEAR = 3       # ステージをクリアしたとき
RETIRE = 4

"""CPUの確認用定義。変数名とその値となる文字列は同じとする"""
CPU1 = "CPU1"
CPU2 = "CPU2"
CPU3 = "CPU3"
CPU4 = "CPU4"
CPU5 = "CPU5"
CPU6 = "CPU6"
CPU7 = "CPU7"
CPU8 = "CPU8"
CPU9 = "CPU9"
CPU10 = "CPU10"
CPU0 = "CPU0"
BOSS1 = "BOSS1"
BOSS2 = "BOSS2"

RECOVERY = "RECOVERY"
SHIELD = "SHIELD"
SPEEDDOWN = "SPEEDDOWN"
SCOREGET = "SCOREGET"
METEORITE = "METEORITE"

"""ステージルールの設定"""

# クリア条件:ステージの移動が止まるまで進み、画面内に残る敵機すべての撃破
# 失敗条件:自機が撃破される
NORMAL = "NORMAL"
SCORE_BASED = "SCORE_BASED"

#bossの座標調整のための設定
Move_range = Rect(600,40,STAGE_WIDTH/2,STAGE_WIDTH/2)
mg = Move_range
Correction = 10

# stage background
SKY = "SKY"
STAR = "STAR"

# timer
R_time = ReK_time()

data_key = {"money":int, "stage_progress":int, "version":str, "death":int, "kill":int, \
            "sum_money":int, "play_time":float, "gun_data":dict, "equip":list}