#! /usr/bin/env python


import rospy
from std_msgs.msg import Int16, Bool
from sensor_msgs.msg import CompressedImage
import os
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge, CvBridgeError


steer = Int16()
steer.data = 1500
throttle = Int16()
# RC car moves at a constant, slow speed
throttle.data = 1460

startFlag = Bool()
startFlag.data = 0
bridge = CvBridge()

def normalize(img):
    img[:,:,0] = np.true_divide(img[:,:,0],255)
    img[:,:,1] = np.true_divide(img[:,:,1],255)
    img[:,:,2] = np.true_divide(img[:,:,2],255)
    return img

def image_callback(msg):
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image_np = cv2.resize(image_np, (320,240))
        image_np = image_np[:][100:]
        # cv2_img = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError:
        print("CVBridgeError")
    else:
        # cv2 image to numpy array
        img = normalize(image_np)
        img = np.expand_dims(img, 0)
        steer.data = model.predict(img)
        steer.data = int((steer.data*199)+1374)
        print("Predicted steer is: " + str(steer.data))
        steer.data = max(1100, min(1900,steer.data))
        startFlag.data = 1
        return


if __name__ == '__main__':
    dataset_path = "~/rcCarEndtoEnd/"
    model_path = "PilotNet_v3-014-0.01591.h5"
    model = load_model(model_path)
    print("Model is ready!")

    rospy.init_node('ros_steer_control')

    pubSteer = rospy.Publisher('/car1/auto_cmd/steer',Int16,queue_size=1)
    pubThrottle = rospy.Publisher('/car1/auto_cmd/throttle',Int16,queue_size=1)
    image_topic = '/camera/color/image_raw/compressed'
    subImage = rospy.Subscriber(image_topic, CompressedImage, image_callback)
    while not rospy.is_shutdown():
        if startFlag.data:
            pubSteer.publish(steer.data)
            pubThrottle.publish(throttle.data)
            print("publishing steer and throttle")
        rospy.sleep(0.3)
        
