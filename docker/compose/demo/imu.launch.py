from launch import LaunchDescription
from launch.actions import TimerAction, LogInfo
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 获取当前目录路径
    current_dir = os.path.dirname(__file__)
    # 配置 EKF 所需的参数文件路径
    ekf_config_file = os.path.join(current_dir, 'ekf_config.yaml')

    # 启动 wit_ros2_imu 节点
    wit_ros2_imu_node = Node(
        package='wit_ros2_imu',
        executable='wit_ros2_imu',
        name='wit_ros2_imu',
        output='screen'
    )

    # 启动 EKF 节点
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_file],
        remappings=[('odometry', 'odometry'),
                ('imu/data', 'imu/data')]
    )

    # 打印消息：wit_ros2_imu 节点启动成功
    wit_ros2_imu_success_message = LogInfo(
        msg="wit_ros2_imu 啟動成功!"
    )

    # 延时启动 EKF 节点，并在启动成功后打印消息
    ekf_startup_message = TimerAction(
        period=5.0,
        actions=[
            ekf_node,
            LogInfo(msg="ekf_node 啟動成功!")
        ]
    )

    return LaunchDescription([
        wit_ros2_imu_node,
        wit_ros2_imu_success_message,
        ekf_startup_message,
    ])
