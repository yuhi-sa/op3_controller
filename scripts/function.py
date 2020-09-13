#!/usr/bin/env python
# coding: utf-8

import numpy as np


def make_Q_table(row):
    Q_table = np.zeros((row,214))
    return Q_table

def take_action(Q_table,row):
    action = np.zeros((row))

    #最大の価値行動価値のものを選ぶ
    for i in range(row):
        action[i]=-1.06 + 0.01*float(np.argmax(Q_table[i,:]))
    return action

def update_Q_tabele(Q_table,row,distance,history):
    gamma=0.01 #学習率
    history.append(data.data)
    reward = data.data - history[-1]
    
    Q_table = Q_table + (reward + gamma*max(Q_table)-Q_table))
    return Q_table
    

