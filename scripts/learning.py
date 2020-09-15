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


from function import Agent
from motion import Motion
#from videomake import videomake

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F


def reset(time_record):
    print('############## Hello New World ##############')

    #初期値に戻す
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(0)
    pub.publish(array)

    time.sleep(1)

    #初期値に戻す
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(0)
    pub.publish(array)

    #世界を無に
    reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
    reset_world()

    time.sleep(3)

    agent.start_time = time_record
    return time_record

def callback(data):
    time_record = rospy.get_time()
    next_state = []
    #状態を取得
    next_state.append(data.pose[1].position.x)
    next_state.append(data.pose[1].position.y)
    next_state.append(data.pose[1].position.z)
    next_state.append(data.pose[1].orientation.x)
    next_state.append(data.pose[1].orientation.y)
    next_state.append(data.pose[1].orientation.z)
    next_state.append(data.pose[1].orientation.w)
    next_state.append(data.twist[1].linear.x)
    next_state.append(data.twist[1].linear.y)
    next_state.append(data.twist[1].linear.z)
    next_state.append(data.twist[1].angular.x)
    next_state.append(data.twist[1].angular.y)
    next_state.append(data.twist[1].angular.z)

    #進んだ距離を取得
    distance = data.pose[1].position.x

    #ここで学習
    if agent.state is not None:
        #Pytorchで使える形に
        next_state = np.array(next_state)
        next_state = torch.from_numpy(next_state).type(torch.FloatTensor)
        next_state = torch.unsqueeze(next_state, 0)

        reward = distance
        reward = np.array(reward)
        reward = torch.from_numpy(reward).type(torch.FloatTensor)
        reward = torch.unsqueeze(reward, 0)

        agent.memorize(next_state, reward)
        agent.update_q_function()

    agent.state = next_state

    ##################20秒ごとに試行をリセット##################
    if time_record > (agent.start_time+20):
        agent.start_time = reset(time_record)
        agent.episode = agent.episode+1

    #所定回数の時は録画

    #if agent.episode == 2:
        #videomake(agent.episode)

    ######################################################

    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    
    #行動を決定
    agent.action = agent.get_action(agent.episode)

    #行動をパブリッシュ
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(agent.action)
    pub.publish(array)

    
    print(agent.episode+1,'試行目',agent.trial,'回目','time',math.floor(time_record-agent.start_time),'distance',distance)
    agent.trial = agent.trial +1


def controller():
    #おまじない　ノード名を宣言
    rospy.init_node('controller', anonymous=True)

    #初期値に戻す
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(0)
    pub.publish(array)

    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('gazebo/model_states', ModelStates, callback)
    #ループの周期．
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        num_states = 13 #状態数
        num_actions = 17 #状態数
        global agent
        agent = Agent(num_states, num_actions) #強化学習するエージェント

        array = Command()
        global motion
        motion = Motion(array)
        controller()
    except rospy.ROSInitException:
        pass