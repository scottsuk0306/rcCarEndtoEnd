#! /usr/bin/env python

import rospy
from std_msgs.msg import Int16, Image
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
throttle.data = 1560

def normalize(img):
    img[:,:,0] -= 100
    img[:,:,0] /= 64

    img[:,:,1] -= 99
    img[:,:,1] /= 63

    img[:,:,2] -= 98
    img[:,:,2] /= 65    
    return img

def image_callback(msg):
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        # cv2 image to numpy array
        img = normalize(img)
        img = np.expand_dims(num_img, 0)
        steer.data = model.predict(img)
        steer.data = max(1100, min(1900,steer.data))
    return


if __name__ == '__main__':
    dataset_path = "~/rcCarEndtoEnd/"
    model_path = os.path.join(dataset_path,"model/PilotNet_v1-001-0.04877.h5")
    model = load_model(model_path)
    print("Model is ready!")

    rospy.init_node('ros_steer_control')

    pubSteer = rospy.Publisher('/car1/auto_cmd/steer',Int16,queue_size=1)
    pubThrottle = rospy.Publisher('/car1/auto_cmd/throttle',Int16,queue_size=1)

    subImage = rospy.Subscriber(image_topic, Image, image_callback)
    image_topic = '/camera/color/image_raw/compressed'
    rate = rospy.Rate(10) # Publish at 2Hz
    
    while not rospy.is_shutdown():     # Endless loop until Ctrl+C
        pubSteer.publish(steer)
        pubThrottle.publish(throttle)
        # publishing has to happen after subscribing.
        # add rospy.sleep(1) for synchronization
