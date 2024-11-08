from launch import LaunchDescription
from launch.actions import TimerAction, LogInfo
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    wit_ros2_imu_node = Node(
        package='wit_ros2_imu',
        executable='wit_ros2_imu',
        name='wit_ros2_imu',
        output='screen'
    )

    # 打印消息：wit_ros2_imu 节点启动成功
    wit_ros2_imu_success_message = LogInfo(
        msg="wit_ros2_imu 啟動成功!"
    )

    return LaunchDescription([
        wit_ros2_imu_node,
        wit_ros2_imu_success_message,
    ])
