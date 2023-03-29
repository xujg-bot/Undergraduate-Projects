import tkinter as tk
import numpy as np
from math import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Bresenham算法计算路径点坐标
def Bresenham(X0, Y0, X1, Y1):
    x = np.array([])
    y = np.array([])
    dx = abs(X1 - X0)
    dy = abs(Y1 - Y0)
    if X0 < X1:
        sx = 1
    else:
        sx = -1
    if Y0 < Y1:
        sy = 1
    else:
        sy = -1
    if dx > dy:
        erro = dx / 2
    else:
        erro = -dy / 2
    while X0 != X1 or Y0 != Y1:
        x = np.append(x, X0)
        y = np.append(y, Y0)
        e2 = erro
        if e2 > -dx:
            erro -= dy
            X0 += sx
        if e2 < dy:
            erro += dx
            Y0 += sy
    return x, y


# 立方体类
# 属性有三维空间坐标（X，Y，Z）、二维投影坐标（m，n），移动步长move_step和旋转角度步长rotate_step
# 方法有三种投影方式、平移和旋转
class Cube:
    def __init__(self, X, Y, Z, move_step=1, rotate_step=0.01, m=0, n=0):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.move_step = move_step
        self.rotate_step = rotate_step
        self.m = m
        self.n = n

    # 斜二测投影
    def Oblique_Twomeasure_Projection(self):
        self.m = np.around(self.X - 0.354 * self.Z)
        self.n = np.around(self.Y - 0.354 * self.Z)

    # 斜等轴投影
    def Oblique_Isometric_Projection(self):
        self.m = np.around(self.X + 0.707 * self.Z)
        self.n = np.around(self.Y + 0.707 * self.Z)

    # 正投影
    def Orthographic_Projection(self):
        self.m = np.around(self.X)
        self.n = np.around(self.Y)

    # 旋转变换
    def Rotation(self, theta_x, theta_y, theta_z):
        # 绕x轴旋转
        self.Y = self.Y * cos(theta_x) - self.Z * sin(theta_x)
        self.Z = self.Y * sin(theta_x) + self.Z * cos(theta_x)
        # 绕y轴旋转
        self.X = self.X * cos(theta_y) + self.Z * sin(theta_y)
        self.Z = -self.X * sin(theta_y) + self.Z * cos(theta_y)
        # 绕z轴旋转
        self.X = self.X * cos(theta_z) - self.X * sin(theta_z)
        self.Y = self.X * sin(theta_z) + self.Y * cos(theta_z)

    # 平移变换
    def Translation(self, Dx, Dy, Dz):
        self.X += Dx
        self.Y += Dy
        self.Z += Dz


# 交互窗口类
# 通过status的值改变投影方式
class UI(tk.Tk):
    WIDTH = 800
    HEIGHT = 600
    TITLE = '计科16201319徐晋国计算机图形学大作业'

    def __init__(self):
        tk.Tk.__init__(self)
        self.status = 0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        # 三个投影的按钮
        tk.Button(self, text="斜二测投影", command=self.switch_0, width=15, height=3).place(x=20, y=10)
        tk.Button(self, text="斜等轴投影", command=self.switch_1, width=15, height=3).place(x=20, y=90)
        tk.Button(self, text="正投影", command=self.switch_2, width=15, height=3).place(x=20, y=170)
        # 操作提示标签
        tk.Label(self, text="w，s键使立方体沿X轴前后移动").place(x=20, y=240)
        tk.Label(self, text="a，d键使立方体沿Y轴前后移动").place(x=20, y=270)
        tk.Label(self, text="t，g键使立方体沿Z轴前后移动").place(x=20, y=300)
        tk.Label(self, text="按住Ctrl+鼠标左键拖动，绕X轴\n正向旋转").place(x=20, y=330)
        tk.Label(self, text="按住Shift+鼠标左键拖动，绕X轴\n逆向旋转").place(x=20, y=370)
        tk.Label(self, text="按住Ctrl+鼠标中键拖动，绕Y轴\n正向旋转").place(x=20, y=410)
        tk.Label(self, text="按住Shift+鼠标中键拖动，绕Y轴\n逆向旋转").place(x=20, y=450)
        tk.Label(self, text="按住Ctrl+鼠标右键拖动，绕Z轴\n正向旋转").place(x=20, y=490)
        tk.Label(self, text="按住Shift+鼠标右键拖动，绕Z轴\n逆向旋转").place(x=20, y=530)
        # 摆放画布
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=200, y=40)
        # 键盘事件绑定
        self.bind("d", self.move_x1)
        self.bind("a", self.move_x2)
        self.bind("w", self.move_y1)
        self.bind("s", self.move_y2)
        self.bind("t", self.move_z1)
        self.bind("g", self.move_z2)
        # 鼠标事件绑定
        self.bind("<Control-B1-Motion>", self.rotate_x1)
        self.bind("<Shift-B1-Motion>", self.rotate_x2)
        self.bind("<Control-B2-Motion>", self.rotate_y1)
        self.bind("<Shift-B2-Motion>", self.rotate_y2)
        self.bind("<Control-B3-Motion>", self.rotate_z1)
        self.bind("<Shift-B3-Motion>", self.rotate_z2)

    # 投影切换命令
    def switch_0(self):
        self.status = 0

    def switch_1(self):
        self.status = 1

    def switch_2(self):
        self.status = 2

    # 平移命令
    def move_x1(self, event):
        cube.Translation(cube.move_step, 0, 0)

    def move_x2(self, event):
        cube.Translation(-cube.move_step, 0, 0)

    def move_y1(self, event):
        cube.Translation(0, cube.move_step, 0)

    def move_y2(self, event):
        cube.Translation(0, -cube.move_step, 0)

    def move_z1(self, event):
        cube.Translation(0, 0, cube.move_step)

    def move_z2(self, event):
        cube.Translation(0, 0, -cube.move_step)

    # 旋转命令
    def rotate_x1(self, event):
        cube.Rotation(cube.rotate_step, 0, 0)

    def rotate_x2(self, event):
        cube.Rotation(-cube.rotate_step, 0, 0)

    def rotate_y1(self, event):
        cube.Rotation(0, cube.rotate_step, 0)

    def rotate_y2(self, event):
        cube.Rotation(0, -cube.rotate_step, 0)

    def rotate_z1(self, event):
        cube.Rotation(0, 0, cube.rotate_step)

    def rotate_z2(self, event):
        cube.Rotation(0, 0, -cube.rotate_step)

    # 刷新画布，绘制散点图
    def plot(self):
        if self.status == 0:
            cube.Oblique_Twomeasure_Projection()
        elif self.status == 1:
            cube.Oblique_Isometric_Projection()
        elif self.status == 2:
            cube.Orthographic_Projection()
        plt.cla()
        plt.xlim((-100, 200))
        plt.ylim((-100, 200))
        # self.ax.axis('off')
        plt.scatter(Bresenham(cube.m[0], cube.n[0], cube.m[1], cube.n[1])[0],
                    Bresenham(cube.m[0], cube.n[0], cube.m[1], cube.n[1])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[0], cube.n[0], cube.m[2], cube.n[2])[0],
                    Bresenham(cube.m[0], cube.n[0], cube.m[2], cube.n[2])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[0], cube.n[0], cube.m[3], cube.n[3])[0],
                    Bresenham(cube.m[0], cube.n[0], cube.m[3], cube.n[3])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[1], cube.n[1], cube.m[4], cube.n[4])[0],
                    Bresenham(cube.m[1], cube.n[1], cube.m[4], cube.n[4])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[1], cube.n[1], cube.m[6], cube.n[6])[0],
                    Bresenham(cube.m[1], cube.n[1], cube.m[6], cube.n[6])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[2], cube.n[2], cube.m[4], cube.n[4])[0],
                    Bresenham(cube.m[2], cube.n[2], cube.m[4], cube.n[4])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[2], cube.n[2], cube.m[5], cube.n[5])[0],
                    Bresenham(cube.m[2], cube.n[2], cube.m[5], cube.n[5])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[3], cube.n[3], cube.m[6], cube.n[6])[0],
                    Bresenham(cube.m[3], cube.n[3], cube.m[6], cube.n[6])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[3], cube.n[3], cube.m[5], cube.n[5])[0],
                    Bresenham(cube.m[3], cube.n[3], cube.m[5], cube.n[5])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[4], cube.n[4], cube.m[7], cube.n[7])[0],
                    Bresenham(cube.m[4], cube.n[4], cube.m[7], cube.n[7])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[5], cube.n[5], cube.m[7], cube.n[7])[0],
                    Bresenham(cube.m[5], cube.n[5], cube.m[7], cube.n[7])[1],
                    c='black', s=1)
        plt.scatter(Bresenham(cube.m[6], cube.n[6], cube.m[7], cube.n[7])[0],
                    Bresenham(cube.m[6], cube.n[6], cube.m[7], cube.n[7])[1],
                    c='black', s=1)
        self.canvas.draw()
        window.after(20, window.plot)


if __name__ == '__main__':
    # 初始化立方体的顶点坐标
    cube = Cube(X=np.array([0, 100, 0, 0, 100, 0, 100, 100]),
                Y=np.array([0, 0, 100, 0, 100, 100, 0, 100]),
                Z=np.array([0, 0, 0, 100, 0, 100, 100, 100]))
    window = UI()
    window.title(window.TITLE)
    window.geometry(f'{window.WIDTH}x{window.HEIGHT}')
    window.after(20, window.plot)
    window.mainloop()
