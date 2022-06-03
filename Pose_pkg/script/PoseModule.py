#!/usr/bin/env python
import cv2
import mediapipe as mp
import time

class poseDetector():
    def __init__(self,
                 static_image_mode=False,   # 是静态图片(True)还是视频(False)
                 model_complexity=2,        # 选择模型，0性能差，2最好但是慢
                 smooth_landmarks=True,     # 是否平滑关键点
                 enable_segmentation=False, # 是否人体抠图
                 smooth_segmentation=True,  # 是否平滑抠图
                 min_detection_confidence=0.5,  # 置信度阀值
                 min_tracking_confidence=0.5):  # 追踪阀值
        self.mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = min_detection_confidence
        self.trackCon = min_tracking_confidence
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self. smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, draw = True):
        lmlist = []
        lm3Dlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):  # Get keypoint from res
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # Get x, y in pixel
                lmlist.append([id, cx, cy])
                lm3Dlist.append([id, lm.x, lm.y, lm.z])
                if draw:
                        cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
        return lmlist, lm3Dlist

def main():
    cap = cv2.VideoCapture(0)
    ptime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmlist = detector.getPosition(img)
        #print(lmlist)

        ###***** FPS *****###
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        ###***** FPS *****###
        cv2.imshow("ori", img)

        cv2.waitKey(1)

if __name__ == "__main__":
    main()