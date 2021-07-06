# C:/users/zat_a/game
# -*- coding: utf-8 -*-
import pyxel
import numpy as np
import math

# 場面の定義
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
        pyxel.init(self.size_x, self.size_y, caption="Test of hit-check : lines", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("foreditor.pyxres")
        # pyxel起動
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == TITLE:
            if self.scene_last != TITLE:
                self.title = Title()
            self.title.update_title()
            self.scene_last = TITLE
        if self.scene == STAGE_SELECT:
            if self.scene_last != STAGE_SELECT:
                self.stage_select = StageSelect(self.size_x, self.size_y, 1)
            self.stage_select.update_stage_select()
            self.scene_last = STAGE_SELECT
            if not self.stage_select.activate:
                del(self.stage_select)
                self.scene = STAGE
        if self.scene == STAGE:
            if self.scene_last == STAGE_SELECT:
                self.stage = Stage(self.size_x, self.size_y, pyxel.frame_count,
                           [220, 220, 10], 
                           [50, 50, 8],
                           [[np.array([[6, 69], [9, 248], [65, 245], [59, 128], [78, 129], [82, 242], [190, 237], [187, 130], [197, 129], [203, 244], [247, 247], [241, 74], [145, 73], [148, 197], [128, 198], [120, 70]]), True]])
            self.stage.update_Stage()
            self.scene_last = STAGE
            if not self.stage.activate:
                del(self.stage)
                self.scene = STAGE_SELECT


    def draw(self):
        pyxel.cls(0)
        if self.scene == TITLE:
            self.title.draw_title()
        if self.scene == STAGE_SELECT:
            self.stage_select.draw_stage_select()            
        if self.scene == STAGE:        
            self.stage.draw_Stage()
        pyxel.text(10, 50, f"scene:{self.scene}", 8)
        


class Title:
    def __init__(self):
        pass
    def update_title(self):
        pass
    def draw_title(self):
        pyxel.crs(0)


class StageSelect:
    def __init__(self, size_x, size_y, stages):
        self.size_x = size_x
        self.size_y = size_y
        self.stages = stages
        self.pointer = Pointer()
        self.activete = True
    
    def update_stage_select(self):
        self.pointer.update_pointer(0, 0, self.size_x, self.size_y)
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.activate = False

    def draw_stage_select(self):
        pyxel.cls(0)
        self.pointer.draw_pointer()

class Stage:
    def __init__(self, size_x, size_y, frame_start, player_arg, chaser_arg, wall_arg):
        # 各オブジェクト生成
        self.frame_start = frame_start
        self.frame = 0
        self.draw_next_frame = True
        self.update_next_frame = True
        self.activate = True
        self.size_x = size_x
        self.size_y = size_y
        self.pointer = Pointer()
        self.player = Player(player_arg[0], player_arg[1], player_arg[2])
        self.chaser = Chaser(chaser_arg[0], chaser_arg[1], chaser_arg[2])
        self.wall = Wall(wall_arg, [self.player.x, self.player.y])
        self.flag = Flag()
    
    def update_Stage(self):
        # 各オブジェクトの処理
        self.frame = pyxel.frame_count - self.frame_start
        self.flag.reset()
        if self.update_next_frame:
            self.pointer.update_pointer(0, 0, self.size_x, self.size_y)
            self.chaser.set_new_vector(self.player.x, self.player.y, pyxel.frame_count)
            self.player.update_player(self.pointer.x, self.pointer.y)
            self.chaser.hit_check(self.player.r, self.player.coord_last, self.player.coord_now)
            self.chaser.set_new_coords()
            self.wall.hit_check(np.array([self.player.x, self.player.y]), self.player.r)
            # ゲームオーバー判定
            self.flag.check_gameover(self.wall.hit, self.chaser.hit)
        # ゲームオーバーの時の処理
        if self.flag.gameover:
            self.activate = False
            self.update_next_frame = False
        # （テスト用）右クリックで復活させる
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.update_next_frame = True

    def draw_Stage(self):
        pyxel.cls(0)
        if self.draw_next_frame:
            self.pointer.draw_pointer()
            self.player.draw_player()
            self.chaser.draw_chaser()
            self.wall.draw_wall()
        pyxel.text(10, 20, f"Game Over : {self.flag.gameover}\nGame Activate:{self.update_next_frame}", 8)


class Pointer:
    def __init__(self):
        self.visible = True
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
    
    def update_pointer(self, x1, y1, x2, y2):
        if pyxel.mouse_x < x1:
            self.x = x1
        elif pyxel.mouse_x > x2:
            self.x = x2
        else:
            self.x = pyxel.mouse_x
        if  pyxel.mouse_y < y1:
            self.y = y1
        elif pyxel.mouse_y > y2:
            self.y = y2
        else:
            self.y = pyxel.mouse_y
        
        if x1<=pyxel.mouse_x<x2 and y1<=pyxel.mouse_y<y2:
            pyxel.mouse(False)
        else:
            pyxel.mouse(True)

    def draw_pointer(self):
        if self.visible:
            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.blt(self.x-2, self.y-2, 0, 8, 0, 5, 5, 0)
            else:
                pyxel.blt(self.x-2, self.y-2, 0, 0, 0, 5, 5, 0)


class Player:
    """プレイヤー

    プレイヤーの座標＝pyxel上のマウス座標。
    プレイヤーの座標の管理と描画。    
    """
    def __init__(self, x, y, r):
        """コンストラクタ
        """
        self.r = r
        self.x = x
        self.y = y
        self.coord_now = np.array([self.x, self.y])
        self.coord_last = self.coord_now
        self.follow = False

    def update_player(self, x, y):
        """自身の座標の更新
        """
        self.coord_last = self.coord_now
        if self.follow:
            self.x = x
            self.y = y
        self.coord_now = np.array([self.x, self.y])
        # 自分がクリックされたら
        if (np.linalg.norm(np.array([x-self.x, y-self.y]), ord=2)<=self.r and 
            pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
            self.follow = True

    def draw_player(self):
        """自身を円として描画
        """
        pyxel.circb(self.x, self.y, self.r, 10)
        pyxel.line(self.coord_last[0], self.coord_last[1], 
                    self.coord_now[0], self.coord_now[1], 10)


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
        self.hit = False

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

    def hit_check(self, tar_r, tar_coord_last, tar_coord_now):
        self.hit = False
        if self.dxy < tar_r + self.r:
            self.hit = True
            return

        self.vec_last2now = np.array(tar_coord_now-tar_coord_last+[0.01, 0.01])     # ベクトル：始点->終点
        self.vec_last2self = np.array([self.x, self.y]-tar_coord_last)    # ベクトル：始点->相手
        self.vec_now2self = np.array([self.x, self.y]-tar_coord_now)        # ベクトル：終点->相手
        self.cross = np.cross(self.vec_last2now / np.linalg.norm(self.vec_last2now, ord=2), self.vec_last2self)            # 始点->相手の単位ベクトルと始点->終点ベクトルとの外積(符号付きの高さ) 
        # 当たり判定
        if (abs(self.cross) <= self.r and 
            (self.check_over90(self.vec_last2now, self.vec_last2self) != 
            self.check_over90(self.vec_last2now, self.vec_now2self) or 
            (np.linalg.norm(self.vec_last2self, ord=2)<=self.r or 
            np.linalg.norm(self.vec_now2self, ord=2)<=self.r))):
            self.hit = True

    def check_over90(self, A, B):
        """hit_check内で使う判定

        ２つのベクトルのなす角が鋭角かどうかをboolで返す。
        内積の正負で判断する。
        """
        if np.dot(A, B) <= 0:
            return True
        else:
            return False
    
    def draw_chaser(self):
        pyxel.circ(self.x, self.y, self.r, self.color)
        if self.color == 8:
            pyxel.circb(self.x, self.y, self.r, 10)


class OneLine:
    """当たり判定機能を持った一本の線
    """
    def __init__(self, start, end, tar_coord):
        self.start = start  # 始点座標
        self.end = end      # 終点座標
        self.color = 5
        self.hit = False
        self.vec_start2end = np.array(self.end-self.start)     # ベクトル：始点->終点
        self.vec_start2tar = np.array(tar_coord-self.start)    # ベクトル：始点->相手
        self.vec_end2tar = np.array(tar_coord-self.end)        # ベクトル：終点->相手
        self.cross_now = np.cross(self.vec_start2end / np.linalg.norm(self.vec_start2end, ord=2), 
                                self.vec_start2tar)            # 始点->相手の単位ベクトルと始点->終点ベクトルとの外積(符号付きの高さ) 
        self.cross_last = self.cross_now

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
    def __init__(self, args, tar_coord):
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
                self.lines.append(OneLine(point, self.points[index+1], tar_coord))
            elif self.close == True:
                self.lines.append(OneLine(point, self.points[0], tar_coord))
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
    def __init__(self, args, tar_coord):
        """コンストラクタ

        リストに線の集まりオブジェクトがそれぞれ格納される。
        [任意の数の[配列, 終点->始点の線で閉じるかのbool値]]が渡される。
        """
        self.hit = False
        self.hit_of_lines = np.array([]) 
        self.wall = np.array([])
        for lines in args:
            self.wall = np.append(self.wall, Lines(lines, tar_coord))
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


class Flag:
    """ステージ進行上のフラグを管理
    """
    def __init__(self):
        """各種フラグの初期化
        """
        self.reset()

    def check_gameover(self, *args):
        """ゲームオーバーの判定
        判定に使用したいbool値をすべて渡して, 
        いずれかがTrueならゲームオーバーのフラグをTrueにする
        """
        if any(args):
            self.gameover = True
    
    def check_crear(self, *args):
        if any(args):
            self.gamecrear = True

    def reset(self):
        """各種フラグを初期値に戻す。
        """
        self.gameover = False
        self.gamecrear = False

            
if __name__ == "__main__":
    App()