#!/usr/bin/env python
# coding: utf-8
import time
from op3_controller.msg import Command 

class Motion:
    def __init__(self,array):
        self.array = array

    def motion(self,num):
        #初期状態
        if num == 100:
            #肘
            self.array.l_el = -0.5 #-1.5
            self.array.r_el = 0.5 #1.5
            #左肩
            self.array.l_sho_pitch = -0.2 # -1.7
            self.array.l_sho_roll =  1.00 #0.00
            #右肩
            self.array.r_sho_pitch = 0.2 #1.7
            self.array.r_sho_roll =  -1.00 #0.00
            #左腰
            self.array.l_hip_pitch = -1.20 #-0.6
            self.array.l_hip_roll = -0.00
            self.array.l_hip_yaw = 0.00
            #右腰
            self.array.r_hip_pitch = 1.20 #0.6
            self.array.r_hip_roll = 0.00
            self.array.r_hip_yaw = 0.00
            #左ひざ
            self.array.l_knee = 2.0
            #右ひざ
            self.array.r_knee = -2.0
            # #左足首
            # self.array.l_ank_pitch = 0.00
            # self.array.l_ank_roll = 0.00
            # #右足首
            # self.array.r_ank_pitch = 0.00
            # self.array.r_ank_roll  = 0.00
        ###########################################################
        elif num == 0:
            #左腰プラス
            self.array.l_hip_pitch = -1.2
            self.array.r_hip_pitch = 1.2

        elif num == 1:
            #左腰マイナス
            self.array.l_hip_pitch = -1.4 #05
            self.array.l_sho_pitch = 0.2 # -1.7
            self.array.r_sho_pitch = 0.2 #1.7
    
        elif num == 2:
            #右腰プラス
            self.array.r_hip_pitch = 1.4 #05
            self.array.l_sho_pitch = -0.2 # -1.7
            self.array.r_sho_pitch = -0.2 #1.7
        
     
        return self.array