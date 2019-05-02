#include <iostream>
#include <opencv2/opencv.hpp>
#include <string.h>

#define BRON 0

using namespace std;
using namespace cv;

int main(int argc, const char** argv) {
    Mat image;
    VideoCapture vcap;

    if(!vcap.open(BRON)) {
        cout << "Kon videostream niet openen!" << endl;
        return -1;
    }
    cout << "Videostream gevonden!" << endl;

    if(!vcap.read(image)) {
        cout << "Kon frame niet inlezen" << endl;
        return -1;
    }

    imwrite("test.jpg", image);

    imshow("Output", image);
    waitKey(0);

    return 0;
}

