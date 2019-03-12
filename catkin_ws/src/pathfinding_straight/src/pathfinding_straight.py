#!/usr/bin/env python

#############################################################
# Author: Laurens Van de Walle
# pathfinding_straight.py
#############################################################

#############################################################
# imports
#############################################################
import rospy
from pathfinding_straight.msg import Motor_Feedback
from pathfinding_straight.msg import Poic
from turtlebot_movement.msg import Movement


def pathfinding_straight():
    """
    Function that loops as long as node is running.
    :return:
    """
    listeners()
    pub = talker()




def update(message):
    """

    :param message:
    :return:
    """
    if message.type == "Motor_Feedback":
        pass

    if message.type == "Poic":
        pass


def listeners():
    """
    Sets up subscribers for this node.
    :return:
    """
    # setup node
    rospy.init_node('pathfinding_straight', anonymous=False)

    # subscribe to necessary topics
    print("Subcribing ")
    rospy.Subscriber("motor_feedback", Motor_Feedback, update)
    rospy.Subscriber("poic", Poic, update)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def talker():
    """

    :return:
    """
    # create publishers
    pub = rospy.Publisher('motor_instructions', Movement, queue_size = 10)
    return pub


if __name__ == '__main__':
    """
    Main function for the pathfinding node(Straight).
    """
    try:
        pathfinding_straight()
    except rospy.ROSInterruptException:
        print("Something went wrong")
        pass
