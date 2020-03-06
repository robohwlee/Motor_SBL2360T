#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import time
import numpy as np
from geometry_msgs.msg import (Point, Quaternion, Pose, PoseArray, Twist,
                               Transform, TransformStamped,
                               PoseWithCovariance, PoseWithCovarianceStamped)


class cmdvelPublisher:

    def __init__(self):
        
        # ROS parameters

        # Initialize ros node
        rospy.init_node('cmd_vel_publisher', anonymous = True)
        # Subscriber
        
        # Publisher
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)


    def spin(self):
        rospy.spin()

       
    def averagedPose(self, _pose):
        '''
        average stacked pose and publish
        '''


        stamp = rospy.Time.now()
        init_pose_msg = InitPose()
        init_pose_msg.header.stamp = stamp
        init_pose_msg.header.frame_id = self.stargazer_frame_id
        init_pose_msg.position.x = np.mean(_pose[0, 10:40])
        init_pose_msg.position.y = np.mean(_pose[1, 10:40])
        init_pose_msg.position.z = 0
        init_pose_msg.angle = np.mean(_pose[2, 10:40])
        
        
        self.init_pose_pub.publish(init_pose_msg)



if __name__ == '__main__':

    try:
        node = cmdvelPublisher()
        node.spin()
    except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")
