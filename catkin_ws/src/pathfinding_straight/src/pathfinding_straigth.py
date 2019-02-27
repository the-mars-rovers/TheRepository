#!/usr/bin/env python

#############################################################
# Author: Laurens Van de Walle
# pathfinding_straight.py
# For now, this file is just an example for how a node works
#############################################################

#############################################################
# imports
#############################################################
import rospy
from std_msgs.msg import String


def pathfinding_straight():
    """
    Function that loops as long as node is running.
    :return:
    """
    pub = rospy.Publisher('motor_instructions', String, queue_size=10)
    rospy.init_node('pathfinding_straight', anonymous=False)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()


if __name__ == '__main__':
    """
    
    """
    try:
        pathfinding_straight()
    except rospy.ROSInterruptException:
        pass
