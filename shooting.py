#!/usr/bin/env python
# coding:utf-8

import pygame
from pygame.locals import *
import sys
import os
from stage import Stage
from initial_screen import Initial_Screen
from menu import Menu
import pygame.mixer
import database as db
from define import *
from help_explain import Help_a, Help_print
import json

class Main(pygame.sprite.Sprite):

    def __init__(self):
        """pygame、ウィンドウなどの初期化処理"""
        pygame.init()   # pygameの初期化
        self.data = db.load()
        self.data_check()
        print(self.data)

        if os.name == 'posix':
            # Linux系OSの場合
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)   # ウィンドウをWIDTH×HEIGHTで作成する
        if os.name == 'nt':
            # Windows
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))   # ウィンドウをWIDTH×HEIGHTで作成する
        
    def do(self):
         while True:
            init_screen = Initial_Screen()              #初期画面の描画              
            init_num = init_screen.draw(self.screen)    
            if init_num == EXIT:
                self.exit()

            if init_num == START_GAME:      #選択したモードがSTART GAMEならメニュー画面に移動

                while True:
                    menu = Menu(self.screen, self.data)    #メニュー画面の描画
                    stage_id, stageTxt = menu.draw()
                    if stage_id == EXIT:
                        self.exit()
                    if stage_id == None:
                        break
                    self.Stage_draw(stage_id, stageTxt)                
            elif init_num == Help:      #選択したモードがHelpならHelp画面に移動
                help_c = Help_a(self.screen)
                help_b = help_c.draw()
                if help_b == EXIT:
                    self.exit()
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

    def StageResult_draw(self, stage_id, result):
        """ステージ結果画面を描画する"""
        self.screen.fill((0,0,0))

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
            
    def _check_gun(self):
        dic = json.load(open("data/gun.json", "r"))
        i = 0
        for name, data in dic.items():
            if i in self.data['gun_data']:
                if self.data['version'] == '1.0.0' and i == 0:
                    data = self.data['gun_data']
                    data[0]['own'] = 1
                i += 1
                continue
            data['name'] = name
            data['own'] = int(i==0)
            self.data['gun_data'][i] = data
            i += 1

    def _check_equip(self):
        # 何も装備されていないとき、Gunを装備する
        if self.data['equip'] == []:
            self.data['equip'] = [0, -1, -1]
        

    def data_check(self):
        for key, cast in data_key.items():
            if key in self.data:
                self.data[key] = cast(self.data[key])
            else:
                self.data[key] = cast()
        self._check_gun()
        self._check_equip()

        # versionを最新に更新する
        self.data['version'] = version

    def exit(self):
        self.data["play_time"] += pygame.time.get_ticks()
        db.save(self.data)
        pygame.quit()
        sys.exit()

if __name__=='__main__':

    game = Main()
    game.do()
