import pyxel
import numpy as np
from stage import Pointer

class StageSelect:
    def __init__(self, size_x, size_y, json_load):
        self.size_x = size_x
        self.size_y = size_y
        self.stages = json_load
        self.number = Number(size_x/2, size_y/2, 1, len(json_load))
        self.pointer = Pointer()
        self.array_button_right = ArrayButton(self.size_x-40, 128, 20, 40, 0)
        self.array_button_left = ArrayButton(40, 128, 20, 40, 1)
        self.activate = True
    
    def update_stage_select(self):
        if self.activate:
            self.pointer.update_pointer(0, 0, self.size_x, self.size_y)
            self.array_button_right.update_array_button(self.pointer.x, self.pointer.y)
            self.array_button_left.update_array_button(self.pointer.x, self.pointer.y)
            self.number.update_number(self.array_button_right.push, self.array_button_left.push)
            if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
                self.activate = False
                return self.stages[str(self.number.num)]

    def draw_stage_select(self):
        if self.activate:
            self.number.draw_number()
            self.pointer.draw_pointer()
            self.array_button_right.draw_array_button()
            self.array_button_left.draw_array_button()
            pyxel.text(10, 10, f"right:{self.array_button_right.push},\nleft:{self.array_button_left.push}", 8)


class ArrayButton:
    def __init__(self, x, y, w, h, l_or_r):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.push = False
        self.l_or_r = l_or_r
        self.col = 8

    def update_array_button(self, tar_x, tar_y):
        self.push = False
        if (self.x-self.w/2 <= tar_x < self.x+self.w/2 and 
            self.y-self.h/2 <= tar_y < self.y+self.h/2 and 
            pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
            self.push = True

    def draw_array_button(self):
        if self.push:
            self.col = 10
        else:
            self.col = 8
        # 右=0
        if self.l_or_r == 0:
            points = np.array([[self.x-self.w/2, self.y-self.h/2], [self.x-self.w/2, self.y+self.h/2], [self.x+self.w/2, self.y]])
            text = "NEXT"
        else:
            points = np.array([[self.x+self.w/2, self.y-self.h/2], [self.x+self.w/2, self.y+self.h/2], [self.x-self.w/2, self.y]])
            text = "PREV"
        for index, point in enumerate(points):
            if index < len(points)-1:
                pyxel.line(point[0], point[1], points[index+1][0], points[index+1][1], self.col)
            else:
                pyxel.line(point[0], point[1], points[0][0], points[0][1], self.col)
        pyxel.text(self.x-self.w/2*0.75, self.y-self.h*0.75, text, self.col)


class Number:
    """[summary]
    """    
    def __init__(self, x, y, num, max):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
            num ([int]): [description]
        """        
        self.count0 = pyxel.frame_count
        self.coords = np.array([x, y])
        self.rad = 0
        self.expansion_rate = 5
        self.expansion_rate_max = 5
        self.v_expansion_rate = 1
        self.v_rad = np.pi/90

        # 中心座標を原点とした位置ベクトル
        self.settings = [
            [
                [[-3, -13], [2, -13], [7, -8], [7, 7], [2, 12], [-3, 12], [-8, 7], [-8, -8]],
                [[-3, -8], [2, -8], [2, 7], [-3, 7]]
            ],
            [
                [[-3, -13], [2, -13], [2, 12], [-3, 12], [-3, -8], [-8, -3], [-8, -8]]
            ],
            [
                [[-3, -13], [2, -13], [7, -8], [7, -3], [-3, 7], [7, 7], [7, 12], [-8, 12], [-8, 7], [2, -3], [2, -8], [-8, -8]]
            ],
            [
                [[-3, -13], [2, -13], [7, -8], [7, 7], [2, 12], [-3, 12], [-8, 7], [2, 7], [2, 2], [-3, 2], [-3, -3], [2, -3], [2, -8], [-8, -8]]
            ], 
            [
                [[-8, -13], [-3, -13], [-3, -3], [2, -3], [2, -13], [7, -13], [7, 12], [2, 12], [2, 2], [-8, 2]]
            ],
            [
                [[-8, -13], [7, -13], [7, -8], [-3, -8], [-3, -3], [2, -3], [7, 2], [7, 7], [2, 12], [-3, 12], [-8, 7], [2, 7], [2, 2], [-3, 2], [-8, -3]]
            ],
            [
                [[-3, -13], [2, -13], [7, -8], [-3, -8], [-3, -3], [2, -3], [7, 2], [7, 7], [2, 12], [-3, 12], [-8, 7], [-8, -8]],
                [[-3, 2], [2, 2], [2, 7], [-3, 7]]
            ],
            [
                [[-8, -13], [7, -13], [7, -3], [-3, 12], [-8, 12], [2, -3], [2, -8], [-8, -8]]
            ],
            [
                [[-3, -13], [2, -13], [7, -8], [7, 7], [2, 12], [-3, 12], [-8, 7], [-8, -8]],
                [[-3, -8], [2, -8], [2, -3], [-3, -3]],
                [[-3, 2], [2, 2], [2, 7], [-3, 7]]
            ],
            [
                [[-3, -13], [2, -13], [7, -8], [7, 7], [2, 12], [-3, 12], [-8, 7], [2, 7], [2, 2], [-3, 2], [-8, -3], [-8, -8]],
                [[-3, -8], [2, -8], [2, -3], [-3, -3]],
            ],
        ]
        self.num = num
        self.num_min = 1
        self.num_max = max
        self.selected_setting = np.array(self.settings[self.num])
        self.col = 10
        self.prev_next = 1
    
    def update_number(self, next, prev):
        """[summary]
        """       
        if prev:
            self.count0 = pyxel.frame_count
            self.prev_next = -1
            self.num -= 1
        elif next:
            self.count0 = pyxel.frame_count
            self.prev_next = 1
            self.num += 1
        if self.num <= self.num_min:
            self.num = self.num_min
        elif self.num >= self.num_max:
            self.num = self.num_max
        self.selected_setting = self.settings[self.num]
        self.expansion_rate *= self.v_expansion_rate
        self.rad_sca = np.pi/8/((pyxel.frame_count-self.count0)+1/50)
        if self.rad_sca <= 0.03:
            self.rad_sca = 0
        #self.coords[1] += np.sin(np.pi/60*(pyxel.frame_count))
        #self.coords[0] += np.cos(np.pi/180*(pyxel.frame_count))
        self.rad = self.rad_sca * (self.prev_next)*np.cos(np.pi/2*(pyxel.frame_count-self.count0))

    def draw_number(self):
        """[summary]
        """        
        for index, points in enumerate(self.selected_setting):
            for index, point in enumerate(points):
                if index < len(points)-1:
                    pyxel.line(self.set_point_coord(point)[0], self.set_point_coord(point)[1], 
                               self.set_point_coord(points[index+1])[0], self.set_point_coord(points[index+1])[1], self.col)
                else:
                    pyxel.line(self.set_point_coord(point)[0], self.set_point_coord(point)[1], 
                               self.set_point_coord(points[0])[0], self.set_point_coord(points[0])[1], self.col)
    
    def set_point_coord(self, point):
        return self.coords + np.dot(np.array([[np.cos(self.rad), -np.sin(self.rad)], [np.sin(self.rad), np.cos(self.rad)]]), point)*self.expansion_rate