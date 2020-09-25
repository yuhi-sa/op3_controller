#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from collections import namedtuple

BATCH_SIZE = 32
CAPACITY = 10000000
GAMMA = 0.01

#namedtupleを作成
Transition = namedtuple(
    'Transition', ('state', 'action', 'next_state', 'reward')
)


#経験を保存するメモリクラスを定義
class ReplayMemory:
    def __init__(self,CAPACITY):
        self.capacity = CAPACITY #メモリの最大長の長さ
        self.memory = [] #経験を保存する変数
        self.index = 0 #保存するindexを示す変数
    
    def push(self, state, action, next_state, reward):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.index] = Transition(state, action, next_state, reward)
        self.index = (self.index + 1)%self.capacity #保存するindexを1ずらす
    
    def sample(self, batch_size):
        #batchサイズ分だけランダムに保存内容を取り出す
        return random.sample(self.memory, batch_size)

    def __len__(self):
        #関数lenに対して，現在の変数memoryの長さを返す
        return len(self.memory)


class Brain:
    def __init__(self, num_states, num_actions):
        self.actions = num_actions
        self.states = num_states
        #経験を記憶するメモリオブジェクトを作成
        self.memory = ReplayMemory(CAPACITY)
        
        #ニューラルネットワークを構成
        self.model = nn.Sequential()
        self.model.add_module('fc1', nn.Linear(self.states, 32))
        self.model.add_module('relu1', nn.ReLU())
        self.model.add_module('fc2', nn.Linear(32,32))
        self.model.add_module('relu2', nn.ReLU())
        self.model.add_module('fc3', nn.Linear(32, self.actions))

        #最適化手法の設定
        self.optimizer = optim.Adam(self.model.parameters(),lr=0.0001)

    def replay(self):
        #経験反復でネットワークの結合パラメータを学習
        if len(self.memory) < BATCH_SIZE:
            #メモリサイズがメモリバッチっより小さい場合は何もしない
            return
        transitions = self.memory.sample(BATCH_SIZE)

        #バッチ作成
        batch = Transition(*zip(*transitions))
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        #ネットワークを推論モードに
        self.model.eval()

        state_action_values = self.model(state_batch).gather(1 ,action_batch)
        
        #next_stateがあるかどうかをチェック
        non_final_mask = torch.ByteTensor(tuple(map(lambda s:s is not None, batch.next_state)))

        #next_stateを求める
        next_state_values = torch.zeros(BATCH_SIZE)
        next_state_values[non_final_mask] = self.model(non_final_next_states).max(1)[0].detach()

        #教師信号となるQ(s_t,a_t)をQ学習の式から求める
        expected_state_action_values = reward_batch + GAMMA*next_state_values

        #ネットワークを訓練モードに
        self.model.train()

        #損失関数を計算する
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        #結合パラメータを更新する
        self.optimizer.zero_grad() #勾配をリセット
        loss.backward() #バックプロパゲーション
        self.optimizer.step() #結合パラメータの更新

    def decide_action(self, state, episode):
        epsilon = 1/(episode+1)

        if epsilon <= np.random.uniform(0,1):
            #ネットワークを推論モードに
            self.model.eval()
            with torch.no_grad():
                action = self.model(state).max(1)[1].view(1,1) #ネットワーク出力の最大値をだす
            # 0,1の行動をランダムに返す
        else:
            action = torch.LongTensor([[random.randrange(self.actions)]])
        return action



# エージェント
class Agent:
    def __init__(self, num_states, num_actions):
        self.brain = Brain(num_states, num_actions)
        self.state = None
        self.next_state = []
        self.action = 0
        self.start_time = 0
        self.trial = 0
        self.episode = 0
        self.last_index = 0
        self.history = []

    def update_q_function(self):
        self.brain.replay()
    
    def get_action(self, episode):
        action = self.brain.decide_action(self.state, episode)
        return action
    
    def memorize(self, state_next, reward):
        self.brain.memory.push(self.state, self.action, state_next, reward)