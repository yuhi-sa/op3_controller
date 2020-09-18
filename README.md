# op3_controller
[ROBOTIS OP3](https://emanual.robotis.com/docs/en/platform/op3/simulation/)にGazeboシミュレーション内で強化学習を用いて歩行獲得させるROSパッケージ．

# 環境
- [Ubuntu 16.04 LTS](https://wiki.ubuntu.com/XenialXerus/ReleaseNotes/Ja#Ubuntu_16.04.2BMG4wwDCmMPMw7TD8MMk-)
- [ROS kinetic](http://wiki.ros.org/ja/kinetic/Installation/Ubuntu)

# 必要なパッケージのインストール
-  ROBOTIS ROS packages
```
 $ cd ~/catkin_ws/src
 $ git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Framework.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Framework-msgs.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Math.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Demo.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-msgs.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Tools.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Common.git
 $ git clone https://github.com/ROBOTIS-GIT/ROBOTIS-Utility.git
```
[Installing ROBOTIS ROS Packages](https://emanual.robotis.com/docs/en/platform/op3/recovery/#installing-robotis-ros-packages)
- ROS kineticのインストール
```
# apt-get install ros-kinetic-ros-control
# apt-get install ros-kinetic-ros-controllers
# apt-get install ros-kinetic-gazebo-ros-control
```
[If ros-kinetic-desktop-full was used to install, the following packages need to be installed.](https://emanual.robotis.com/docs/en/platform/op3/simulation/#gazebo-installation)
- op3_contoller(このpackage)をインストール
```
cd ~/catkin_ws/src
git clone clone URL
```

# 使い方
1. ROBOTIS-OP3 in Gazeboを起動する
```
roslaunch op3_gazebo robotis_world.launch
```
2. op3_controllerを起動する
```
conda activate (python2が入っているanaconda)
rosrun op3_controller controller.py

conda activate (python3が入っているanaconda)
rosrun op3_controller recorder.py

conda activate (python3が入っているanaconda)
rosrun op3_controller learning.py
```
# おまけ
- GUIコマンドを利用したデモ
```
roslaunch op3_manager op3_gazebo.launch
roslaunch op3_demo demo.launch
```
- [OP3のトピックまとめ](https://docs.google.com/document/d/12Ig3dS7uL5MNAOPqCCfnPpRVxRyvWaqoya56uJFsFv4/edit?usp=sharing)


# 参考
- [ROBOTIS OP3 e-Manual](https://emanual.robotis.com/docs/en/platform/op3/simulation/)
- [ROBOTIS-GIT/ROBOTIS-OP3](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3)
