# coding:utf-8

from rek_time import ReK_time

"""Rekでの、それぞれのファイルに共通の定数を定義している"""

# ウィンドウのサイズ
WIDTH = 960
HEIGHT = 600

# 初期画面におけるモード選択
START_GAME = 0          #START GAMEを選択した時
Help = 1                #Helpを選択した時

# メニュー画面におけるステージ名
Stage1 = "Stage1.txt"
Stage2 = "Stage2.txt"
Stage3 = "Stage3.txt" 

# 各ステージにおけるプレイヤー機体の初期位置
PLAYER_X = 100
PLAYER_Y = 300

# stageにおける処理結果
EXIT = 0            # ウィンドウの「閉じるボタン」を押したとき
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
CPU0 = "CPU0"

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

R_time = ReK_time()