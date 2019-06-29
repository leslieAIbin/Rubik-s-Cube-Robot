# -*- coding: utf-8 -*-

import cv2
import numpy as np

cam_url = 'http://10.5.121.224:8080/video'   #此处@后的ipv4 地址需要改为app提供的地址
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(0)



def perspective_img():
    img = cv2.imread('B.jpg')
    pts1 = np.float32([[199, 60], [485, 57], [483, 351], [197, 342]])
    pts2 = np.float32([[0, 0], [300, 0], [300, 300], [0, 300]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (300, 300))
    return dst
def addimg():
    img_U = cv2.imread('dst0.jpg')
    img_R = cv2.imread('dst1.jpg')
    img_F = cv2.imread('dst2.jpg')
    img_D = cv2.imread('dst3.jpg')
    img_L = cv2.imread('dst4.jpg')
    img_B = cv2.imread('dst5.jpg')
    dst = [img_U, img_R, img_F, img_D, img_L, img_B]
    frame = np.concatenate(dst, axis=1)
    cv2.imwrite('add_img_test.jpg',frame)
    return frame
while True:
    # frame = cv2.imread("hsv_img.jpg")
    # frame = addimg()
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()



    # x, y = frame.shape[0:2]
    # frame = cv2.resize(frame, (int(y/2), int(x/2)))
    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2)
    print cap1.isOpened()



    #cv2.imshow('dst', dst)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    elif k == 32:
        frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        dst = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        Z = dst.reshape((-1, 3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 7
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape(dst.shape)

        cv2.imshow("res2", res2)
        cv2.imwrite('kmeans.jpg',res2)


cv2.destroyAllWindows()
