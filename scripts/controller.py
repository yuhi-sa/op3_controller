#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をinnpo-to 
from std_msgs.msg import Float64

def callback(data):
    #subscriberのID　rospy.get_caller_id()
    #subscrineしたデータの中身　data.data
    rospy.loginfo(rospy.get_caller_id() + 'データきたー %s', data.data)
        

def controller():
    #おまじない　ノード名を宣言
    rospy.init_node('controller', anonymous=True)
    #Subscriberを作成．トピックを読み込む．
    #sub = rospy.Subscriber('command', String, callback)
    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('robotis_op3/head_pan_position/command', Float64, queue_size=1)
    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #データをパブリッシュ
        pub.publish(10)
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass