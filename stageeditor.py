from mygame import Player
import pyxel
import numpy as np

class App:
    def __init__(self):
        self.size_x = 256
        self.size_y = 256
        self.system_screen = SystemScreen(0, 0, self.size_x, 64)
        pyxel.init(self.size_x, self.size_y, caption="test!", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("foreditor.pyxres")
        pyxel.mouse(True)
        self.pointer = Pointer()
        self.lines = Lines(True)
        self.wall = Wall()
        self.mouseL_now = False
        self.mouseL_last = False
        self.mouseR_now = False
        self.mouseR_lase = False
        pyxel.run(self.update, self.draw)

    def update(self):
        self.pointer.check(self.size_x, self.size_y, self.system_screen.h)
        self.mouseL_last = self.mouseL_now
        self.mouseR_lase = self.mouseR_now
        self.mouseL_now = pyxel.btn(pyxel.MOUSE_LEFT_BUTTON)
        self.mouseR_now = pyxel.btn(pyxel.MOUSE_RIGHT_BUTTON)
        if self.mouseL_last == False and self.mouseL_now == True:
            self.lines.add_point(self.pointer)
        if self.mouseR_lase == False and self.mouseR_now == True and len(self.lines.points)>=2:
            self.lines.active = False
            self.wall.add_lines(self.lines)
            self.lines = Lines(True)

    def draw(self):
        pyxel.cls(0)
        self.system_screen.draw()
        self.pointer.draw_pointer()
        self.lines.draw_lines(self.pointer)
        self.wall.draw_wall(self.pointer)
        pyxel.text(10, 74, f"mouse_x:{pyxel.mouse_x}\nmouse_y:{pyxel.mouse_y}\nmouseL_now:{self.mouseL_now}\nmouseL_last:{self.mouseL_last}\nwall.points:{self.wall.wall}", 8)

class Pointer:
    def __init__(self):
        self.x = pyxel.mouse_x
        self.y = pyxel.mouse_y
    
    def check(self, size_x, size_y, system_height):
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
        else:
            pyxel.mouse(True)

    
    def draw_pointer(self):
        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            pyxel.blt(self.x-2, self.y-2, 0, 8, 0, 5, 5, 0)
        else:
            pyxel.blt(self.x-2, self.y-2, 0, 0, 0, 5, 5, 0)


class Lines:
    def __init__(self, close):
        self.close = close
        self.points = np.array([])
        self.active = True
    
    def add_point(self, pointer):
        if len(self.points) == 0:
            self.points = np.array([[pointer.x, pointer.y]]) 
        else:
            self.points = np.vstack([self.points, np.array([[pointer.x, pointer.y]])])
    
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
            lines.close = False
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
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 8)


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hover = False

    def check_hover(self, tar):
        if (self.x<=pyxel.mouse_x<self.x+self.w and 
            self.y<=pyxel.mouse_y<self.y+self.y):
            self.hover = True
        else:
            self.hover = False
        
        if self.hover and tar:
            pass

    def aaa(self):
        pass
        

if __name__ == "__main__":
    App()