# C:/users/zat_a/game
# -*- coding: utf-8 -*-
import pyxel
import math
import numpy as np

class App:
    """pyxelを使用したアプリケーション

    """
    def __init__(self):
        """コンストラクタ

        pyxelの設定とpyxresファイルの読み込み、
        その後pyxel起動。
        1フレーム毎にupdateとdrawが実行される。
        """
        self.size_x = 256
        self.size_y = 256
        pyxel.init(self.size_x, self.size_y, caption="test!", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("test.pyxres")
        self.player = Player()
        self.chaser = Chaser(50, 50, 8)
        pyxel.run(self.update, self.draw)

    def update(self):
        """pyxelの更新処理。
        
        座標などの計算はここに記述。
        """
        # 画面から出ないポインターの処理
        self.player.check(self.size_x, self.size_y, pyxel.mouse_x, pyxel.mouse_y)
        # 追跡者の処理
        self.chaser.set_new_vector(self.player.x, self.player.y, pyxel.frame_count)
        # 追跡者とプレイヤーの当たり判定
        if self.chaser.dxy < self.player.r+self.chaser.r:
            self.flag.gameover = True
        self.chaser.set_new_coords()
        # Qキーで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self): 
        """pyxelの描画処理。
        
        描画系の処理は全てここに記述。
        """
        # 画面を色１でクリア
        pyxel.cls(1)
        #  == 以下で新たに描画していく ==
        # システム背景
        pyxel.rect(0, 0, self.size_x, 48, 2)
        # 確認用テキスト：経過フレーム数、マウス座標
        pyxel.text(1, 1, str(pyxel.frame_count), 15)
        pyxel.text(1, 10, f"mouse_x:{self.player.x}, mouse_y:{self.player.y}", 15)
        pyxel.text(1, 20, f"dxy:{self.chaser.dxy}", 15)
        # 壁
        for index, point in enumerate(self.wall.points):
            if index < len(self.wall.points)-1:
                pyxel.line(point[0], point[1], self.wall.points[index+1][0], self.wall.points[index+1][1], 10)
            else:
                pyxel.line(point[0], point[1], self.wall.points[0][0], self.wall.points[0][1], 10)
            # (ポインターとの位置関係確認用)
            pyxel.line(point[0], point[1], self.player.x, self.player.y, 8)
            pyxel.line(self.chaser.x, self.chaser.y, self.player.x, self.player.y, 8)
        # pyxresファイル内から：マウス座標が中央に見えるように配置。
        # マウスクリックで別の対象描画
        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            pyxel.blt(self.player.x-8, self.player.y-8, 0, 16*(pyxel.frame_count%4), 0, 16, 16, 0)
        else:
            pyxel.blt(self.player.x-8, self.player.y-8, 0, 16*(pyxel.frame_count%2), 16, 16, 16, 0)
        # プレイヤーの当たり判定
        pyxel.circb(self.player.x, self.player.y, self.player.r, 8)
        # 敵
        pyxel.circ(self.chaser.x, self.chaser.y, self.chaser.r, self.chaser.color)
        if self.chaser.color == 8:
            pyxel.circb(self.chaser.x, self.chaser.y, self.chaser.r, 10)

class Chaser:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.v = 0
        self.vx = 0
        self.vy = 0
        self.movable = True
        self.color = 8

    def set_new_coords(self):
        """
        速度を足して座標更新。
        """
        self.x += self.vx
        self.y += self.vy
    
    def set_new_vector(self, tar_x, tar_y, frame_count):
        """
        対象に向かう角度を算出して
        ｘとｙ方向の速度に反映。
        """
        if self.movable == True:
            self.dy = tar_y-self.y   # 対象との距離：y
            self.dx = tar_x-self.x   # 対象との距離：x
            rad = np.arctan2(self.dy, self.dx)    # 対象との角度
            # x, yどちらの距離も1未満なら動きを止める
            if abs(self.dx) < 1 and abs(self.dy) < 1:
                self.v = 0
            else:
                self.v = 0.8
            self.vx = self.v*math.cos(rad)
            self.vy = self.v*math.sin(rad)
            self.dxy = int(math.sqrt(self.dx*self.dx+self.dy*self.dy))  # 対象との直線距離
            # self.dxyをの点滅の速さに使う
            if  70 <= self.dxy < 120:
                change_time = 20
            elif  40 <= self.dxy < 70:
                change_time = 10
            elif self.dxy < 40:
                change_time = 4
            else:
                change_time = 1 
            # 色と大きさを切り替えて自身を点滅させる
            if frame_count%change_time/2 < change_time/4:
                self.color = 8
                self.r = 7
            else:
                self.color = 10
                self.r = 8
        

class Player:
    """
    pyxelのマウスポインタ座標を補正し、
    画面からはみ出ないようにする
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 8

    def check(self, size_x, size_y, mouse_x, mouse_y):
        if mouse_x < 0:
            self.x = 0
        elif mouse_x > size_x:
            self.x = size_x
        else:
            self.x = mouse_x
        if mouse_y < 0:
            self.y = 0
        elif mouse_y > size_y:
            self.y = size_y
        else:
            self.y = mouse_y

class Flag:
    def __init__(self):
        self.gameover = False
        self.gameclear = False


def main():
    App()

if __name__ == "__main__":
    main()
