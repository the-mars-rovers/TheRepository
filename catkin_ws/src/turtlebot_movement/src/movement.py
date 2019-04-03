#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlebot_movement.msg import Movement     # custom message
from math import pi
from std_msgs.msg import Bool


def translate(speed, dist, forward, vel_msg, velocity_publisher):
    # Checking if the movement is forward or backwards
    if forward:
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    # Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    # Setting the current time for distance calculus
    t0 = float(rospy.Time.now().to_sec())
    current_distance = 0

    try:
        # Loop to move the turtle in an specified distance
        while current_distance < dist:
            # Publish the velocity
            velocity_publisher.publish(vel_msg)
            # rospy.sleep(0.5)
            # Takes actual time to velocity calculus
            t1 = float(rospy.Time.now().to_sec())
            # Calculates distancePoseStamped
            current_distance = speed * (t1 - t0)
    finally:
        # After the loop, stops the robot
        vel_msg.linear.x = 0
        # Force the robot to stop
        velocity_publisher.publish(vel_msg)


def rotate(speed, angle, vel_msg, velocity_publisher):
    if angle > 0:
        clockwise = True
    else:
        clockwise = False

    # Converting from angles to radians
    angular_speed = speed * 2 * pi / 360
    relative_angle = angle * 2 * pi / 360

    # We wont use linear components
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
    if clockwise:
        print("Turning clockwise")
        vel_msg.angular.z = -abs(angular_speed)
    else:
        print("Turning counter-clockwise")
        vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while current_angle < abs(relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1 - t0)

    # Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)


def move(move_msg):
    print("Getting ready to move")
    print(move_msg)
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    fb_pub = rospy.Publisher('motor_feedback', Bool, queue_size=10)
    vel_msg = Twist()
    fb_msg = Bool()

    fb_msg.data = False
    fb_pub.publish(fb_msg)

    sp = move_msg.speed
    di = move_msg.dist
    an_sp = move_msg.angle_speed
    an = move_msg.angle
    fo = move_msg.forward

    if an != 0:
        rotate(an_sp, an/1.85, vel_msg, vel_pub)

    translate(sp, di*(10.0/3.86), fo, vel_msg, vel_pub)
    fb_msg.data = True
    fb_pub.publish(fb_msg)
    print("Done moving")
    print("--------------------------")
    return 1


def listener():
    rospy.init_node('turtlebot_movement')
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    dummy_pub = rospy.Publisher('motor_instructions', Movement, queue_size=1) #this publisher is just for testing purposes and is only here to create the topic 'motor_instructions'
    rospy.Subscriber('motor_instructions', Movement, move)
    print("Listener on motor_instructions started.")
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        # Listen to topic motor_instructions
        listener()
    except rospy.ROSInterruptException:
        pass
