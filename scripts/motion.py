#!/usr/bin/env python
# coding: utf-8
from op3_controller.msg import Command 

class Motion:
    def __init__(self,array):
        self.array = array

    def motion(self,num):
        #初期状態
        if num == 9:
            #肘
            self.array.l_el = -1.5
            self.array.r_el = 1.5
            #左肩
            self.array.l_sho_pitch = -1.7
            self.array.l_sho_roll =  0.00
            #右肩
            self.array.r_sho_pitch =  1.7
            self.array.r_sho_roll =  0.00
            #左腰
            self.array.l_hip_pitch = -0.6
            self.array.l_hip_roll = 0.00
            self.array.l_hip_yaw = 0.00
            #右腰
            self.array.r_hip_pitch = 0.6
            self.array.r_hip_roll = 0.00
            self.array.r_hip_yaw = 0.00
            #左ひざ
            self.array.l_knee = 0.00
            #右ひざ
            self.array.r_knee = 0.00
            # #左足首
            # self.array.l_ank_pitch = 0.00
            # self.array.l_ank_roll = 0.00
            # #右足首
            # self.array.r_ank_pitch = 0.00
            # self.array.r_ank_roll  = 0.00
        ###########################################################
        # elif num == 0: 
        #     #左肩プラス
        #     self.array.l_sho_roll += 0.1
        #     if self.array.l_sho_roll > 3/2:
        #         self.arry.l_sho_roll = 3/2
        
        # elif num == 1:
        #     #左肩マイナス
        #     self.array.l_sho_roll -= 0.1
        #     if self.array.l_sho_roll < -3/2:
        #         self.arry.l_sho_roll = -3/2
    
        # elif num == 2: 
        #     #右肩プラス
        #     self.array.r_sho_roll += 0.1
        #     if self.array.r_sho_roll > 3/2:
        #         self.arry.r_sho_roll = 3/2
        
        # elif num == 3:
        #     #右肩マイナス
        #     self.array.r_sho_roll -= 0.1
        #     if self.array.r_sho_roll < -3/2:
        #         self.arry.r_sho_roll = -3/2

        # elif num == 7:
        #     #右腰プラス
        #     self.array.r_hip_pitch += 0.3
        #     if self.array.r_hip_pitch > 3/2:
        #         self.array.r_hip_pitch = 3/2

        # elif num == 8:
        #     #右腰マイナス
        #     self.array.r_hip_pitch -= 0.3
        #     if self.array.r_hip_pitch < -3/2:
        #         self.array.r_hip_pitch = -3/2

        elif num == 0:
            #左膝プラス
            self.array.l_knee -= 0.3
            if self.array.l_knee <0.6:
                self.array.l_knee =0.6

        elif num == 1:
            #左膝マイナス
            self.array.l_knee += 0.3
            if self.array.l_knee >-0.6:
                self.array.l_knee =-0.6

        elif num == 2:
            #右膝プラス
            self.array.r_knee += 0.3
            if self.array.r_knee >0.6:
                self.array.r_knee =0.6

        elif num == 3:
            #右膝マイナス
            self.array.r_knee -= 0.6
            if self.array.r_knee <-0.3:
                self.array.r_knee =-0.3

        # elif num == 11:
        #     #左足首プラス
        #     self.array.l_ank_pitch += 0.03
        #     if self.array.l_ank_pitch >1/2:
        #         self.array.l_ank =1/2

        # elif num == 12:
        #     #左足首マイナス
        #     self.array.l_ank_pitch -= 0.03
        #     if self.array.l_ank_pitch <-1/2:
        #         self.array.l_ank =-1/2            

        # elif num == 13:
        #     #左足首プラス
        #     self.array.r_ank_pitch += 0.03
        #     if self.array.r_ank_pitch >1/2:
        #         self.array.r_ank =1/2

        # elif num == 14:
        #     #左足首マイナス
        #     self.array.r_ank_pitch -= 0.03
        #     if self.array.r_ank_pitch <-1/2:
        #         self.array.r_ank =-1/2            
        return self.array