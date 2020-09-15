#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F


def make_Q_table(state_len, action_len):

    # ニューラルネットワークを構築
    Q_table = nn.Sequential()
    Q_table.add_module('fc1', nn.Linear(state_len, 10))
    Q_table.add_module('relu1', nn.ReLU())
    Q_table.add_module('fc2', nn.Linear(10, 10))
    Q_table.add_module('relu2', nn.ReLU())
    Q_table.add_module('fc3', nn.Linear(10, action_len))

    return Q_table

def take_action(Q_table, trial, state, action_length):
    # ε-greedy法で徐々に最適行動のみを採用する
    epsilon = 0.5 * (30000 / (trial + 1))

    if epsilon <= np.random.uniform(0, 1):
        Q_table.eval()  # ネットワークを推論モードに切り替える
        with torch.no_grad():
            state = torch.Tensor(state)
            action = Q_table(state)
            #print(action)

    else:
        # 0,1の行動をランダムに返す
        action = [np.random.rand()-0.5, #0
                    np.random.rand()-0.5, #1
                    np.random.rand()-0.5, #2
                    np.random.rand()-0.5, #3
                    np.random.rand()-0.5, #4
                    np.random.rand()-0.5, #5
                    -abs(np.random.rand()-0.5), #6 膝は前に曲がると痛そうなので負の値に
                    -abs(np.random.rand()-0.5), #7 膝は前に曲がると痛そうなので負の値に
                    np.random.rand()-0.5, #8
                    np.random.rand()-0.5, #9
                    np.random.rand()-0.5, #10
                    np.random.rand()-0.5  #11
                ]
    return action


def update_Q_tabele(Q_table):
    Q_table.train()

    Q_table.optimizer.zero_grad()  # 勾配をリセット
    Q_table.loss.backward()  # バックプロパゲーションを計算
    Q_table.optimizer.step()  # 結合パラメータを更新

    return Q_table
    

