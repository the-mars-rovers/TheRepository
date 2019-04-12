#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Bool


def grip(grip_msg):
    """
    :type grip_msg: Bool
    """
    servo_pub = rospy.Publisher('/servo', UInt16, queue_size=1)
    servo_msg = UInt16()
    if grip_msg.data:
        servo_msg.data = 45
    else:
        servo_msg.data = 120

    print(servo_msg)
    servo_pub.publish(servo_msg)


def listener():
    rospy.init_node('turtlebot_gripper')
    rospy.Subscriber('gripper_movement', Bool, grip)
    print("Listener on gripper_movement started.")
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        # Listen to topic motor_instructions
        listener()
    except rospy.ROSInterruptException:
        pass
