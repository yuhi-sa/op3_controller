#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
import rospy
import math
from datetime import datetime
from std_srvs.srv import Empty
#メッセージ型をインポート
from std_msgs.msg import Float64
from std_msgs.msg import String
from op3_controller.msg import Command 
from gazebo_msgs.msg import ModelStates

#強化学習のために作ったライブラリをインポート
from function import make_Q_table
from function import take_action
from function import update_Q_tabele

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

history =[0]

global start_time
start_time = 0
global trial
trial = 0
global Q_table

#動かせる部位の数
global action_len
action_len = 12


def reset(time_record):
    print('############## Hello New World ##############')
    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    #初期状態
    array_r = Command()
    #左腰
    array_r.l_hip_pitch = 0.00
    array_r.l_hip_roll = 0.00
    array_r.l_hip_yaw = 0.00
    #右腰
    array_r.r_hip_pitch = 0.00
    array_r.r_hip_roll = 0.00
    array_r.r_hip_yaw = 0.00
    #左ひざ
    array_r.l_knee = 0.00
    #右ひざ
    array_r.r_knee = 0.00
    #左足首
    array_r.l_ank_pitch = 0.00
    array_r.l_ank_roll = 0.00
    #右足首
    array_r.r_ank_pitch = 0.00
    array_r.r_ank_roll  = 0.00
    #データをパブリッシュ
    pub.publish(array_r)

    time.sleep(1)
    pub.publish(array_r)
    time.sleep(2)
    reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
    reset_world()
    time.sleep(3)
    start_time = time_record
    return time_record

def callback(data):
    global start_time
    time_record = rospy.get_time()
    state = []
    #状態を取得
    state.append(data.pose[1].position.x)
    state.append(data.pose[1].position.y)
    state.append(data.pose[1].position.z)
    state.append(data.pose[1].orientation.x)
    state.append(data.pose[1].orientation.y)
    state.append(data.pose[1].orientation.z)
    state.append(data.pose[1].orientation.w)
    state.append(data.twist[1].linear.x)
    state.append(data.twist[1].linear.y)
    state.append(data.twist[1].linear.z)
    state.append(data.twist[1].angular.x)
    state.append(data.twist[1].angular.y)
    state.append(data.twist[1].angular.z)

    #進んだ距離を取得
    distance = data.pose[1].position.x

    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', Command, queue_size=1)

    #20秒ごとにリセット
    if time_record > (start_time+10):
        start_time = reset(time_record)

    ##############  強化学習頑張れーーー  #################
    # Qtableを作る(最初の一回だけ)
    global trial
    global action_len
    if trial == 0:
        state_len = len(state)
        global Q_table
        Q_table = make_Q_table(state_len, action_len)
    
    #行動を決定
    action = take_action(Q_table, trial, state, action_len)

    #行動価値関数を更新
    #Q_table = update_Q_tabele(Q_table)

    ################################################
    array = Command()
    #左腰
    array.l_hip_pitch = action[0]
    array.l_hip_roll = action[1]
    array.l_hip_yaw = action[2]
    #右腰
    array.r_hip_pitch = action[3]
    array.r_hip_roll = action[4]
    array.r_hip_yaw = action[5]
    #左ひざ
    array.l_knee = action[6]*0
    #右ひざ
    array.r_knee = action[7]*0
    #左足首
    array.l_ank_pitch = action[8]
    array.l_ank_roll = action[9]
    #右足首
    array.r_ank_pitch = action[10]
    array.r_ank_roll  = action[11]
    #データをパブリッシュ
    pub.publish(array)
    
    print(trial,'回目','time',math.floor(time_record-start_time),'distance',distance)
    trial = trial +1


def controller():
    #おまじない　ノード名を宣言
    rospy.init_node('controller', anonymous=True)
    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('gazebo/model_states', ModelStates, callback)
    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass