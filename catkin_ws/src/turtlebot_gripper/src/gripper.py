import rospy
from std_msgs.msg import Int8
from std_msgs.msg import Bool


def grip(grip_msg):
    servo_pub = rospy.Publisher('servo', Int8, queue_size=1)
    servo_msg = Int8()
    if grip_msg:
        servo_msg.data = 45
        servo_pub.publish(servo_msg)
    else:
        servo_msg.data = 120
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
