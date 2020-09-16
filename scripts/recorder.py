#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
#メッセージ型をインポート
from std_msgs.msg import String

from videomake import Videomake


def callback(data):
    Videomake(data.data)
   
def recorders():
    #ノード名を宣言
    rospy.init_node('recode', anonymous=True)
    #Subscriberを作成
    rospy.Subscriber('recorder', String, callback)
    rospy.spin()

if __name__ == '__main__':
    recorders()