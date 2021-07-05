import pyxel
import numpy as np

class App:
    def __init__(self):
        self.size_x = 256
        self.size_y = 256
        pyxel.init(self.size_x, self.size_y, caption="test!", scale=5, fps=30, quit_key=pyxel.KEY_ESCAPE, fullscreen=True)
        pyxel.load("foreditor.pyxres")
        self.lines = Lines(True)
        self.mouseL_now = False
        self.mouseL_last = False
        pyxel.run(self.update, self.draw)


    def update(self):
        self.mouseL_last = self.mouseL_now
        self.mouseL_now = pyxel.btn(pyxel.MOUSE_LEFT_BUTTON)
        if self.mouseL_last == False and self.mouseL_now == True:
            self.lines.add_point()
        #elif self.mouseL_last == True and self.mouseL_now == False:
        #    pass

    def draw(self):
        pyxel.cls(0)
        if self.mouseL_now:
            pyxel.blt(pyxel.mouse_x-2, pyxel.mouse_y-2, 0, 8, 0, 5, 5, 0)
        else:
            pyxel.blt(pyxel.mouse_x-2, pyxel.mouse_y-2, 0, 0, 0, 5, 5, 0)
        pyxel.text(10, 10, f"mouse_x:{pyxel.mouse_x}\nmouse_y:{pyxel.mouse_y}\nmouseL_now:{self.mouseL_now}\nmouseL_last:{self.mouseL_last}\npoints:{self.lines.points}", 8)
        self.lines.draw_lines()


class Lines:
    """線の集まりを包括管理
    """
    def __init__(self, close):
        """コンストラクタ

        リストに線オブジェクトがそれぞれ格納される。
        [配列, 終点->始点の線で閉じるかのbool値]が渡される。
        """
        self.close = close
        self.points = np.array([])
    
    def add_point(self):
        if len(self.points) == 0:
            self.points = np.array([[pyxel.mouse_x, pyxel.mouse_y]]) 
        else:
            self.points = np.vstack([self.points, np.array([[pyxel.mouse_x, pyxel.mouse_y]])])
    
    def draw_lines(self):
        """構成する全ての線の描画
        """
        if len(self.points) > 0:
            for index, point in enumerate(self.points):
                if index < len(self.points)-1:
                    pyxel.line(point[0], point[1], self.points[index+1][0], self.points[index+1][1], 10)
            pyxel.line(self.points[-1][0], self.points[-1][1], pyxel.mouse_x, pyxel.mouse_y, 5)
            if self.close == True:
                pyxel.line(pyxel.mouse_x, pyxel.mouse_y, self.points[0][0], self.points[0][1], 3)
                pyxel.line(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1], 3)
                
            
class Wall:
    """線の集まり　の集まりを包括管理
    
    """
    def __init__(self, args):
        """コンストラクタ

        リストに線の集まりオブジェクトがそれぞれ格納される。
        [任意の数の[配列, 終点->始点の線で閉じるかのbool値]]が渡される。
        """
        self.wall = np.array([])
        for lines in args:
            self.wall = np.append(self.wall, Lines(lines))
    
    def draw_wall(self):
        """構成する全ての線の集まりの描画
        """
        for lines in self.wall:
            lines.draw_lines()
        

if __name__ == "__main__":
    App()