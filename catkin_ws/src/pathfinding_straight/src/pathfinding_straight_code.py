#!/usr/bin/env python

#############################################################
# Author: Laurens Van de Walle
# pathfinding_straight_code.py
#############################################################

# imports
import rospy
from turtlebot_movement.msg import Movement
from pathfinding_straight.msg import Motor_Feedback
from pathfinding_straight.msg import Poic
from pathfinding_straight.msg import Detect


# publish to movement and detect topics
pub_mov = rospy.Publisher('motor_instructions', Movement, queue_size=10)
pub_det = rospy.Publisher('detection', Detect, queue_size=10)

waiting_for_feedback = False
sequence_number = 0


def process_message(message):
    """
    Processes the message from POI location.
    :param message: message received by listener
    """
    # create new message
    # test
    new_message = Movement()
    new_message.speed = 1
    new_message.dist = 0.1
    new_message.forward = True
    new_message.angle_speed = 30
    new_message.angle = message.distance_to_center

    pub_mov.publish(new_message)
    global waiting_for_feedback
    waiting_for_feedback = True


def update(message):
    """
    Callback function for the listeners.
    :param message: message received by listener
    """

    # if the motor is giving feedback
    if isinstance(message, Motor_Feedback):
        if message.ready:
            global waiting_for_feedback
            waiting_for_feedback = False
            global sequence_number
            sequence_number += 1
            if sequence_number < 4:
                full_rotation(sequence_number)

    # if we  get new information from the camera
    if isinstance(message, Poic):
        # if we are still waiting for feedback from the actuators don't do anything
        if message.distance_to_center != 200 and message.seq_num < 4:
            new_message = Movement()
            new_message.angle = 90*message.seq_num + message.distance_to_center
            new_message.angle_speed = 30
            new_message.dist = 0
            new_message.speed = 0
            new_message.forward = True
            pub_mov.publish(new_message)
        else:
            process_message(message)


def listener():
    """
    Sets up subscribers for this node.
    """
    # setup node
    rospy.init_node('pathfinding_straight', anonymous=False)

    # subscribe to necessary topics
    print("Subscribing ")
    rospy.Subscriber("motor_feedback", Motor_Feedback, update)
    rospy.Subscriber("poic", Poic, update)

    # Doing the first 4 rotates for 360 view
    full_rotation(0)

    rospy.spin()


def full_rotation(number):
    """
    Does a full rotation of the bot, every 90 degrees a picture will be taken.
    """
    rate = rospy.Rate(4)
    # create the message for rotation
    mov_message = Movement()
    mov_message.speed = 1
    mov_message.dist = 0
    mov_message.forward = True
    mov_message.angle_speed = 30
    mov_message.angle = 90

    # create message for detection
    det_message = Detect()

    # rotate 4 times and take a picture
    det_message.seq_num = number
    pub_mov.publish(mov_message)
    rate.sleep()
    pub_det.publish(det_message)


if __name__ == '__main__':
    """
    Main function for the pathfinding node(Straight).
    """
    try:
        listener()
    except rospy.ROSInterruptException:
        print("Something went wrong")
        pass
