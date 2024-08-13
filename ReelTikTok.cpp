#include <opencv2/core/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <utility>
#include <sstream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[]) {

    string source = "./data/backgroundvids/1.mp4";
    string outputVideoPath = "./data/cache/video.avi";
    int codec = VideoWriter::fourcc('X', 'V', 'I', 'D');

    VideoCapture inputVideo;

    // Open the video file
    if (!inputVideo.open(source)) {
        cout << "Could not open the video file." << endl;
        return -2;
    }

    // Check if the video file is opened successfully
    if (!inputVideo.isOpened()) {
        cout << "Failed to open the video file." << endl;
        return -3;
    }

    vector<pair<string, double>> imageTimestamps;

    // Open the text file
    ifstream file("./data/timestamps.txt");
    if (!file) {
        cout << "Failed to open the timestamps file." << endl;
        return -4;
    }

    // Read the data from the file
    string line;
    double lastIntegerTimestamp = 0.0;
    while (getline(file, line)) {
        istringstream iss(line);
        string imagePath, audioPath;
        double timestamp;
        if (getline(iss, imagePath, '|') && getline(iss, audioPath, '|') && iss >> timestamp) {
            imageTimestamps.push_back(make_pair(imagePath, timestamp));
            if (static_cast<int>(timestamp) > lastIntegerTimestamp) {
                lastIntegerTimestamp = static_cast<int>(timestamp);
            }
        }
    }
    file.close();

    double fps = inputVideo.get(CAP_PROP_FPS);

    VideoWriter outputVideo;

    Mat frame;
    inputVideo >> frame;
    if (frame.empty()) {
        cout << "Failed to read a frame from the video." << endl;
        return -5;
    }

    Size frameSize = Size(frame.cols, frame.rows);

    outputVideo.open(outputVideoPath, codec, fps, frameSize);
    if (!outputVideo.isOpened()) {
        cout << "Failed to open the output video file." << endl;
        return -6;
    }

    // Define initial image and scaling factor
    Mat image;
    double scale = 1.0;

    // Define destination ROI rectangle
    Rect dstRC;

    for (;;) {
        double currentTimestamp = inputVideo.get(CAP_PROP_POS_MSEC) / 1000.0;

        // Check if the current timestamp matches any of the image timestamps
        for (const auto& pair : imageTimestamps) {
            if (abs(pair.second - currentTimestamp) < 0.01) {
                image = imread(pair.first, IMREAD_COLOR);
                if (!image.empty()) {
                    // Calculate the scaling factor
                    scale = min(static_cast<double>(frame.cols) / image.cols, static_cast<double>(frame.rows) / image.rows);

                    // Resize the image to fit the frame
                    resize(image, image, Size(), scale, scale, INTER_LINEAR);

                    // Calculate the destination ROI
                    int cx = (frame.cols - image.cols) / 2;
                    int cy = (frame.rows - image.rows) / 2;
                    dstRC = Rect(cx, cy, image.cols, image.rows);
                }
            }
        }

        if (!image.empty()) {
            Mat frameCopy = frame.clone();
            Mat dstROI = frameCopy(dstRC);
            // Copy the pixels from src to dst.
            image.copyTo(dstROI);
            imshow("frame", frameCopy);
            outputVideo.write(frameCopy);  // Write the modified frame to the output video file
        }
        else {
            imshow("frame", frame);
            outputVideo.write(frame);  // Write the frame to the output video file
        }

        char key = (char)waitKey(30);
        // Exit this loop on escape:
        if (key == 27 || currentTimestamp >= lastIntegerTimestamp)
            break;

        inputVideo >> frame;
        if (frame.empty())
            break;
    }

    // Release the VideoWriter and VideoCapture objects
    outputVideo.release();
    inputVideo.release();

    return 0;
}