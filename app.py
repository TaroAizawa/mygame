# C:/users/zat_a/game
# -*- coding: utf-8 -*-
import pyxel
import numpy as np
import math
import json
from title import Title
from stage_select import StageSelect
from stage import Stage

# 場面の定義：アプリ
TITLE = 0
STAGE_SELECT = 1
STAGE = 2

class App():
    def __init__(self):
        # pyxelの初期設定
        self.scene = STAGE_SELECT
        self.scene_last = TITLE
        self.size_x = 256
        self.size_y = 256
        self.fps = 30
        self.stage_settings_json = json.load(open('stage_setting.json', 'r'))
        self.selected_stage = None
        pyxel.init(self.size_x, self.size_y, caption="IRAIRA-CHASE!", scale=5, fps=self.fps, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("for_mygame.pyxres")
        # pyxel起動
        pyxel.run(self.update, self.draw)

    def update(self):
        # ===== タイトル画面 =====
        if self.scene == TITLE:
            if self.scene_last != TITLE:
                self.title = Title()
            self.title.update_title()
            self.scene_last = TITLE
        # ===== ステージセレクト画面 =====
        elif self.scene == STAGE_SELECT:
            if self.scene_last != STAGE_SELECT:
                self.stage_select = StageSelect(self.size_x, self.size_y, self.stage_settings_json)
            self.selected_stage = self.stage_select.update_stage_select()
            if not self.stage_select.activate:
                self.scene = STAGE
            self.scene_last = STAGE_SELECT
        # ===== ステージ =====
        elif self.scene == STAGE:
            if self.scene_last == STAGE_SELECT:
                self.stage = Stage(self.size_x, self.size_y,
                           self.selected_stage["player_args"], self.selected_stage["chaser_args"], self.selected_stage["wall_args"])
                self.stage.set_frame0()
            self.stage.update_Stage()
            if not self.stage.activate:
                del(self.stage)
                self.scene = STAGE_SELECT
            self.scene_last = STAGE
            
    def draw(self):
        pyxel.cls(0)
        # ===== タイトル画面 =====
        if self.scene == TITLE:
            if self.scene_last == TITLE:
                self.title.draw_title()
        # ===== ステージセレクト画面 =====
        elif self.scene == STAGE_SELECT:
            if self.scene_last == STAGE_SELECT:
                self.stage_select.draw_stage_select()
        # ===== ステージ =====          
        elif self.scene == STAGE:
            if self.scene_last == STAGE:        
                self.stage.draw_Stage()
        pyxel.text(10, 50, f"scene:{self.scene}", 8)

      
if __name__ == "__main__":
    App()