#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をインポート
from std_msgs.msg import Float64
from op3_controller.msg import Command 

def callback(data):
    #Publisherを作成('トピック名',型,サイズ)
    #左腰
    l_hip_pitch = rospy.Publisher('robotis_op3/l_hip_pitch_position/command', Float64, queue_size=1)
    l_hip_roll = rospy.Publisher('robotis_op3/l_hip_roll_position/command', Float64, queue_size=1)
    l_hip_yaw = rospy.Publisher('robotis_op3/l_hip_yaw_position/command', Float64, queue_size=1)
    #右腰
    r_hip_pitch = rospy.Publisher('robotis_op3/r_hip_pitch_position/command', Float64, queue_size=1)
    r_hip_roll = rospy.Publisher('robotis_op3/r_hip_roll_position/command', Float64, queue_size=1)
    r_hip_yaw = rospy.Publisher('robotis_op3/r_hip_yaw_position/command', Float64, queue_size=1)
    #左ひざ
    l_knee = rospy.Publisher('robotis_op3/l_knee_position/command', Float64, queue_size=1)
    #右ひざ
    r_knee = rospy.Publisher('robotis_op3/r_knee_position/command', Float64, queue_size=1)
    #左足首
    l_ank_pitch = rospy.Publisher('robotis_op3/l_ank_pitch_position/command', Float64, queue_size=1)
    l_ank_roll = rospy.Publisher('robotis_op3/l_ank_roll_position/command', Float64, queue_size=1)  
    #右足首
    r_ank_pitch = rospy.Publisher('robotis_op3/r_ank_pitch_position/command', Float64, queue_size=1)
    r_ank_roll = rospy.Publisher('robotis_op3/r_ank_roll_position/command', Float64, queue_size=1)     

    #データをpublish
    l_hip_pitch.publish(data.l_hip_pitch)
    l_hip_roll.publish(data.l_hip_roll)
    l_hip_yaw.publish(data.l_hip_yaw)
    r_hip_pitch.publish(data.r_hip_pitch)
    r_hip_roll.publish(data.r_hip_roll)
    r_hip_yaw.publish(data.r_hip_yaw)
    l_knee.publish(data.l_knee)
    r_knee.publish(data.r_knee)
    l_ank_pitch.publish(data.l_ank_pitch)
    l_ank_roll.publish(data.l_ank_roll)
    r_ank_pitch.publish(data.r_ank_pitch)
    r_ank_roll.publish(data.r_ank_roll)

def controller():
    #ノード名を宣言
    rospy.init_node('controller', anonymous=True)
    #Subscriberを作成
    sub = rospy.Subscriber('command_pub', Command, callback)
    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass