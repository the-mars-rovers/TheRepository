#include <iostream>
#include <opencv2/opencv.hpp>
#include <string.h>

using namespace std;
using namespace cv;

int main(int argc, const char** argv) {
    Mat image;
    Mat splitImage[3];
    Mat outputR, outputG, outputB, output;
    vector<vector<Point>> contours;
    int maximum;

    //Helpboodschap configureren
    CommandLineParser parser(argc, argv,
    "{help | |Met dit programma dienen twee parameters meegegeven te worden}"
    "{img | |Het absolute pat van de afbeelding}");

    //Indien gevraagd helpboodschap afdrukken
    if(parser.has("help")) {
        parser.printMessage();
        return -1;
    }

    //Parameters inlezen
    string img(parser.get<string>("img"));

    //Juiste hoeveelheid gegevens ingegeven?
    if(img == "") {
        cerr << "Parameters niet correct opgegeven!"  << endl;
        parser.printMessage();
        return -1;
    }

    //Afbeeldingen inlezen + nakijken of dit gelukt is
    cout << "File " << img << " inlezen..." << endl;
    image = imread(img, CV_LOAD_IMAGE_COLOR);
    if(!image.data)
    {
        cout <<  "Kon img1 niet openen" << endl ;
        return -1;
    }

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

    imshow("Output", image);
    waitKey(0);

    return 0;
}
