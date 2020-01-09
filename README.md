SPR 16th
====
developブランチが最新で動作するものです．

Japanopen2020の16期生のSPR (ROS2)


## Branch

develop：最新で動作確認済みver  
develop_〇〇_system：各班でのテスト用

## Install

Pocketsphinx
```
$ python -m pip install --upgrade pip setuptools wheel
$ pip install --upgrade pocketsphinx
```
Svoxpico
```
$ sudo apt-get install -y libttspico-utils
```
## Usage

```
$ git clone https://github.com/rionehome/spr-16th.git  
$ cd spr-16th/  
$ git checkout develop  
$ git clone https://github.com/ItoMasaki/turtlebot_bringup.git  
$ colcon build  
$ source install/setup.bash  
$ ros2 launch spr_cic CIC.launch.py  
```
