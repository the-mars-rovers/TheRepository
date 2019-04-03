//OpenCV includes
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

//Ros includes
#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>

using namespace std;
using namespace cv;

void detectCallback(const std_msgs::String::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str());
}

float detect_ball(Mat image) {
    Mat splitImage[3];
    Mat outputR, outputG, outputB, output;
    vector<vector<Point>> contours;
    int maximum;

    split(image, splitImage);

    threshold(splitImage[2], outputR, 130, 255, CV_THRESH_BINARY);

    threshold(splitImage[0], outputB, 100, 255, CV_THRESH_BINARY);

    threshold(splitImage[1], outputG, 100, 255, CV_THRESH_BINARY);

    //G en B inverteren
    bitwise_not(outputB, outputB);
    bitwise_not(outputG, outputG);

    bitwise_and(outputR, outputB, output);
    bitwise_and(output, outputG, output);

    findContours(output, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    //Grootste bepalen
    maximum = 0;
    for(uint k=1;k<contours.size();k++) {
        if(contourArea(contours[k]) > contourArea(contours[maximum])) {
            maximum = k;
        }
    }

    //De grootste blob tekenen op de afbeelding
    drawContours(image, contours, maximum, Scalar(0,255,0), 3);

    //Canter van de blob berekenen
    Moments m = moments(contours[maximum],true);
    Point p(m.m10/m.m00, m.m01/m.m00);

    cout << "Center: " << p << " w:" << image.cols << endl;

    circle(image, p, 3, Scalar(0, 255, 0), 3);

    return 0.0;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "poid_detect");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("detect", 1000, detectCallback);

  ros::spin();

  return 0;
}