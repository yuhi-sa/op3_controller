#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
import rospy
import math
import sys
import csv
import threading
from datetime import datetime
from std_srvs.srv import Empty
#メッセージ型をインポート
from std_msgs.msg import Float64
from std_msgs.msg import String
from op3_controller.msg import Command 
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from transform import quaternion_to_euler_zyx 


from function import Agent
from motion import Motion
from videomake import Videomake

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

########################################################################################
def reset(time_record):
    print('############## 新世界へようこそ##############')

    #初期値に戻す
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)

    time.sleep(1)

    #世界を無に
    reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
    reset_world()

    #ファーストポジション
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)

    #しゃがんだ体制スタート
    # pub = rospy.Publisher('gazebo/set_model_state',ModelState,queue_size=1)
    # state_msg = ModelState()
    # state_msg.model_name = 'robotis_op3'
    # state_msg.pose.position.x = 0.0
    # state_msg.pose.position.y = 0.0
    # state_msg.pose.position.z = 0.3
    # state_msg.pose.orientation.x = 0.0
    # state_msg.pose.orientation.y = 1.0
    # state_msg.pose.orientation.z = 0.0
    # state_msg.pose.orientation.w = 0.5
    # pub.publish(state_msg)

    time.sleep(2)
    return time_record

########################################################################################
def callback(data):
    #next_stateを初期化
    if len(agent.next_state)>0:
        agent.next_state = []

    #状態を取得
    agent.next_state.append(data.pose[1].position.x)
    agent.next_state.append(data.pose[1].position.y)
    agent.next_state.append(data.pose[1].position.z)
    agent.next_state.append(data.pose[1].orientation.x)
    agent.next_state.append(data.pose[1].orientation.y)
    agent.next_state.append(data.pose[1].orientation.z)
    agent.next_state.append(data.pose[1].orientation.w)
    agent.next_state.append(data.twist[1].linear.x)
    agent.next_state.append(data.twist[1].linear.y)
    agent.next_state.append(data.twist[1].linear.z)
    agent.next_state.append(data.twist[1].angular.x)
    agent.next_state.append(data.twist[1].angular.y)
    agent.next_state.append(data.twist[1].angular.z)
########################################################################################


def learning(next_state,time_record):

    #進んだ距離を取得
    distance = next_state[0]
    #横にずれた幅
    gosa = abs(next_state[1])
    #高さ
    high = next_state[2]

    reward_tmp = 0

    #ここで学習

    #Pytorchで使える形に
    next_state = np.array(next_state)
    next_state = torch.from_numpy(next_state).type(torch.FloatTensor)
    next_state = torch.unsqueeze(next_state, 0)

    #報酬設計
    if high >=0.145 and distance-agent.distance_tmp>=0:
        reward = (distance-agent.distance_tmp)*1000  #- (gosa-agent.gosa_tmp)*10
    elif high >=0.145 and distance-agent.distance_tmp<0:
        reward = (distance-agent.distance_tmp)*10  #- (gosa-agent.gosa_tmp)*10
    elif high < 0.145:
        reward = -2 + (distance-agent.distance_tmp)*10 #- (gosa-agent.gosa_tmp)*10
    
    agent.distance_tmp = distance
    agent.gosa_tmp = gosa
    reward_tmp = reward
    #Pytorchで使える形に
    reward = np.array(reward)
    reward = torch.from_numpy(reward).type(torch.FloatTensor)
    reward = torch.unsqueeze(reward, 0)

    if agent.state is not None:
        agent.memorize(next_state, reward)
        agent.update_q_function()

    agent.state = next_state

    print('試行数:', agent.episode-1, '回数：', agent.trial, '秒数：', math.floor(time_record-agent.start_time), '報酬：', math.floor(reward_tmp*100)/100, 
            '距離：', distance)
    

    ###所定回数の時は録画###############################################
    pub2 = rospy.Publisher('recorder', String, queue_size=1)
    if (agent.episode%200) -2 == 0:
        if not agent.last_index == agent.episode:
            data = str(agent.last_index)
            pub2.publish(data)
            agent.last_index = agent.episode
    #################################################################
    
    ###20秒ごとに試行をリセット はじめの一回目は一応姿勢治すためにリセット###########
    if time_record > (agent.start_time+20) or agent.episode==1 or high < 0.145:
        #世界よさらば
        print('############## さらば世界 ##############')
        agent.start_time = reset(time_record)
        agent.trial = 0
        agent.episode = agent.episode+1
        agent.history.append(distance)
    
        #距離を記録
        if agent.episode == 50:
            file = open('distance_record.csv', 'w') 
            w = csv.writer(file)
            w.writerow(agent.history)
            file.close()

        #行動履歴を出力
        filename1 = "action" + str(agent.episode) +".csv"
        file1 = open(filename1, 'w') 
        w = csv.writer(file1)
        w.writerow(agent.history1)
        file1.close()

        #高さ履歴を出力
        filename2 = "high" + str(agent.episode) +".csv"
        file2 = open(filename2, 'w') 
        w = csv.writer(file2)
        w.writerow(agent.history2)
        file2.close()

        #行動と高さを初期化
        agent.history1 = []
        agent.history2 = []

    #################################################################


    #Publisherを作成('トピック名',型,サイズ)
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    
    #行動を決定
    if agent.state is not None:
        agent.action = agent.get_action(agent.episode)

    #行動をパブリッシュ
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(agent.action)
    pub.publish(array)


    #報酬の履歴を保存
    #agent.history.append([agent.trial,distance])

    agent.trial = agent.trial +1

    #行動を記録
    tmp_action = agent.action.to('cpu').detach().numpy().copy()
    if tmp_action[0][0] == 0:
        agent.history1.append(0)
    if tmp_action[0][0] == 1:
        agent.history1.append(1)
    if tmp_action[0][0] == 2:
        agent.history1.append(2)

    #高さを記録
    agent.history2.append(high)

########################################################################################

def controller():
    #ノード名を宣言
    rospy.init_node('controller', anonymous=True)

    #初期値に戻す
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)

    #Subscriberを作成．トピックを読み込む．
    sub = rospy.Subscriber('gazebo/model_states', ModelStates, callback)
    #ループの周期．
    rate = rospy.Rate(1000)

    while not rospy.is_shutdown():
        time_record = rospy.get_time()

        if len(agent.next_state) > 0:
            learning(agent.next_state,time_record)
        #行動周期を遅らせる
        time.sleep(0.025)
        rate.sleep()

########################################################################################

if __name__ == '__main__':
    try:
        num_states = 13 #状態数
        num_actions = 3 #行動数
        global agent
        agent = Agent(num_states, num_actions) #強化学習するエージェント
        array = Command()
        global motion
        motion = Motion(array)

        controller()
    except rospy.ROSInitException:
        pass