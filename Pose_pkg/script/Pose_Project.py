#!/usr/bin/env python
from tkinter import Image
import cv2
import time
import PoseModule as pm
import rospy
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError

class KeyPoints():
    def __init__(self):
        self.img_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback)
        self.keypoint = rospy.Publisher('KetPoint', Point, queue_size = 1)
        self.res_img = rospy.Publisher('Res_Img', Image, queue_size = 1)
        self.bridge = CvBridge
        
    def callback(self, img):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(img, 'bgr8')
        except CvBridgeError:
            print('CvBridgeError')
        
        detector = pm.poseDetector()
        img = detector.findPose(cv_image)
        lmlist, lm3Dlist = detector.getPosition(img, draw = False)
        x, y, z = lm3Dlist[0],lm3Dlist[1], lm3Dlist[2]
        kp = Pose(x,y,z)
        ###***** FPS *****###
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (50, 150), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 8)
        ###***** FPS *****###
        
        try:
            self.res_img.publish(self.bridge.cv2_to_compressed_imgmsg(img, 'bgr8'))
            self.keypoint.publish(kp)
        except CvBridgeError:
            print('ERROR')

if __name__ == '__main__':
    rospy.init_node('Get_KeyPoints')
    KeyPoints()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass