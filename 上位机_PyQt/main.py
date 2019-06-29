# -*- coding: utf-8 -*-

import sys
import cv2
import os
import time
import numpy as np
import json
import kociemba
import serial
import serial.tools.list_ports

from mainWindow import Ui_Form
from hsvWindow import Ui_Dialog

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cube_assert

with open('color_info.json', 'r', encoding='utf-8') as f_color_read:
    read_color_str = json.load(f_color_read)
    read_color_dict = json.loads(read_color_str)
    print("read hsv data success!")

with open('position.json', 'r', encoding='utf-8') as f_position_read:
    read_position_str = json.load(f_position_read)
    read_position_dict = json.loads(read_position_str)
    print("read position data success!")
    

class MyHsvWindow(QDialog, Ui_Dialog):
    def __init__(self, color, frame):
        super(MyHsvWindow, self).__init__()
        self.setupUi(self)
        self.frame = cv2.resize(frame, (100, 600))
        self.color = color
        self.lineEdit.setText("%d，%d" % (color[0][0], color[1][0]))
        self.lineEdit_2.setText("%d，%d" % (color[0][1], color[1][1]))
        self.lineEdit_3.setText("%d，%d" % (color[0][2], color[1][2]))

        frame_temp = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        qt_frame = QImage(frame_temp.data, frame_temp.shape[1], frame_temp.shape[0], QImage.Format_RGB888)
        self.label_14.setPixmap(QPixmap.fromImage(qt_frame))

        self.spinBox.setValue(color[0][0])
        self.spinBox_2.setValue(color[1][0])
        self.spinBox_3.setValue(color[0][1])
        self.spinBox_4.setValue(color[1][1])
        self.spinBox_5.setValue(color[0][2])
        self.spinBox_6.setValue(color[1][2])

    def get_dialog_value(self):
        data0 = [self.spinBox.value(), self.spinBox_3.value(), self.spinBox_5.value()]
        data1 = [self.spinBox_2.value(), self.spinBox_4.value(), self.spinBox_6.value()]
        return [data0, data1]

    def box_value_changed(self):
        mask_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask_temp = cv2.inRange(mask_hsv, np.array([self.spinBox.value(), self.spinBox_3.value(), self.spinBox_5.value()]),
                                 np.array([self.spinBox_2.value(), self.spinBox_4.value(), self.spinBox_6.value()]))
        mask_temp = cv2.cvtColor(mask_temp, cv2.COLOR_BGR2RGB)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(mask_temp, cv2.MORPH_CLOSE, kernel)
        qt_mask = QImage(closing.data, closing.shape[1], closing.shape[0], QImage.Format_RGB888)
        self.label_15.setPixmap(QPixmap.fromImage(qt_mask))


# 主窗口
class MyMainWindow(QMainWindow, Ui_Form):

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

        self.cap_index0 = None
        self.cap_index1 = None
        self.cap0 = None
        self.cap1 = None
        self.th0 = None
        self.th1 = None

        self.color_num = [0 for _ in range(54)]  # 用来暂存魔方的色块信息，用数字代表颜色 ：蓝白橙绿黄红---（1-6）
        self.step = ""
        # 绘图用U R F D L B起始坐标
        self.cube_list = [[270, 90], [90, 180], [180, 90], [90, 90], [90, 0], [0, 90]]
        # 绘图用RGB值
        self.color_RGB = [[12, 62, 192], [255, 255, 255], [255, 128, 0], [11, 136, 30], [255, 255, 0], [255, 0, 0]]
        # json文件导入参数
        self.position = read_position_dict
        self.color_hsv = read_color_dict
        self.img_size = 20

        self.frame0 = None
        self.frame1 = None

        self.frame = []
        self.point_flag = 0
        self.reset_flag = 0
        # 初始化一个定时器

    def print_point(self, event, x, y, flags, param):
        if self.point_flag == 0:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.position['position0'].append([x, y])
                print(self.position['position0'])
            if event == cv2.EVENT_RBUTTONDOWN:
                self.position['position0'].pop()
                print(self.position['position0'])

        if self.point_flag == 1:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.position['position1'].append([x, y])
                print(self.position['position1'])
            if event == cv2.EVENT_RBUTTONDOWN:
                self.position['position1'].pop()
                print(self.position['position1'])

    # 根据魔方标准字母排列创建十字架图形
    def cube_draw(self):
        bg_img = np.zeros((359, 269, 3), np.uint8)
        # 三通道都是147为灰色
        bg_img[:, :] = [147, 147, 147]

        # 012345 - 蓝白橙绿黄红
        for i in range(len(self.color_num)):
            x = self.cube_list[i // 9][0] + (i % 9 // 3) * 30
            y = self.cube_list[i // 9][1] + (i % 3) * 30

            cube_b = self.color_RGB[self.color_num[i]-1][0]
            cube_g = self.color_RGB[self.color_num[i]-1][1]
            cube_r = self.color_RGB[self.color_num[i]-1][2]

            bg_img[x:x + 29, y:y + 29] = [cube_r, cube_g, cube_b]
        return bg_img

    # 透视变换 拼接
    def img_connect(self):
        pts0 = np.float32([[0, 0], [3 * self.img_size, 0], [0, 3 * self.img_size], [3 * self.img_size, 3 * self.img_size]])
        position_side = [[self.position['position0'][1], self.position['position0'][2],
                          self.position['position0'][0], self.position['position0'][6]],
                         [self.position['position0'][6], self.position['position0'][2],
                          self.position['position0'][4], self.position['position0'][3]],
                         [self.position['position0'][0], self.position['position0'][6],
                          self.position['position0'][5], self.position['position0'][4]],
                         [self.position['position1'][4], self.position['position1'][5],
                          self.position['position1'][6], self.position['position1'][0]],
                         [self.position['position1'][2], self.position['position1'][3],
                          self.position['position1'][6], self.position['position1'][4]],
                         [self.position['position1'][1], self.position['position1'][2],
                          self.position['position1'][0], self.position['position1'][6]]]

        dst = []
        # 透视变换
        for i in range(6):
            pts = np.float32(position_side[i])
            m = cv2.getPerspectiveTransform(pts, pts0)
            if i < 3:
                dst.append(cv2.warpPerspective(self.frame0, m, (3 * self.img_size, 3 * self.img_size)))
            else:
                dst.append(cv2.warpPerspective(self.frame1, m, (3 * self.img_size, 3 * self.img_size)))
        # 拼接
        self.frame = np.concatenate(dst)

    # 阈值分割
    def img_transform(self):
        # 得到每种颜色的阈值掩模
        mask = []
        frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask.append(cv2.inRange(frame_hsv, np.array(self.color_hsv['blue'][0]), np.array(self.color_hsv['blue'][1])))
        mask.append(cv2.inRange(frame_hsv, np.array(self.color_hsv['white'][0]), np.array(self.color_hsv['white'][1])))
        mask.append(cv2.inRange(frame_hsv, np.array(self.color_hsv['orange'][0]), np.array(self.color_hsv['orange'][1])))
        mask.append(cv2.inRange(frame_hsv, np.array(self.color_hsv['green'][0]), np.array(self.color_hsv['green'][1])))
        mask.append(cv2.inRange(frame_hsv, np.array(self.color_hsv['yellow'][0]), np.array(self.color_hsv['yellow'][1])))
        kernel = np.ones((2, 2), np.uint8)
        for i in range(5):
            closing = cv2.morphologyEx(mask[i], cv2.MORPH_CLOSE, kernel)
            mask[i] = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        # 确定位置,用数字代表颜色 同阈值掩模索引
        # i 表示 6个掩模图像
        # j 表示每幅图像有54个色块

        self.color_num = [0 for _ in range(54)]
        width = self.img_size  # 掩模色块宽度（宽和高相等）
        indent = int(width * 0.15)  # 缩进值，排除色块边缘

        for j in range(len(self.color_num)):
            cube_x = j % 3 * width  # 即将处理的色块开始x坐标
            cube_y = j // 3 * width   # 即将处理的色块开始y坐标
            # 图像高度为3*6个色块高度  宽度为3个色块宽度
            # 图像索引格式image[height, width]
            for i in range(5):
                closing = mask[i]
                if closing[cube_y + width//2, cube_x + width//2] == 255:
                    self.color_num[j] = i+1
                    break
                else:
                    hist_mask = np.zeros(closing.shape[:2], np.uint8)
                    hist_mask[cube_y + indent:cube_y + width - indent, cube_x + indent:cube_x + width - indent] = 255
                    # 只查看白色像素个数，即当前颜色掩模像素点
                    hist = cv2.calcHist([closing], [0], hist_mask, [1], [255, 256])
                    if j % 9 == 4 and hist[0] > width * width // 8:
                        if self.color_num[j] == 0:
                            self.color_num[j] = i+1
                            break
                    elif hist[0] > width * width // 4:
                        if self.color_num[j] == 0:
                            self.color_num[j] = i+1
                            break

        # 利用中心色块数字，用位置"U R F D L B"替换，得到标准魔方编码
        self.step = cube_assert.cube_assert(self.color_num)

    # 发送解魔方步骤到STM32
    def send2stm32(self):
        if not self.step:
            return
        step_send = "*" + self.step + " #\r\n"
        step_send = step_send.replace("2 ", "2")
        step_send = step_send.replace("' ", "1")
        step_send = step_send.replace(" ", "0")
        print(step_send)
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")
            return
        else:
            try:
                plist_0 = list(plist[0])
                serial_name = plist_0[0]
                serial_find = serial.Serial(serial_name, 115200, timeout=60)
                print("check which port was really used >", serial_find.name)
                serial_find.write(step_send.encode())
            except:
                print("The serial port busy!")
                raise
            return

    def button_run_clicked(self):
        if self.frame0 is None or self.frame1 is None:
            QMessageBox.warning(self, '警告', '摄像头未加载！')
            return
        self.img_connect()
        self.img_transform()
        self.send2stm32()

        rgb_img = self.cube_draw()
        rgb_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_img.shape
        qt_img = QImage(rgb_img.data, width, height, 3*width, QImage.Format_RGB888)
        self.label_9.setPixmap(QPixmap.fromImage(qt_img))

    def button_setpos_clicked(self):
        if self.frame0 is None or self.frame1 is None:
            QMessageBox.warning(self, '警告', '摄像头未加载！')
            return

        cv2.namedWindow('SetPos')
        cv2.setMouseCallback('SetPos', self.print_point)

        while True:
            if self.point_flag == 0:
                temp = self.frame0.copy()
                position_temp = self.position['position0']
            elif self.point_flag == 1:
                temp = self.frame1.copy()
                position_temp = self.position['position1']
            else:
                with open("./position.json", "w") as f_position_write:
                    position_write_str = json.dumps(self.position, sort_keys=True, indent=4, ensure_ascii=False)
                    json.dump(position_write_str, f_position_write, ensure_ascii=False)
                    self.point_flag = 0
                break

            for i in range(len(position_temp)):
                x = position_temp[i][0]
                y = position_temp[i][1]
                cv2.line(temp, (x-5, y-5), (x+5, y+5), (255, 0, 0), 4)
                cv2.line(temp, (x-5, y+5), (x+5, y-5), (255, 0, 0), 4)
            cv2.imshow('SetPos', temp)

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                self.point_flag = 0
                break
            if k == 13 and len(position_temp) == 7:
                self.point_flag += 1

        cv2.destroyWindow('SetPos')
        self.reset_flag = 1

    def button_sethsv_clicked(self):
        if self.frame0 is None or self.frame1 is None:
            QMessageBox.warning(self, '警告', '摄像头未加载！')
            return
        self.img_connect()
        child_window = MyHsvWindow(self.color_hsv[self.comboBox.currentText()], self.frame)
        if child_window.exec_():
            self.color_hsv[self.comboBox.currentText()] = child_window.get_dialog_value()
            with open('color_info.json', 'w', encoding='utf-8') as f_color_write:
                write_color_str = json.dumps(self.color_hsv, sort_keys=True, indent=4, ensure_ascii=False)
                json.dump(write_color_str, f_color_write, ensure_ascii=False)
                print("write color hsv data success!")

    def button_debug_clicked(self):
        self.step = self.lineEdit.text()
        self.send2stm32()

    def button_tools_clicked(self):
        os.system('README.txt')

    def button_loadcam1_clicked(self):
        if self.cap0 is not None:
            self.th0.quit()
            self.cap0.release()
        self.cap_index0 = self.comboBox_2.currentIndex()
        if self.cap_index0 == self.cap_index1:
            print("该摄像头被其他进程占用")
            return
        self.cap0 = cv2.VideoCapture(self.cap_index0)
        self.th0 = ImgThread(self.cap0)
        self.th0.change_image.connect(self.load_image0)
        self.th0.start()

    def button_loadcam2_clicked(self):
        if self.cap1 is not None:
            self.th1.quit()
            self.cap1.release()
        self.cap_index1 = self.comboBox_3.currentIndex()
        if self.cap_index1 == self.cap_index0:
            print("该摄像头被其他进程占用")
            return
        self.cap1 = cv2.VideoCapture(self.cap_index1)
        self.th1 = ImgThread(self.cap1)
        self.th1.change_image.connect(self.load_image1)
        self.th1.start()

    def load_image0(self):
        if self.th0.frame is not None:
            self.label_7.setPixmap(QPixmap.fromImage(self.th0.load_img))
            self.frame0 = self.th0.frame

    def load_image1(self):
        if self.th1.frame is not None:
            self.label_8.setPixmap(QPixmap.fromImage(self.th1.load_img))
            self.frame1 = self.th1.frame


class ImgThread(QThread):

    change_image = pyqtSignal()

    def __init__(self, cap):
        super(ImgThread, self).__init__()
        self.cap = cap
        self.frame = None
        self.load_img = None

    def run(self):
        while self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if ret:
                    self.frame = frame
                    rgb_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    qt_img = QImage(rgb_img.data, rgb_img.shape[1], rgb_img.shape[0], QImage.Format_RGB888)
                    self.load_img = qt_img.scaled(320, 240, Qt.KeepAspectRatio)
                    self.change_image.emit()  # 发出信号
                    self.sleep(0.01)
                else:
                    print('get camera image failed!')
            except:
                raise


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

