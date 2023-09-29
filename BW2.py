import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import random

class DepthImageProcessor:
    def __init__(self):
        rospy.init_node('depth_image_processor')
        self.bridge = CvBridge()
        self.depth_image = None
        self.color_image = None
        self.mleft = []
        self.mright = []

    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.mleft = [x, y]
        elif event == cv2.EVENT_RBUTTONDBLCLK:
            self.mright = [x, y]

    def depth_callback(self, msg):
        self.depth_image = self.bridge.imgmsg_to_cv2(msg)

    def image_callback(self, msg):
        self.color_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def process_depth_image(self):
        cv2.namedWindow("Depth Image")
        cv2.setMouseCallback("Depth Image", self.draw)

        while not rospy.is_shutdown():
            if self.depth_image is not None and self.color_image is not None:
                depth_image_copy = self.depth_image.copy()
                color_image_copy = self.color_image.copy()

                ret, thresholded = cv2.threshold(depth_image_copy, 2000, 255, cv2.THRESH_BINARY)
                connectivity = 4
                output = cv2.connectedComponentsWithStats(thresholded, connectivity, cv2.CV_32S)

                num_labels = output[0]
                labels = output[1]
                stats = output[2]

                max_label = 1
                max_area = stats[1, cv2.CC_STAT_AREA]

                for label in range(2, num_labels):
                    area = stats[label, cv2.CC_STAT_AREA]
                    if area > max_area:
                        max_label = label
                        max_area = area

                result_image = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
                for label in range(1, num_labels):
                    if label != max_label:
                        result_image[labels == label] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

                cv2.imshow("Depth Image", depth_image_copy)

                cv2.imshow("Final Result", result_image)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        cv2.destroyAllWindows()

    def run(self):
        depth_subscriber = rospy.Subscriber("/camera/depth/image_raw", Image, self.depth_callback)
        image_subscriber = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)

        rospy.spin()

if __name__ == "__main__":
    depth_processor = DepthImageProcessor()
    depth_processor.run()
