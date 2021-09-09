#!/bin/python3

from numpy.lib.npyio import save
from abb_irb120_reacher.task_env.irb120_reacher import abb_irb120_moveit
import gym
import rospy
import rospkg
import sys
from gym_gazebo_sb3.common import ros_gazebo
from gym_gazebo_sb3.common.ros_node import ROS_Kill_All_processes
from gym_gazebo_sb3.wrappers.NormalizeActionWrapper import NormalizeActionWrapper
from gym_gazebo_sb3.wrappers.TimeLimitWrapper import TimeLimitWrapper
from gym_gazebo_sb3.wrappers.NormalizeObservWrapper import NormalizeObservWrapper

# Models
from gym_gazebo_sb3.models.ddpg import DDPG
from gym_gazebo_sb3.models.td3 import TD3
from gym_gazebo_sb3.models.sac import SAC
from gym_gazebo_sb3.models.ppo import PPO
from gym_gazebo_sb3.models.dqn import DQN

if __name__ == '__main__':

    # Launch Gazebo 
    ros_gazebo.Launch_Gazebo(paused=True, gui=False)

    # Start node
    rospy.logwarn("Start")
    rospy.init_node('train_irb120_reacher')

    # Launch the task environment
    env = gym.make('ABBIRB120ReacherEnv-v0')

    #--- Normalize action space
    env = NormalizeActionWrapper(env)

    #--- Normalize observation space
    env = NormalizeObservWrapper(env)

    #--- Set max steps
    env = TimeLimitWrapper(env, max_steps=100)
    env.reset()

    #--- Set the save and log path
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path("abb_irb120_reacher")

    #-- DDPG
    save_path = pkg_path + "/models/static_reacher/ddpg/"
    log_path = pkg_path + "/logs/static_reacher/ddpg/"
    model = DDPG(env, save_path, log_path, config_file_pkg="abb_irb120_reacher", config_filename="ddpg.yaml")
    
    #-- TD3
    # save_path = pkg_path + "/models/static_reacher/td3/"
    # log_path = pkg_path + "/logs/static_reacher/td3/"
    # model = TD3(env, save_path, log_path, config_file_pkg="abb_irb120_reacher", config_filename="td3.yaml")

    #-- SAC
    # save_path = pkg_path + "/models/static_reacher/sac/"
    # log_path = pkg_path + "/logs/static_reacher/sac/"
    # model = SAC(env, save_path, log_path, config_file_pkg="abb_irb120_reacher", config_filename="sac.yaml")

    #--- PPO
    # save_path = pkg_path + "/models/static_reacher/ppo/"
    # log_path = pkg_path + "/logs/static_reacher/ppo/"
    # model = PPO(env, save_path, log_path, config_file_pkg="abb_irb120_reacher", config_filename="ppo.yaml")


    model.train()
    model.save_model()
    model.close_env()

    sys.exit()