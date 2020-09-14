#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をinnpo-to 
from std_msgs.msg import Float64
from op3_controller.msg import command 

#強化学習のために作ったライブラリをインポート
from function import make_Q_table
from function import take_action
from function import update_Q_tabele

history =[0]

def callback(data):
    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', command, queue_size=1)
    distance =data.data
    print(distance)

    ##############強化学習頑張れーーー#################
    # Qtableを作る(最初の一回だけ)
    #if ikkaime == 0:
    row = 12
    Q_table = make_Q_table(row)
    #ikkaime = 1
    
    #行動を決定
    action = take_action(Q_table,row)

    #行動価値関数を更新
    Q_table = update_Q_tabele(Q_table,row,distance,history)

    ################################################
    array = command()
    #左腰
    array.l_hip_pitch = action[0]
    array.l_hip_roll = action[1]
    array.l_hip_yaw = action[2]
    #右腰
    array.r_hip_pitch = action[3]
    array.r_hip_roll = action[4]
    array.r_hip_yaw = action[5]
    #左ひざ
    array.l_knee = action[6]
    #右ひざ
    array.r_knee = action[7]
    #左足首
    array.l_ank_pitch = action[8]
    array.l_ank_roll = action[9]
    #右足首
    array.r_ank_pitch = action[10]
    array.r_ank_roll  = action[11]
    #データをパブリッシュ
    pub.publish(array)
        

def controller():
    #おまじない　ノード名を宣言
    rospy.init_node('controller', anonymous=True)
    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('record_report', Float64, callback) 

    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass