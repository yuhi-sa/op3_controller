#!/usr/bin/env python
# coding: utf-8

#スクリーンショットを動画にする
import numpy as np
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import pyautogui as pag
import os
import time


def Videomake(episode):
    print('録画スタート')
    #保存するファイル名
    img_dir_name="./op3_movie"+episode

    #画像保存用ファイルを作成
    os.makedirs(img_dir_name, exist_ok=True)

    # 動画用の画像（スクリーンショット）を用意
    #画像を格納するリスト
    img_list = []
    img_No = 0
    #動画のフレームレイト
    FPS=14
    #録画したい時間
    movie_time=40
    #上記フレームレイトと録画時間を満たす繰り返し数
    photo_no=FPS*movie_time
    #繰り返しスクリーンショットを撮り、ファイルに保存
    for i in range(0, photo_no, 1):
        img_No = img_No + 1
        img=pag.screenshot()
        img=np.asarray(img)
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img_output= '{}/{:010d}.png'.format(img_dir_name, img_No)
        cv2.imwrite(img_output, img)
        img_list.append(img_output)

    # 保存された画像を繋げて動画作成
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video  = cv2.VideoWriter(img_dir_name+'desktop_capture.mp4', fourcc, FPS, (3840, 1080))#画面サイズに応じて変更必要
    for s in img_list:
        img = cv2.imread(s)
        video.write(img)

    video.release()
    print('終了')