import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.wait_for_controller_connection import WaitForControllerConnection
from launch_ros.actions import Node
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    package_dir = get_package_share_directory('webots_ros2_ld90')
    
    # Start a Webots simulation instance
    world = LaunchConfiguration('world')
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    
    webots = WebotsLauncher(
        world=PathJoinSubstitution([package_dir, 'worlds', world]),
        ros2_supervisor=True
    )

    # Create the robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': '<robot name=""><link name=""/></robot>'
        }],
    )

    # Wheel drop left and right
    tf_wheel_drop_left = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='wheel_drop_left_to_base_link',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'wheel_drop_left'],
    )

    tf_wheel_drop_right = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='wheel_drop_right_to_base_link',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'wheel_drop_right'],
    )

    # Range finder 
    tf_kinect_range = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='kinect_range_to_base_link',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'kinect_range'],
    )


    # ROS control spawners
    ros2_control_params = os.path.join(package_dir, 'resource', 'ros2control.yaml')
    controller_manager_timeout = ['--controller-manager-timeout', '50']
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['joint_state_broadcaster'] + controller_manager_timeout,
    )

    diffdrive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        output='screen',
        arguments=['diffdrive_controller'] + controller_manager_timeout,
    )
    
    ros_control_spawners = [joint_state_broadcaster_spawner, diffdrive_controller_spawner]
    
    mappings = [
        ('/diffdrive_controller/cmd_vel_unstamped', '/cmd_vel'), 
        ('/diffdrive_controller/odom', '/odom'),
        ('/LD90/main_lidar', '/scan_main'),
        ('/LD90/kinect_range', '/scan_sub'),
    ]      
    
    # Create a ROS node interacting with the simulated robot
    robot_description_path = os.path.join(package_dir, 'resource', 'LD90.urdf')
    robot_driver = WebotsController(
        robot_name='LD90',
        parameters=[
            {
                'robot_description': robot_description_path,
                'use_sim_time': use_sim_time,
                'set_robot_state_publisher': True
            },
            ros2_control_params
        ],
        remappings=mappings
    )

    # Wait for the simulation to be ready to start navigation nodes
    waiting_nodes = WaitForControllerConnection(
        target_driver=robot_driver,
        nodes_to_start=ros_control_spawners
    )   

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='my_ld90.wbt',
            description='Choose one of the world files from /webots_ros2_ld90/worlds directory'
        ),
        webots,
        robot_state_publisher,
        webots._supervisor,
        tf_wheel_drop_left,
        tf_wheel_drop_right,
        tf_kinect_range,
        robot_driver,
        waiting_nodes,
        # The following action will kill all nodes once the Webots simulation has exited
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
