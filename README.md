SPR 16th
====

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
ReSpeaker

以下パソコンにReSpeakerを繋いだ状態で

```
$ git checkout develop 
$ cd sound_system/prepare_tools/
$ sh respeaker.sh
```
dlib
```
$ sudo apt-get install -y cmake gfortran graphicsmagick libgraphicsmagick1-dev libatlas-base-dev libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev libjpeg-dev liblapack-dev libswscale-dev python-dev python-protobuf software-properties-common
$ pip3 install dlib --user
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
