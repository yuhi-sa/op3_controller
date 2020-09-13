#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をinnpo-to 
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
from op3_controller.msg import record

def callback(data):
    #subscriberのID　rospy.get_caller_id()
    #subscrineしたデータの中身　data.data
    distance = data.pose[1].position.x
    print(distance)
    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('record_report', Float64, queue_size=1)
    #データをパブリッシュ
    pub.publish(distance)
    #rospy.loginfo(rospy.get_caller_id(), distance)
        
def record():
    #おまじない　ノード名を宣言
    rospy.init_node('record', anonymous=True)
    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('gazebo/model_states', ModelStates, callback)
    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        record()
    except rospy.ROSInitException:
        pass