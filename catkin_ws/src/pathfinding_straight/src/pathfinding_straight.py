#!/usr/bin/env python

#############################################################
# Author: Laurens Van de Walle
# pathfinding_straight.py
#############################################################

# imports
import rospy
# from pathfinding_straight.msg import Motor_Feedback
# from pathfinding_straight.msg import Poic
from turtlebot_movement.msg import Movement
import time


def process_message():
    """
    Processes the message from poic
    :param message:
    :return:
    """
    pub = rospy.Publisher('motor_instructions', Movement, queue_size=1)
    rate = rospy.Rate(1)
    for i in range(1, 3):
        print(str(i))
        # create new message
        # test
        new_message = Movement()
        new_message.speed = 1
        new_message.dist = 0.01
        new_message.forward = True
        new_message.angle_speed = 30
        new_message.angle = 0

        pub.publish(new_message)

        rate.sleep()


def update(message):
    """
    Callback function for the listeners
    :param message:
    :return:
    """
    waiting_for_feedback = False
    message_in_queue = False

    # if the motor is giving feedback
    if message.type == "Motor_Feedback":
        if message.ready:
            waiting_for_feedback = False

    # if we  get new information from the camera
    if message.type == "Poic" or message_in_queue:
        # if we are still waiting for feedback from the actuators don't do anything
        if waiting_for_feedback:
            pass
        else:
            process_message(message)


def listener():
    """
    Sets up subscribers for this node.
    :return:
    """
    # setup node
    rospy.init_node('pathfinding_straight', anonymous=False)
    process_message()

    # subscribe to necessary topics
    print("Subscribing ")
    # rospy.Subscriber("motor_feedback", Motor_Feedback, update)
    # rospy.Subscriber("poic", Poic, update)

    # publish to movement topic
    # pub = rospy.Publisher('motor_instructions', Movement, queue_size=10)

    # Doing the first 4 rotates for 360 view
    # create the message
    # new_message = Movement()
    # new_message.speed = 1
    # new_message.dist = 0
    # new_message.forward = True
    # new_message.angle_speed = 30
    # new_message.angle = 90

    # rotate 4 times and take a picture

    # rospy.spin()


if __name__ == '__main__':
    """
    Main function for the pathfinding node(Straight).
    """
    try:
        listener()
    except rospy.ROSInterruptException:
        print("Something went wrong")
        pass
