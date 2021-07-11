import pyxel
import numpy as np

class App:
    def __init__(self):
        self.size_x = 256
        self.size_y = 256
        self.system_screen = SystemScreen(0, 0, self.size_x, 64)
        pyxel.init(self.size_x, self.size_y, caption="test!", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("for_mygame.pyxres")
        pyxel.mouse(True)
        self.pointer = Pointer()
        self.lines = Lines(True)
        self.wall = Wall()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.pointer.check(self.size_x, self.size_y, self.system_screen.h)
        self.system_screen.update_system()
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.lines.add_point(self.pointer)
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON) and len(self.lines.points) > 1:
            self.lines.active = False
            self.wall.add_lines(self.lines)
            self.lines = Lines(True)

    def draw(self):
        pyxel.cls(0)
        self.system_screen.draw_system()
        self.pointer.draw_pointer()
        self.lines.draw_lines(self.pointer)
        self.wall.draw_wall(self.pointer)
        pyxel.text(10, 74, f"mouse_x:{pyxel.mouse_x}\nmouse_y:{pyxel.mouse_y}\npointer.mouseL_now:{self.pointer.mouseL_now}\npointer.mouseL_last:{self.pointer.mouseL_last}\nwall.points:{self.wall.wall}", 8)
        pyxel.text(158, 45, f"Press mouse_R button or\nselect other drawing to\ndetermine this drawing.", 0)


class Pointer:
    def __init__(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
        self.mouseL_now = False
        self.mouseL_last = False
    
    def check(self, size_x, size_y, system_height):
        self.mouseL_last = self.mouseL_now
        if pyxel.mouse_x < 0:
            self.x = 0
        elif pyxel.mouse_x > size_x:
            self.x = size_x
        else:
            self.x = pyxel.mouse_x
        if  pyxel.mouse_y < system_height:
            self.y = system_height
        elif pyxel.mouse_y > size_y:
            self.y = size_y
        else:
            self.y = pyxel.mouse_y
        
        if 0<=pyxel.mouse_x<size_x and system_height<=pyxel.mouse_y<size_y:
            pyxel.mouse(False)
            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                self.mouseL_now = True
            else:
                self.mouseL_now = False
        else:
            self.mouseL_now = False
            pyxel.mouse(True)

    def draw_pointer(self):
        if self.mouseL_now:
            pyxel.blt(self.x-2, self.y-2, 0, 8, 0, 5, 5, 0)
        else:
            pyxel.blt(self.x-2, self.y-2, 0, 0, 0, 5, 5, 0)


class Lines:
    def __init__(self, close):
        self.close = close
        self.points = []
        self.active = True
    
    def add_point(self, pointer):
        if len(self.points) == 0:
            self.points = [[pointer.x, pointer.y]] 
        elif len(self.points) == 1 and (self.points[-1][0] != pointer.x or self.points[-1][1] != pointer.y):
            self.points.append([pointer.x, pointer.y])
        elif (len(self.points) >= 2 and 
            ((self.points[-1][0] != pointer.x or self.points[-1][1] != pointer.y)and
            (self.points[-2][0] != pointer.x or self.points[-2][1] != pointer.y))):
            self.points.append([pointer.x, pointer.y])
        
    def draw_lines(self, pointer):
        """構成する全ての線の描画
        """
        if len(self.points) > 0:
            for index, point in enumerate(self.points):
                if index < len(self.points)-1:
                    pyxel.line(point[0], point[1], self.points[index+1][0], self.points[index+1][1], 10)
            if self.active == True:
                pyxel.line(self.points[-1][0], self.points[-1][1], pointer.x, pointer.y, 5)
            if self.close == True:
                if self.active == False:
                    pyxel.line(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1], 10)
                else:
                    pyxel.line(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1], 3)            
                if self.active == True:
                    pyxel.line(pointer.x, pointer.y, self.points[0][0], self.points[0][1], 3)

                
class Wall:
    def __init__(self):
        self.wall = []
        self.lines_objects = []
        self.index = 0
    
    def add_lines(self, lines):
        # 点が２個だったら元々「閉じる」でも閉じなく設定し直す
        if len(lines.points) <= 2:
            lines.close = 0
        # 点と閉じる設定のリストを末尾に追加
        self.wall.append([lines.points, lines.close])
        # (描画用)線群のオブジェクトを末尾に追加
        self.lines_objects.append(lines)
    
    def draw_wall(self, pointer):
        for lines in self.lines_objects:
            lines.draw_lines(pointer)
        

class SystemScreen:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.button = Button(10, 10, 10, 10)
    
    def update_system(self):
        self.button.check_hover()

    def draw_system(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 8)
        pyxel.rect(self.button.x, self.button.y, self.button.w, self.button.h, 10)
        pyxel.text(10, 20, f"button_switch:{self.button.switch_on}", 10)


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hover = False
        self.switch_on = False

    def check_hover(self):
        if (self.x<=pyxel.mouse_x<self.x+self.w and 
            self.y<=pyxel.mouse_y<self.y+self.y):
            self.hover = True
        else:
            self.hover = False
        if self.hover and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            if self.switch_on == False:
                self.switch_on = True
            else:
                self.off_switch()

    def off_switch(self):
        self.switch_on = False

        

if __name__ == "__main__":
    App()