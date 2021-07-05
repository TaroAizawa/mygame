# C:/users/zat_a/game
# -*- coding: utf-8 -*-
import pyxel
import numpy as np

class App():
    def __init__(self):
        # pyxelの初期設定
        self.size_x = 256
        self.size_y = 256
        pyxel.init(self.size_x, self.size_y, caption="Test of hit-check : lines", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        # 各オブジェクト生成
        self.player = Player(16)
        self.wall = Wall([[np.array([[64, 192], [192, 192], [192, 64], [64, 64]]), False], 
                          [np.array([[64, 176], [150, 120], [64, 80]]), True],
                          [np.array([[10, 64], [10, 192]]), False]])
        self.flag = Flag()
        # pyxel起動
        pyxel.run(self.update, self.draw)

    def update(self):
        # 各オブジェクトの処理
        self.flag.reset()
        self.player.update()
        self.wall.hit_check(np.array([self.player.x, self.player.y]), self.player.r)
        # ゲームオーバー判定
        self.flag.check_gameover((self.wall.hit))

    def draw(self):
        pyxel.cls(0)
        self.player.draw_player()
        self.wall.draw_wall()
        pyxel.text(10, 20, f"Game Over : {self.flag.gameover}", 8)


class Player:
    """プレイヤー

    プレイヤーの座標＝pyxel上のマウス座標。
    プレイヤーの座標の管理と描画。    
    """
    def __init__(self, r):
        """コンストラクタ
        """
        self.r = r
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
        self.coord_now = np.array([self.x, self.y])
        self.coord_last = self.coord_now
    def update(self):
        """自身の座標の更新
        """
        self.coord_last = self.coord_now
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
        self.coord_now = np.array([self.x, self.y])
        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width:
            self.x = pyxel.width
        else:
            self.x = pyxel.mouse_x
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height:
            self.y = pyxel.height
        else:
            self.y = pyxel.mouse_y

    def draw_player(self):
        """自身を円として描画
        """
        pyxel.circb(self.x, self.y, self.r, 10)
        pyxel.line(self.coord_last[0], self.coord_last[1], 
                    self.coord_now[0], self.coord_now[1], 10)


class OneLine:
    """当たり判定機能を持った一本の線
    """
    def __init__(self, start, end):
        self.start = start  # 始点座標
        self.end = end      # 終点座標
        self.color = 5
        self.hit = False
        self.cross_now = 0
        self.cross_last = 0

    def hit_check(self, tar_coord, tar_r):
        """相手を円と見たときの当たり判定
        """
        self.hit = False
        self.vec_start2end = np.array(self.end-self.start)     # ベクトル：始点->終点
        self.vec_start2tar = np.array(tar_coord-self.start)    # ベクトル：始点->相手
        self.vec_end2tar = np.array(tar_coord-self.end)        # ベクトル：終点->相手
        self.cross_now = np.cross(self.vec_start2end / np.linalg.norm(self.vec_start2end, ord=2), 
                                self.vec_start2tar)            # 始点->相手の単位ベクトルと始点->終点ベクトルとの外積(符号付きの高さ) 
        # 当たり判定
        if (abs(self.cross_now) <= tar_r and 
            (self.check_over90(self.vec_start2end, self.vec_start2tar) != 
            self.check_over90(self.vec_start2end, self.vec_end2tar) or 
            (np.linalg.norm(self.vec_start2tar, ord=2)<=tar_r or 
            np.linalg.norm(self.vec_end2tar, ord=2)<=tar_r))):
            self.hit = True
        elif ((self.check_over90(self.vec_start2end, self.vec_start2tar) != 
            self.check_over90(self.vec_start2end, self.vec_end2tar)) and 
            ((self.cross_now < 0) != (self.cross_last < 0))):
            self.hit = True
        self.cross_last = self.cross_now
    
    def check_over90(self, A, B):
        """hit_check内で使う判定

        ２つのベクトルのなす角が鋭角かどうかをboolで返す。
        内積の正負で判断する。
        """
        if np.dot(A, B) <= 0:
            return True
        else:
            return False
    
    def draw_oneline(self):
        """自身の描画

        テストのため当たり判定がTrueなら色を変える。
        """
        if self.hit == True:
            self.color = 10
        else:
            self.color = 5
        pyxel.line(self.start[0], self.start[1], self.end[0], self.end[1], self.color)


class Lines:
    """線の集まりを包括管理
    """
    def __init__(self, args):
        """コンストラクタ

        リストに線オブジェクトがそれぞれ格納される。
        [配列, 終点->始点の線で閉じるかのbool値]が渡される。
        """
        self.close = args[1]
        self.points = args[0]
        self.lines = []
        self.hit = False
        self.hit_of_lines = np.array([])
        for index, point in enumerate(self.points):
            if index < len(self.points)-1:
                self.lines.append(OneLine(point, self.points[index+1]))
            elif self.close == True:
                self.lines.append(OneLine(point, self.points[0]))
            self.hit_of_lines = np.append(self.hit_of_lines, False)
    
    def hit_check(self, tar_coord, tar_r):
        """対象との当たり判定を行う

        構成する線オブジェクトの全てで判定し、
        いずれかの判定がTrueなら自身の当たり判定をTrueにする。
        """
        self.hit = False
        for index, line in enumerate(self.lines):
            line.hit_check(tar_coord, tar_r)
            if line.hit == True:
                self.hit_of_lines[index] = True
            else:
                self.hit_of_lines[index] = False
        if np.any(self.hit_of_lines):
            self.hit = True

    def draw_lines(self):
        """構成する全ての線の描画
        """
        for line in self.lines:
            line.draw_oneline()


class Wall:
    """線の集まり　の集まりを包括管理
    
    """
    def __init__(self, args):
        """コンストラクタ

        リストに線の集まりオブジェクトがそれぞれ格納される。
        [任意の数の[配列, 終点->始点の線で閉じるかのbool値]]が渡される。
        """
        self.hit = False
        self.hit_of_lines = np.array([]) 
        self.wall = np.array([])
        for lines in args:
            self.wall = np.append(self.wall, Lines(lines))
            self.hit_of_lines = np.append(self.hit_of_lines, False)
    
    def hit_check(self, tar_coord, tar_r):
        """対象との当たり判定を行う

        構成する線の集まりオブジェクトの全てで判定し、
        いずれかの判定がTrueなら自身の当たり判定をTrueにする。
        """
        self.hit = False
        for index, lines in enumerate(self.wall):
            lines.hit_check(tar_coord, tar_r)
            self.hit_of_lines[index] = lines.hit
        if np.any(self.hit_of_lines):
            self.hit = True

    def draw_wall(self):
        """構成する全ての線の集まりの描画
        """
        for lines in self.wall:
            lines.draw_lines()
        pyxel.text(10, 10, f"hit:{self.hit}", 8)


class Flag:
    """ゲーム進行上のフラグを管理
    """
    def __init__(self):
        """各種フラグの初期化
        """
        self.gameover = False

    def check_gameover(self, *args):
        """ゲームオーバーの判定
        判定に使用したいbool値をすべて渡して, 
        いずれかがTrueならゲームオーバーのフラグをTrueにする
        """
        if any(args):
            self.gameover = True
    
    def reset(self):
        """各種フラグを初期値に戻す。
        """
        self.gameover = False

            
if __name__ == "__main__":
    App()