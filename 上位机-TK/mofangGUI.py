# -*- coding: UTF-8 -*-
from Tkinter import *
import json
import cv2
from PIL import Image as PILImage
from PIL import ImageTk
import numpy as np
import time
import kociemba
import serial
import serial.tools.list_ports


white = [np.array([0, 0, 106]), np.array([180, 69, 255])]
yellow = [np.array([17, 45, 45]), np.array([35, 255, 255])]
green = [np.array([35, 45,  45]), np.array([87, 255, 255])]
orange = [np.array([5, 100, 100]), np.array([16, 255, 255])]
blue = [np.array([96, 46, 46]), np.array([124, 255, 255])]
red1 = [np.array([146, 123, 112]), np.array([180, 255, 255])]
red2 = [np.array([0, 48, 48]), np.array([14, 255, 255])]
IMG_SIZE = 100

f = open("./config.json", "r")
position_origin = json.load(f)
f.close()

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)


class CubeGUI:
    def __init__(self):

        self.cube_list = [[270, 90], [90, 180], [180, 90], [90, 90], [90, 0], [0, 90]]
        self.cube_color = {'U': [255, 0, 0], 'R': [255, 255, 0], 'F': [255, 128, 0],
                           'D': [255, 255, 255], 'L': [11, 136, 30], 'B': [12, 62, 192]}

        # position_origin 为文件读取原始坐标
        # position_top position_bottom 为重置预保存坐标
        # position为求解魔方使用坐标
        self.position = position_origin
        self.position_top = []
        self.position_bottom = []

        self.cube = 'URBLUFRBUFURFRDDLFFULFFRRDRULFRDUBDLLBURLLDDBDBBBBUDFL'
        self.step = "  。  人  器   机   方   魔   解"

        self.point_flag = 0
        self.reset_flag = 0
        self.run_flag = 0

        # 创建主窗口
        self.root = Tk()
        self.root.title("Rubik's Cube")
        self.root.geometry('480x480')
        self.root.resizable(width=False, height=False)

        # 创建组件
        self.button_run = Button(self.root, text='运行', bd=4, width=8, height=2, font=('system', 12), command=self.gui_run)
        self.button_reset = Button(self.root, text='重置', bd=4, width=8, height=2, font=('system', 12), command=self.reset)
        self.button_end = Button(self.root, text='退出', bd=4, width=8, height=2, font=('system', 12), command=self.quit)

        self.image_label = Label(self.root)
        self.load_img(cv2.imread('init_cube.jpg'))
        self.list_step = Listbox(self.root, width=10, height=21, bd=2, font=('Arial', 13))
        self.solve_step_input()

        # 布局定位
        self.image_label.place(x=165, y=200, anchor=CENTER)
        self.list_step.place(x=350, y=20, anchor=NW)
        self.button_run.place(x=30, y=400, anchor=NW)
        self.button_reset.place(x=125, y=400, anchor=NW)
        self.button_end.place(x=220, y=400, anchor=NW)

    # 在顶层窗口中将解魔方步骤导入列表组件

    def solve_step_input(self):
        self.list_step.delete(0, END)
        for item in self.step.split(" "):
            self.list_step.insert(1, item)

    # 根据魔方标准字母排列创建十字架图形

    def cube_draw(self):
        bg_img = np.zeros((359, 269, 3), np.uint8)
        bg_img[:, :, 0] = 147
        bg_img[:, :, 1] = 147
        bg_img[:, :, 2] = 147

        for i in range(len(self.cube)):
            x = self.cube_list[i / 9][0] + (i % 9 / 3) * 30
            y = self.cube_list[i / 9][1] + (i % 3) * 30

            cube_b = self.cube_color[self.cube[i]][0]
            cube_g = self.cube_color[self.cube[i]][1]
            cube_r = self.cube_color[self.cube[i]][2]

            bg_img[x:x + 29, y:y + 29, 0] = cube_r
            bg_img[x:x + 29, y:y + 29, 1] = cube_g
            bg_img[x:x + 29, y:y + 29, 2] = cube_b
        cv2.imwrite('draw_cube.jpg', bg_img)
        return bg_img

    # 在顶层窗口图像标签中导入图像

    def load_img(self, image):
        res = PILImage.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img_png = ImageTk.PhotoImage(res)
        self.image_label.config(image=img_png)
        self.image_label.image = img_png

    # 重置位置坐标时，画十字标府函数

    def print_point(self, event, x, y, flags, param):
        if self.point_flag == 0:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.position_top.append([x, y])
                print self.position_top
            if event == cv2.EVENT_RBUTTONDOWN:
                self.position_top.pop()
                print self.position_top

        if self.point_flag == 1:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.position_bottom.append([x, y])
                print self.position_bottom
            if event == cv2.EVENT_RBUTTONDOWN:
                self.position_bottom.pop()
                print self.position_bottom

    # 运行按钮调用

    def gui_run(self):
        self.run_flag = 1
        ret0, img0 = cap0.read()
        while ret0 is False:
            ret0, img0 = cap0.read()
        ret1, img1 = cap1.read()
        while ret1 is False:
            ret1, img1 = cap1.read()

        # 调用外部函数
        self.cube = img_transform(self.position[0], self.position[1], [img0, img1])  # 处理图像
        try:
            self.cube = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
            self.step = kociemba.solve(self.cube)  # 调用解魔方算法
            send2stm32(self.step)  # 发送步骤到下位机
            self.load_img(self.cube_draw())  # 绘制魔方图像
            self.solve_step_input()  # 显示复原步骤
        except ValueError:
            print "cube discriminate error"
            self.step = None


    # 重置按钮调用函数
    # point_flag = 0表示可以重置第一张图的坐标
    # point_flag = 1表示可以重置第二张图的坐标
    # point_flag = 2时重置完成，写入json文件
    # reset_flag 表示重置成功
    def reset(self):

        del self.position_top[:]
        del self.position_bottom[:]
        cv2.namedWindow('position set')
        cv2.setMouseCallback('position set', self.print_point)

        ret0, img0 = cap0.read()
        while ret0 is False:
            ret0, img0 = cap0.read()
        ret1, img1 = cap1.read()
        while ret1 is False:
            ret1, img1 = cap1.read()
        while 1:
            if self.point_flag == 0:
                temp = img0.copy()
                position_temp = self.position_top
            elif self.point_flag == 1:
                temp = img1.copy()
                position_temp = self.position_bottom
            else:
                with open("./config.json", "w") as f:
                    self.position = [self.position_top, self.position_bottom]
                    json.dump(self.position, f)
                    self.point_flag = 0
                break

            for i in range(len(position_temp)):
                x = position_temp[i][0]
                y = position_temp[i][1]
                cv2.line(temp, (x-5, y-5), (x+5, y+5), (255, 0, 0), 4)
                cv2.line(temp, (x-5, y+5), (x+5, y-5), (255, 0, 0), 4)
            cv2.imshow('position set', temp)

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                self.point_flag = 0
                break
            if k == 13 and len(position_temp) == 7:
                self.point_flag += 1

        cv2.destroyWindow('position set')
        self.reset_flag = 1

    # 退出按钮调用函数

    def quit(self):
        cv2.destroyAllWindows()
        self.root.quit()


# 对原图像进行透视变换，拼接，阈值分割
def img_transform(position1, position2, img):
    pts0 = np.float32([[0, 0], [3*IMG_SIZE, 0], [0, 3*IMG_SIZE], [3*IMG_SIZE, 3*IMG_SIZE]])
    position_side = []

    kernel = np.ones((5, 5), np.uint8)
    position_side.append([position1[1], position1[2], position1[0], position1[6]])  # U
    position_side.append([position1[6], position1[2], position1[4], position1[3]])  # R
    position_side.append([position1[0], position1[6], position1[5], position1[4]])  # F

    position_side.append([position2[4], position2[5], position2[6], position2[0]])  # D
    position_side.append([position2[2], position2[3], position2[6], position2[4]])  # L
    position_side.append([position2[1], position2[2], position2[0], position2[6]])  # B

    dst = []
    # 透视变换
    for i in range(6):
        pts = np.float32(position_side[i])
        m = cv2.getPerspectiveTransform(pts, pts0)
        dst.append(cv2.warpPerspective(img[i/3], m, (3*IMG_SIZE, 3*IMG_SIZE)))

    # 拼接
    frame = np.concatenate(dst)
    # 得到每种颜色的阈值掩模
    mask = []
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask.append(cv2.inRange(frame_hsv, blue[0], blue[1]))
    mask.append(cv2.inRange(frame_hsv, white[0], white[1]))
    mask.append(cv2.inRange(frame_hsv, orange[0], orange[1]))
    mask.append(cv2.inRange(frame_hsv, green[0], green[1]))
    mask.append(cv2.inRange(frame_hsv, yellow[0], yellow[1]))

    # mask_show = cv2.resize(mask[2], None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("mask_show", mask_show)
    # 确定位置,用数字代表颜色 同阈值掩模索引
    cube_temp = [None for _ in xrange(54)]  # 用来暂存魔方的色块信息，用数字代表颜色 ：蓝白橙绿黄红---（0-5）

    # i 表示 6个掩模图像
    # j 表示每幅图像有54个色块
    for i in range(5):
        opening = cv2.morphologyEx(mask[i], cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        for j in range(len(cube_temp)):

            hist_mask = np.zeros(closing.shape[:2], np.uint8)
            hist_mask[j/3*IMG_SIZE:j/3*IMG_SIZE+IMG_SIZE, j % 3*IMG_SIZE:j % 3*IMG_SIZE+IMG_SIZE] = 255
            hist = cv2.calcHist([closing], [0], hist_mask, [1], [255, 256])  # 只查看白色像素个数，即当前颜色掩模像素点
            if j % 9 == 4 and hist[0] > IMG_SIZE * IMG_SIZE / 10:
                cube_temp[j] = i
            elif hist[0] > IMG_SIZE*IMG_SIZE/5:
                cube_temp[j] = i
    print "蓝色：%d\t" % cube_temp.count(0)
    print "白色：%d\t" % cube_temp.count(1)
    print "橙色：%d\t" % cube_temp.count(2)
    print "绿色：%d\t" % cube_temp.count(3)
    print "黄色：%d\t" % cube_temp.count(4)

    if cube_temp.count(None) == 9:
        cube_temp = [5 if x==None else x for x in cube_temp]
    print cube_temp
    # 利用中心色块数字，用位置"U R F D L B"替换，得到标准魔方编码
    cube = ""
    for i in range(len(cube_temp)):
        if cube_temp[i] == cube_temp[4]:
            cube += 'U'
        elif cube_temp[i] == cube_temp[13]:
            cube += 'R'
        elif cube_temp[i] == cube_temp[22]:
            cube += 'F'
        elif cube_temp[i] == cube_temp[31]:
            cube += 'D'
        elif cube_temp[i] == cube_temp[40]:
            cube += 'L'
        elif cube_temp[i] == cube_temp[49]:
            cube += 'B'
        else:
            print "data error!"
    return cube


# 发送解魔方步骤到STM32
def send2stm32(step):
    plist = list(serial.tools.list_ports.comports())
    step = "*"+step+"#\r\n"
    if len(plist) <= 0:
        print ("The Serial port can't find!")
    else:
        plist_0 = list(plist[0])
        serial_name = plist_0[0]
        serial_find = serial.Serial(serial_name, 115200, timeout=60)
        print ("check which port was really used >", serial_find.name)
        serial_find.write(step.encode())
    return


def main():

    gui = CubeGUI()
    gui.root.mainloop()


if __name__ == "__main__":
    main()






