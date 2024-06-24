# webots_ros2_ld90

* URDF Source: [https://github.com/OmronAPAC/Omron_LD_ROS_Package](https://github.com/OmronAPAC/Omron_LD_ROS_Package)


![image](https://github.com/inmo-jang/webots_ros2_ld90/assets/42867523/abfe8694-f1bb-4448-94d9-75d692c491ae)


### How to use this

```
colcon build
source install/local_setup.bash

# 빈 map에서 실행
ros2 launch webots_ros2_ld90 robot_launch.py

# 과제 map에서 실행
ros2 launch webots_ros2_ld90 robot_launch.py world:=contest.wbt

# SLAM용 사람 없는 map에서 실행
ros2 launch webots_ros2_ld90 robot_launch.py world:=contest_non_ped.wbt

# SLAM용 사람 없는 + 함정 없는 map에서 실행
ros2 launch webots_ros2_ld90 robot_launch.py world:=contest_non_ped_non_manhole.wbt

```

### ros2 command
```
1) ros2 topic echo /tf
   ros2 run tf2_tools view_frames
2) /cmd_vel...
	move forward: ros2 topic pub /cmd_vel geometry_msgs/Twist "linear: {x: 0.3}"
	move backward: ros2 topic pub /cmd_vel geometry_msgs/Twist "linear: {x: -0.3}"
	left rotation: ros2 topic pub /cmd_vel geometry_msgs/Twist "angular: {z: 0.5}"
	right rotation: ros2 topic pub /cmd_vel geometry_msgs/Twist "angular: {z: -0.5}"
3) ros2 topic echo /odom, ros2 topic echo /joint_states
4) ros2 topic echo /scan
```

### rviz map command
```
Start RVIZ) ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz

Mapping using SLAM) 
	1) ros2 launch nav2_bringup bringup_launch.py params_file:=resource/nav2_params.yaml map:=my_map.yaml slam:=True
	2) ros2 run teleop_twist_keyboard teleop_twist_keyboard
	3) ros2 run nav2_map_server map_saver_cli -f my_map
... my_map.pgm 및 my_map.yaml 파일 저장 확인

Use map) ros2 launch nav2_bringup bringup_launch.py params_file:=resource/nav2_params.yaml map:=resource/my_mapff.yaml

```
