from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, RegisterEventHandler
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    # 定義參數
    size_arg = DeclareLaunchArgument('size', default_value='3x6', description='校準板大小')
    square_arg = DeclareLaunchArgument('square', default_value='0.026', description='方格邊長 (單位：米)')
    image_topic_arg = DeclareLaunchArgument('image_topic', default_value='/camera/color/image_raw', description='圖像話題名稱')
    camera_name_arg = DeclareLaunchArgument('camera_name', default_value='/my_camera', description='相機名稱')

    # 打印當前參數的設置
    log_size = LogInfo(msg=['Size: ', LaunchConfiguration('size')])
    log_square = LogInfo(msg=['Square: ', LaunchConfiguration('square')])
    log_image_topic = LogInfo(msg=['Image Topic: ', LaunchConfiguration('image_topic')])
    log_camera_name = LogInfo(msg=['Camera Name: ', LaunchConfiguration('camera_name')])

    # 定義 camera_calibration 節點
    camera_calibration_node = Node(
        package='camera_calibration',
        executable='cameracalibrator',
        name='cameracalibrator',
        output='screen',
        arguments=[
            '--size', LaunchConfiguration('size'),
            '--square', LaunchConfiguration('square'),
            '--ros-args', '-r', ['image:=', LaunchConfiguration('image_topic')],
            '-p', ['camera:=', LaunchConfiguration('camera_name')]
        ]
    )

    # 註冊事件監聽，確保節點啟動成功
    on_start_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=camera_calibration_node,
            on_start=[
                LogInfo(msg="Camera calibration node has started successfully.")
            ]
        )
    )

    return LaunchDescription([
        size_arg,
        square_arg,
        image_topic_arg,
        camera_name_arg,
        log_size,
        log_square,
        log_image_topic,
        log_camera_name,
        camera_calibration_node,
        on_start_handler
    ])
