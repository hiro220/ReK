#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
from stage import Stage
from initial_screen import Initial_Screen
from menu import Menu
import pygame.mixer
import database as db
from define import *
from help_explain import Help_a, Help_print
from shop import *

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化
        self.data = db.load()
        self.data_check()
        print(self.data)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)   # ウィンドウをWIDTH×HEIGHTで作成する
        self.shop = Shop(self.screen)

    def do(self):
         while True:
            init_screen = Initial_Screen()              #初期画面の描画              
            init_num = init_screen.draw(self.screen)    

            if init_num == START_GAME:      #選択したモードがSTART GAMEならメニュー画面に移動

                while True:
                    menu = Menu(self.screen)    #メニュー画面の描画
                    stage_id, stageTxt = menu.draw()
                    if stage_id == None:
                        break
                    elif stageTxt == "1":
                        shop = self.shop.draw()
                    else:
                        self.Stage_draw(stage_id, stageTxt)             
            elif init_num == Help:      #選択したモードがHelpならHelp画面に移動
                help_c = Help_a(self.screen)
                help_b = help_c.draw()
            elif init_num == End:
                self.exit()

    def Stage_draw(self, stage_id, stageTxt):
        stage_file = "stage/" + stageTxt
        stage = Stage(self.screen, stage_file, self.data)
        pygame.mixer.music.load("sound/sound1.mp3")     # 音楽ファイルの読み込み
        pygame.mixer.music.play(-1)                     # 音楽の再生回数(ループ再生)
        result = stage.loop()
        if result[0] == EXIT:
            self.exit()
        elif result[0] == RETIRE:
            return
        self.StageResult_draw(stage_id, result)
        return

    def StageResult_draw(self, stage_id, result):
        """ステージ結果画面を描画する"""
        self.screen.fill((0,0,0))

        Score_font = pygame.font.Font("freesansbold.ttf", 50)
        Enter_font = pygame.font.Font("freesansbold.ttf", 20)

        #Score_text = Score_font.render("SCORE: " + str(result[1]), True, (255,255,255))
        Enter_text = Enter_font.render("ENTER:RETURN", True, (255,255,255))

        #self.screen.blit(Score_text, [460, 500])
        self.screen.blit(Enter_text, [5, 5])
        result, score, money = result

        if result == GAMECLEAR:
            if self.data["stage_progress"] < stage_id:
                self.data["stage_progress"] = stage_id
            image = pygame.image.load("img/gameclear.jpg").convert_alpha()
            self.screen.blit(image, [255, 50])
            self.data["money"] += money
            self.data["sum_money"] += money
            db.insert_score(stage_id, score)
            self.draw_ranking(db.load_ranking(stage_id))
        elif result == GAMEOVER:
            image = pygame.image.load("img/gameover.jpg").convert_alpha()
            self.screen.blit(image, [270, 10])

        while True:
            pygame.display.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return 
                if event.type == QUIT:
                    self.exit()
        
    def draw_ranking(self, ranking):
        # 新しいデータ順にソート
        ranking = sorted(ranking, key=lambda x:x[0], reverse=True)
        # スコアの高い順にソート
        ranking = sorted(ranking, key=lambda x:x[1], reverse=True)
        # 今回の結果データを抽出
        this_score = max(ranking, key=lambda x:x[0])
        pre_score = -1
        rank = 0
        pos = 0
        for i, data in enumerate(ranking):
            if pre_score != data[1]:
                pre_score = data[1]
                rank = i+1
            color = (255,255,255)
            if this_score[0] == data[0]:
                color = (255,0,0)
            if i < 5 or this_score[0]==data[0]:
                score = pygame.font.Font("freesansbold.ttf", 50).render(str(rank) + " : " + str(data[1]), True, color)
                self.screen.blit(score, [550, 180+50*(pos+1)])
                pos += 1
            
    def data_check(self):
        for key, cast in data_key.items():
            if key in self.data:
                self.data[key] = cast(self.data[key])
            else:
                self.data[key] = cast()
        self.data['version'] = version

    def exit(self):
        self.data["play_time"] += pygame.time.get_ticks()
        db.save(self.data)
        pygame.quit()
        sys.exit()

if __name__=='__main__':

    game = Main()
    game.do()
