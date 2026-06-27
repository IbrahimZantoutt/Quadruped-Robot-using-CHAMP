# Nav2 navigation servers on top of the live SLAM map (no map_server/AMCL).
# cmd_vel: controller -> /cmd_vel_nav -> velocity_smoother -> /cmd_vel (CHAMP).
# Params: config/autonomy/navigation.yaml. Usually started by gazebo_rviz nav2:=true.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    default_params_file = os.path.join(
        get_package_share_directory("quadbot_config"),
        "config", "autonomy", "navigation.yaml",
    )

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time", default_value="true",
        description="Use simulation (Gazebo) clock",
    )
    declare_params_file = DeclareLaunchArgument(
        "params_file", default_value=default_params_file,
        description="Nav2 params file",
    )

    nav2_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("nav2_bringup"), "launch", "navigation_launch.py"]
            )
        ),
        launch_arguments={
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "params_file": LaunchConfiguration("params_file"),
        }.items(),
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_params_file,
        nav2_ld,
    ])
