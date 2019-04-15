#include "ros/ros.h"
#include "std_msgs/String.h"

#include "poid_object/Poic.h"

#include <sstream>

bool ontvangen = false;

void detectCallback(const poid_object::Poic msg)
{
  ROS_INFO("Oke, binnengekregen...");

  if(msg.ok == true) {
    ontvangen = true;
  }
}

/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappadd_executable(poid_test src/poid_test.cpp)
target_link_libraries(poid_test ${catkin_LIBRARIES})
add_dependencies(poid_test poid_test_generate_messages_cpp)ings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "poid_test");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;

  /**
   * The advertise() function is how you tell ROS that you want to
   * publish on a given topic name. This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing. After this advertise() call is made, the master
   * node will notify anyone who is trying to subscribe to this topic name,
   * and they will in turn negotiate a peer-to-peer connection with this
   * node.  advertise() returns a Publisher object which allows you to
   * publish messages on that topic through a call to publish().  Once
   * all copies of the returned Publisher object are destroyed, the topic
   * will be automatically unadvertised.
   *
   * The second parameter to advertise() is the size of the message queue
   * used for publishing messages.  If messages are published more quickly
   * than we can send them, the number here specifies how many messages to 
   * buffer up before throwing some away.
   */
  ros::Publisher chatter_pub = n.advertise<poid_object::Poic>("detect", 1000);
  ros::Subscriber sub = n.subscribe("detect_ok", 1000, detectCallback);

  ros::Rate loop_rate(10);
  int count = 0;
  int teller = 0;

  while (ros::ok() & (ontvangen == false))
  {
    if(teller == 10) {
      /**
       * This is a message object. You stuff it with data, and then publish it.
       */
      poid_object::Poic msg;

      msg.seq_num = count;

      ROS_INFO("%d", msg.seq_num);
      count++;

      /**
       * The publish() function is how you send messages. The parameter
       * is the message object. The type of this object must agree with the type
       * given as a template parameter to the advertise<>() call, as was done
       * in the constructor above.
       */
      chatter_pub.publish(msg);
      teller=0;
    }
    teller++;

    ros::spinOnce();

    loop_rate.sleep();
  }


  return 0;
}