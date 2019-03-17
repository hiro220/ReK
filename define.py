# coding:utf-8

"""Rekでの、それぞれのファイルに共通の定数を定義している"""

# ウィンドウのサイズ
WIDTH = 960
HEIGHT = 600

# 初期画面におけるモード選択
START_GAME = 0          #START GAMEを選択した時
Help = 1                #Helpを選択した時

# 各ステージにおけるプレイヤー機体の初期位置
PLAYER_X = 100
PLAYER_Y = 300

# stageにおける処理結果
EXIT = 0            # ウィンドウの「閉じるボタン」を押したとき
CONTINUE = 1        # ステージが続いているとき
GAMEOVER = 2        # ゲームオーバーになったとき
GAMECLEAR = 3       # ステージをクリアしたとき

"""CPUの確認用定義。変数名とその値となる文字列は同じとする"""
CPU1 = "CPU1"
CPU2 = "CPU2"
CPU3 = "CPU3"

RECOVERY = "RECOVERY"
SHIELD = "SHIELD"

"""ステージルールの設定"""
NORMAL = "NORMAL"