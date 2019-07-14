#!/usr/bin/env python
from __future__ import print_function # TODO is this needed

import sys
import rospy
import object_detection_lib
from detection.msg import detection_results
from std_msgs.msg import Empty
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class ObjectDetectionNode:
    def __init__(self):
        self.__bridge = CvBridge()
        # Publisher to publish update image
        #self.__image_pub = rospy.Publisher("test1", Image, queue_size=1)
        # Subscribe to the topic which will supply the image fom the camera
        self.__image_sub = rospy.Subscriber("/bebop/image_raw",Image, self.Imagecallback,queue_size=None,buff_size=2**24)

        # Flag to indicate that we have been requested to use the next image
        #self.__scan_next = False

        # Read the path for models/research/object_detection directory from the parameter server or use this default
        object_detection_path = rospy.get_param('/object_detection/path', '/home/lee_ming_wei/models/research/object_detection')

        # Read the confidence level, any object with a level below this will not be used
        confidence_level = rospy.get_param('/object_detection/confidence_level', 0.70)

        # Create the object_detection_lib class instance
        self.__odc = object_detection_lib.ObjectDetection(object_detection_path, confidence_level)


    # Callback for new image received
    def Imagecallback(self, data):
        image=self.convert_image(data)

        # The supplied image will be modified if known objects are detected
        self.__odc.scan_for_objects(image)

        cv2.imshow('image',image)
        cv2.waitKey(1)
			
             #publish the image, it may have been modified
            #try:
              #self.__image_pub.publish(self.__bridge.cv2_to_imgmsg(image, "bgr8"))
           # except CvBridgeError as e:
             #print(e)

    # Convert the ROS image to an OpenCV image
    def convert_image(self,ros_image):
        try:
            image = self.__bridge.imgmsg_to_cv2(ros_image, "bgr8")
            return image
        except CvBridgeError as e:
            print(e)

def main(args):
    odn = ObjectDetectionNode()
    rospy.init_node('test1', anonymous=False)
    rospy.loginfo("object detection node started")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
