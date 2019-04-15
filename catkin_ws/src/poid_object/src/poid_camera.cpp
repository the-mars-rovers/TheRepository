//OpenCV includes
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

//Ros includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "poid_object/Camera.h"

#include <sstream>

#define BRON 1

void returnPicture(void) {
    Mat image;
    cv::VideoCapture vcap;

    if(!vcap.open("/dev/video0")) {
        cout << "Kon videostream niet openen!" << endl;
        return;
    }
    cout << "Videostream gevonden!" << endl;

    if(!vcap.read(image)) {
        cout << "Kon frame niet inlezen" << endl;
        return;
    }

    imshow("Display", image);
    waitKey(0); 
    //imwrite("test.jpg", image);
}

void getCallback(poid_object::Camera msg)
{
    ROS_INFO("I heard: [%d]", msg.id);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "poid_camera");

  ros::NodeHandle n;

  ROS_INFO("Node gestart en aan het luisteren...");

  returnPicture();

  ros::Subscriber sub = n.subscribe("get_picture", 1000, getCallback);

  ros::spin();

  return 0;
}