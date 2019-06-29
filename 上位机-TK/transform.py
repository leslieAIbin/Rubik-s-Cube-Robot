# -*- coding: utf-8 -*-

# 1.对原图像实现透视变换
# 2.合并透视变换后的子图
# 3.对合并图进行K-means聚类
# 4.转换成标准字符串
# 5.发送解魔方步骤到MCU

import cv2
import numpy as np
import kociemba
import json
import serial
import serial.tools.list_ports
import time

white = [np.array([0, 0, 106]), np.array([180, 69, 255])]
yellow = [np.array([17, 45, 45]), np.array([35, 255, 255])]
green = [np.array([35, 45,  45]), np.array([87, 255, 255])]
orange = [np.array([5, 100, 100]), np.array([16, 255, 255])]
blue = [np.array([96, 46, 46]), np.array([124, 255, 255])]
red1 = [np.array([146, 123, 112]), np.array([180, 255, 255])]
red2 = [np.array([0, 48, 48]), np.array([14, 255, 255])]
IMG_SIZE = 100

point_flag = 0
position_top = [[115, 99], [327, 21], [534, 86], [513, 318], [327, 454], [157, 323], [307, 195]]
position_bottom = [[144, 196], [304, 69], [505, 56], [570, 275], [439, 453], [247, 390], [342, 216]]


def nothing(x):
    pass


# 对原图像进行透视变换，拼接，阈值分割
def img_transform(position_top, position_bottom, img):
    pts0 = np.float32([[0, 0], [3*IMG_SIZE, 0], [0, 3*IMG_SIZE], [3*IMG_SIZE, 3*IMG_SIZE]])
    position_side = []

    kernel = np.ones((5, 5), np.uint8)
    position_side.append([position_top[1], position_top[2], position_top[0], position_top[6]])  # U
    position_side.append([position_top[6], position_top[2], position_top[4], position_top[3]])  # R
    position_side.append([position_top[0], position_top[6], position_top[5], position_top[4]])  # F

    position_side.append([position_bottom[4], position_bottom[5], position_bottom[6], position_bottom[0]])  # D
    position_side.append([position_bottom[2], position_bottom[3], position_bottom[6], position_bottom[4]])  # L
    position_side.append([position_bottom[1], position_bottom[2], position_bottom[0], position_bottom[6]])  # B

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
    print cube
    try:
        step = kociemba.solve(cube)
        print step
        # send2stm32(step)
    except ValueError:
        print "cube discriminate error"
        step = None
    return frame, step


# 发送解魔方步骤到STM32
def send2stm32(step):
    plist = list(serial.tools.list_ports.comports())
    step = "*"+step+"#\r\n"
    print step
    if len(plist) <= 0:
        print ("The Serial port can't find!")
    else:
        plist_0 = list(plist[0])
        serial_name = plist_0[0]
        serial_find = serial.Serial(serial_name, 115200, timeout=60)
        print ("check which port was really used >", serial_find.name)
        serial_find.write(step.encode())
    return


def print_point(event, x, y, flags, param):
    if point_flag == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            position_top.append([x, y])
            print position_top
        if event == cv2.EVENT_RBUTTONDOWN:
            position_top.pop()
            print position_top

    if point_flag == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            position_bottom.append([x, y])
            print position_bottom
        if event == cv2.EVENT_RBUTTONDOWN:
            position_bottom.pop()
            print position_bottom


def get_point(img0, img1):
    global point_flag
    cv2.namedWindow('position set')
    cv2.setMouseCallback('position set', print_point)
    while True:
        if point_flag == 0:
            temp = img0.copy()
            position_temp = position_top
        elif point_flag == 1:
            temp = img1.copy()
            position_temp = position_bottom
        else:
            point_flag = 0
            break
        for i in range(len(position_temp)):
            x = position_temp[i][0]
            y = position_temp[i][1]
            cv2.line(temp, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), 4)
            cv2.line(temp, (x - 5, y + 5), (x + 5, y - 5), (255, 0, 0), 4)
        cv2.imshow('position set', temp)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            break
        if k == 13 and len(position_temp) == 7:
            point_flag += 1

    cv2.destroyWindow('position set')


def set_hsv(frame):
    cv2.namedWindow('trackWindow')
    cv2.createTrackbar('H_low', 'trackWindow', 0, 180, nothing)
    cv2.createTrackbar('H_up', 'trackWindow', 0, 180, nothing)
    cv2.createTrackbar('S_low', 'trackWindow', 0, 255, nothing)
    cv2.createTrackbar('S_up', 'trackWindow', 0, 255, nothing)
    cv2.createTrackbar('V_low', 'trackWindow', 0, 255, nothing)
    cv2.createTrackbar('V_up', 'trackWindow', 0, 255, nothing)
    while True:
        H_low = cv2.getTrackbarPos('H_low', 'trackWindow')
        H_up = cv2.getTrackbarPos('H_up', 'trackWindow')
        S_low = cv2.getTrackbarPos('S_low', 'trackWindow')
        S_up = cv2.getTrackbarPos('S_up', 'trackWindow')
        V_low = cv2.getTrackbarPos('V_low', 'trackWindow')
        V_up = cv2.getTrackbarPos('V_up', 'trackWindow')

        low = np.array([H_low, S_low, V_low])
        up = np.array([H_up, S_up, V_up])

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, low, up)

        res2 = cv2.resize(mask, (150, 900))
        cv2.imshow('mask', res2)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyWindow('mask')
            cv2.destroyWindow('trackWindow')
            break


def main():
    time0 = time.time()
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(2)
    ret0, img0 = cap1.read()
    time.sleep(1)
    ret1, img1 = cap2.read()
    img = [img0, img1]

    frame, solve_step = img_transform(position_top, position_bottom, img)  # 处理图像
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        print ("The Serial port can't find!")
    else:
        plist_0 = list(plist[0])
        serial_name = plist_0[0]
        serial_find = serial.Serial(serial_name, 115200, timeout=60)
        print ("check which port was really used >", serial_find.name)
        if solve_step:
            solve_step = "*" + solve_step + "#\r\n"
            print solve_step
            serial_find.write(solve_step.encode())

    res1 = cv2.resize(frame, (150, 900))
    cv2.imshow('frame', res1)
    # set_hsv(frame)
    while True:

        if len(plist) > 0:
            count = serial_find.inWaiting()
            if count > 0:
                data = serial_find.read(count)
                print data
                if data == "finish":
                    print time.time() - time0
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            # print[low, up]
            break
        elif k == 32:
            get_point(img0, img1)

if __name__ == "__main__":
    main()

