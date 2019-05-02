//OpenCV includes
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

//Ros includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "poid_object/Poic.h"
#include "poid_object/Detect.h"
#include <sstream>

using namespace std;
using namespace cv;

ros::Publisher chatter_pub;

float detect_ball() {
    //Foto nemen
    Mat image;
    cv::VideoCapture vcap;

    if(!vcap.open("/dev/video0")) {
        cout << "Kon videostream niet openen!" << endl;
        return 200.0;
    }
    cout << "Videostream gevonden!" << endl;

    if(!vcap.read(image)) {
        cout << "Kon frame niet inlezen" << endl;
        return 200.0;
    }

    //imshow("Display", image);



    //Bal detecteren
    Mat splitImage[3];
    Mat outputR, outputG, outputB, output;
    vector<vector<Point>> contours;
    int maximum;

    split(image, splitImage);

    threshold(splitImage[2], outputR, 130, 255, CV_THRESH_BINARY);

    threshold(splitImage[0], outputB, 100, 255, CV_THRESH_BINARY);

    threshold(splitImage[1], outputG, 100, 255, CV_THRESH_BINARY);

    cout << "Bitwise stuff" << endl;

    //G en B inverteren
    bitwise_not(outputB, outputB);
    bitwise_not(outputG, outputG);

    bitwise_and(outputR, outputB, output);
    bitwise_and(output, outputG, output);

    cout << "findContours" << endl;

    findContours(output, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    //Grootste bepalen
    maximum = 0;
    for(uint k=0;k<contours.size();k++) {
        if(contourArea(contours[k]) > contourArea(contours[maximum])) {
            maximum = k;
        }
    }

    //De grootste blob tekenen op de afbeelding
    //drawContours(image, contours, maximum, Scalar(0,255,0), 3);

    cout << "moments" << endl;
    //Center van de blob berekenen
    Moments m = moments(contours[maximum],true);
    Point p(m.m10/m.m00, m.m01/m.m00);

    cout << "Center: " << p << " w:" << image.cols << endl;

    //Het punt klaar maken voor interpretatie
    float punt = (float)p.y - (float)image.cols/2;
    punt = punt/((float)image.cols/2) * 90;

    cout << "Punt: " << punt << endl;

    //Is de blob groot genoeg? Of zijn we er al?
    float grote = contours[maximum].size();

    cout << "Grote van de blob:" << grote << endl;

    if(grote < 20) {
        cout << "Blob is te klein" << endl;
        return 200.0;
    }

    if(grote > 500) {
        cout << "We zijn er!" << endl;
        return 300.0;
    }

    //circle(image, p, 3, Scalar(0, 255, 0), 3);

    return punt;
}

void detectCallback(const poid_object::Detect msg)
{
  cout << "Start detectie" << endl;
  ROS_INFO("Sequentie nummer: [%d]", msg.seq_num);

  //Zender verwittigen dat de vraag ontvangen is
  /*
  poid_object::Poic msg_ok;
  msg_ok.ok = true;
  chatter_pub.publish(msg_ok);
  */

  //Detectie starten
  int punt = (int)detect_ball();

  //De puntgegevens verzenden
  poid_object::Poic msg_point;
  msg_point.seq_num = msg.seq_num;
  msg_point.distance_to_center = punt;
  chatter_pub.publish(msg_point);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "poid_detect");

  cout << "Running..." << endl;

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("detect", 1000, detectCallback);

  chatter_pub = n.advertise<poid_object::Poic>("detect_ok", 1000);

  ros::spin();

  return 0;
}