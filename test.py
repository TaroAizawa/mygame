# C:/users/zat_a/game
# -*- coding: utf-8 -*-
from numpy.lib.index_tricks import s_
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
        pyxel.init(self.size_x, self.size_y, caption="test!", scale=5, fps=5, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("test.pyxres")
        self.bubble = Bubble(0, 200, 10, 25, - np.pi/6, 1, 0, 0, 200, self.size_y)
        pyxel.run(self.update, self.draw)

    def update(self):
        """pyxelの更新処理。
        
        座標などの計算はここに記述。
        """
        if pyxel.frame_count <= 100:
            self.bubble.update_bubble()

        # Qキーで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self): 
        """pyxelの描画処理。
        
        描画系の処理は全てここに記述。
        """
        # 画面を色１でクリア
        pyxel.cls(1)
        self.bubble.draw_bubble()
        


class Bubble:
    def __init__(self, x, y, r, v, rad, a, x1, y1, x2, y2):
        self.coord_now = np.array([x, y])
        self.r = r
        self.v_sca = v
        self.rad = rad
        self.v_unit = np.array([math.cos(rad), math.sin(rad)])
        self.a = a
        self.points = np.array([[x2, y2], [x2, y1]])
        
        self.ue = False

    def update_bubble(self):
        print(f"coord_now:{self.coord_now}")
        """次フレームの座標と速度ベクトルを決める
        """
        # 相手の点の始点->終点の線分ベクトル
        vec_start2end = self.points[0]-self.points[1]     
        # 相手の線と自身のベクトルのなす角
        rad_self2line = np.inner(self.v_sca*self.v_unit, vec_start2end)
        if rad_self2line >= np.pi/2:
            rad_self2line = rad_self2line % np.pi/2
        # ===== 現在 =====
        # 相手の点と自身の各種ベクトルを出す
        vec_start2self = self.coord_now-self.points[0]    # ベクトル：始点->自身
        vec_end2self = self.coord_now-self.points[1]        # ベクトル：終点->自身
        self.cross_now = np.cross(vec_start2end / np.linalg.norm(vec_start2end, ord=2), 
                                vec_start2self)            # 始点->相手の単位ベクトル と 始点->終点ベクトルとの外積(符号付きの高さ)

        # ===== 次フレーム =====
        # 次フレームの予定座標を出す
        coord_next = self.coord_now + self.v_sca * self.v_unit
        # 相手の点と自身の各種ベクトルを出す
        vec_start2self = coord_next-self.points[0]    # ベクトル：始点->自身
        vec_end2self = coord_next-self.points[1]        # ベクトル：終点->自身
        # 相手の線分に対する自身の高さを出す（外積）
        self.cross_next = np.cross(vec_start2end / np.linalg.norm(vec_start2end, ord=2), 
                                vec_start2self)            # 始点->相手の単位ベクトル と 始点->終点ベクトルとの外積(符号付きの高さ)

        # ===== 現在と次フレームの情報を比較して修正 =====
        # 現在 -> 未来の中心座標の線分ベクトルが相手の線分をまたいでいた場合
        if ((self.check_over90(vec_start2end, vec_start2self) != 
            self.check_over90(vec_start2end, vec_end2self)) and 
            ((self.cross_now < 0) != (self.cross_next < 0))):
            """# 元の速度ベクトルの長さに対する交点座標までの長さの割合s
            s = (abs(np.cross(self.points[0]-self.coord_now, vec_start2end))
                 /abs(np.cross(self.v_sca*self.v_unit, vec_start2end)))
            # 元の速度ベクトルの長さに対する、円が線分ベクトルに接地するような中心座標までの長さの割合s_ground
            s_ground = s - self.r/(self.v_sca*math.sin(rad_self2line))
            # 反射後の余った速度ベクトル
            buff = np.dot(np.array([[0, -1], [1, 0]]), vec_start2end)
            print(f"/n/n/n{buff}/n/n/n")
            v_toline = s_ground * self.v_sca * self.v_unit
            v_remain = ((1 - s_ground) * self.v_sca * self.v_unit 
                        + ((np.dot(np.array([[math.cos(rad_self2line), math.sin(rad_self2line)*(-1)], 
                                            [math.sin(rad_self2line), math.cos(rad_self2line)]]), 
                                            vec_start2end))
                            /(np.linalg.norm(vec_start2end)))*(1-s_ground)*self.v_sca*math.cos(rad_self2line)*2)
            # 次フレームの座標 = 現在の座標 + 接地までの速度ベクトル + 反射後の余った速度ベクトル　に修正
            #print(f"\n\n\n{v_remain}\n\n\n")
            coord_next = self.coord_now + v_toline
            # 次フレームからの単位ベクトルのみ更新
            self.v_unit = v_remain/np.linalg.norm(v_remain, ord=2)"""
        # 中心座標が越えてはいないが円が線分が当たっていた場合
        elif (abs(self.cross_next) <= self.r and 
            (self.check_over90(vec_start2end, vec_start2self) != 
            self.check_over90(vec_start2end, vec_end2self) or 
            (np.linalg.norm(vec_start2self, ord=2)<=self.r or 
            np.linalg.norm(vec_end2self, ord=2)<=self.r))):
            self.ue = True
            # 元の速度ベクトルの長さに対する、円が線分ベクトルに接地するような中心座標までの長さの割合s_ground
            s_ground = 1 - (self.r - abs(self.cross_next))/(self.v_sca*math.sin(rad_self2line))
            print(f"s_ground:{s_ground}")
            # 反射後の余った速度ベクトル
            buff = np.dot(np.array([[0, -1], [1, 0]]), vec_start2end)
            print(f"/n/n/n{buff}/n/n/n")
            v_toline = s_ground * self.v_sca * self.v_unit
            v_remain = ((1 - s_ground) * self.v_sca * self.v_unit 
                        + ((np.dot(np.array([[0, -1], [1, 0]]), vec_start2end))
                          /(np.linalg.norm(vec_start2end)))*(1-s_ground)*self.v_sca*math.sin(rad_self2line)*2)
            # 次フレームの座標 = 現在の座標 + 接地までの速度ベクトル + 反射後の余った速度ベクトル　に修正
            #print(f"\n\n\n{v_remain}\n\n\n")
            coord_next = self.coord_now + v_toline + v_remain
            # 次フレームからの単位ベクトルのみ更新
            self.v_unit = (v_remain)/np.linalg.norm(v_remain, ord=2)

        # 速度を加速度ぶん更新
        self.v_sca *= self.a
        # ===== 修正したうえで、次フレームの状態を現在のものとして反映する =====
        self.coord_now = coord_next

    def check_over90(self, A, B):
        """hit_check内で使う判定

        ２つのベクトルのなす角が鋭角かどうかをboolで返す。
        内積の正負で判断する。
        """
        if np.dot(A, B) <= 0:
            return True
        else:
            return False

    def draw_bubble(self):
        pyxel.circb(self.coord_now[0], self.coord_now[1], self.r, 10)
        pyxel.line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1], 10)
        pyxel.line(self.coord_now[0], self.coord_now[1], self.coord_now[0]+self.v_unit[0]*self.v_sca, self.coord_now[1]+self.v_unit[1]*self.v_sca, 10)
        pyxel.text(10, 10, f"{self.v_unit}, {self.v_sca}, {self.ue}", 8)


def main():
    App()

if __name__ == "__main__":
    main()
