#!/usr/bin/env python

#############################################################
# Author: Laurens Van de Walle
# pathfinding_code.py
#############################################################

# imports
import rospy
from turtlebot_movement.msg import Movement
from pathfinding.msg import Poic
from pathfinding.msg import Detect
from std_msgs.msg import Bool


# publish to movement and detect topics
pub_mov = rospy.Publisher('motor_instructions', Movement, queue_size=10)
pub_det = rospy.Publisher('detection', Detect, queue_size=10)
pub_grip = rospy.Publisher('gripper_movement', Bool, queue_size=10)

waiting_for_feedback = False
sequence_number = 0
gripper_activated = False
poi_found = False
redo = False


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
    if isinstance(message, Bool):
        if message.data:
            global gripper_activated
            global waiting_for_feedback
            waiting_for_feedback = False
            global sequence_number
            sequence_number += 1
            if sequence_number < 3:
                full_rotation()
            # elif gripper_activated:
            #     gripper_activated = False
            #     grip_message = Bool()
            #     grip_message.data = False
            #     mov_message = Movement()
            #     mov_message.speed = 1
            #     mov_message.dist = -0.1
            #     mov_message.forward = True
            #     mov_message.angle_speed = 30
            #     mov_message.angle = 0
            #     pub_grip.publish(grip_message)
            #     pub_mov.publish(mov_message)
            elif gripper_activated:
                gripper_activated = False
                new_message = Bool()
                new_message.data = False
                pub_grip.publish(new_message)
                # onto the next object
                global sequence_number
                sequence_number = 0
                full_rotation()
            else:
                new_message = Detect()
                new_message.seq_num = sequence_number
                pub_det.publish(new_message)

    # if we  get new information from the camera
    if isinstance(message, Poic):
        # if we are still waiting for feedback from the actuators don't do anything
        global poi_found
        if message.distance_to_center != 200 and message.seq_num < 4:
            poi_found = True

            new_message = Bool()
            new_message.data = False
            pub_grip.publish(new_message)

            new_message = Movement()
            new_message.angle = 90*message.seq_num + message.distance_to_center
            new_message.angle_speed = 30
            new_message.dist = 0
            new_message.speed = 0
            new_message.forward = True
            pub_mov.publish(new_message)
        elif message.distance_to_center == 300:
            new_message = Bool()
            new_message.data = True
            pub_grip.publish(new_message)

            # 360 degree spin with object
            new_message = Movement()
            new_message.angle = 360
            new_message.angle_speed = 30
            new_message.dist = 0
            new_message.speed = 0
            new_message.forward = True
            pub_mov.publish(new_message)

            global gripper_activated
            gripper_activated = True
        else:
            new_message = Bool()
            new_message.data = False
            pub_grip.publish(new_message)
            process_message(message)

        "If no pois are found in a full rotation"
        if message.distance_to_center == 200 and not poi_found and message.seq_num == 3:
            global sequence_number
            sequence_number = 0
            new_message = Movement()
            new_message.angle = 0
            new_message.angle_speed = 30
            new_message.dist = 0.5
            new_message.speed = 0
            new_message.forward = True
            pub_mov.publish(new_message)

            full_rotation()


def listener():
    """
    Sets up subscribers for this node.
    """
    # setup node
    rospy.init_node('pathfinding_straight', anonymous=False)

    # subscribe to necessary topics
    print("Subscribing ")
    rospy.Subscriber("motor_feedback", Bool, update)
    rospy.Subscriber("poic", Poic, update)

    # Doing the first 4 rotates for 360 view
    full_rotation()

    rospy.spin()


def full_rotation():
    """
    Does a full rotation of the bot, every 90 degrees a picture will be taken.
    """
    rate = rospy.Rate(3)
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
    global sequence_number
    det_message.seq_num = sequence_number
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
