#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をinnpo-to 
from std_msgs.msg import Float64
from op3_controller.msg import command 

def callback(data):
    #subscriberのID　rospy.get_caller_id()
    #subscrineしたデータの中身　data.data
    rospy.loginfo(rospy.get_caller_id() + 'データきたー %s', data.data)
        

def controller():
    #おまじない　ノード名を宣言
    rospy.init_node('controller', anonymous=True)
    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('record_report', Float64, callback)
    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', command, queue_size=1)

    array = command()
    #左腰
    array.l_hip_pitch =np.random.rand()
    array.l_hip_roll =np.random.rand()
    array.l_hip_yaw =np.random.rand()
    #右腰
    array.r_hip_pitch =np.random.rand()
    array.r_hip_roll =np.random.rand()
    array.r_hip_yaw =np.random.rand()
    #左ひざ
    array.l_knee =np.random.rand()
    #右ひざ
    array.r_knee =np.random.rand()
    #左足首
    array.l_ank_pitch =np.random.rand()
    array.l_ank_roll =np.random.rand()
    #右足首
    array.r_ank_pitch =np.random.rand()
    array.r_ank_roll  =np.random.rand()    

    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #データをパブリッシュ
        pub.publish(array)
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass