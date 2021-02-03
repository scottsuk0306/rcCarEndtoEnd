#! /usr/bin/python

import os
import sys
import cv2
import csv
import rospy, rosbag
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

if len(sys.argv) == 2:
    out_dir = sys.argv[1]
    if not os.path.exists(sys.argv[1]):
        os.makedirs(out_dir)

    else:
        print sys.argv[1], 'already exists'
        sys.exit()

else:
    print 'specify output directory'
    sys.exit()

bridge = CvBridge()

def main():
    rospy.init_node('image_save')
    # Topic name 
    topicName0 = '/camera/color/image_raw/compressed'
    topicName1 = '/car1/rc_cmd/steer'           # steer
    # topicName2 = '/car1/rc_cmd/throttle'        # throttle

    # Bag file 
    inbag_name ='./2021-01-26-15-49-24.bag'

    bag = rosbag.Bag(inbag_name)
    flag = False

    for topic, msg, t in bag.read_messages():

        if(topic == topicName0):
            try:
                # Convert compressed image to RAW
                img = bridge.compressed_imgmsg_to_cv2(msg)

            except CvBridgeError, e:
                print(e)

            else:
                # Writing image to the directory mentioned while executing script
                cv2.imwrite(sys.argv[1] +'/frame_' + str(msg.header.stamp) + '.jpeg', img)

                # Saving metadata information as per requirement
                with open(sys.argv[1] +'/metadata.csv','ab') as f1:
                    thewriter1 = csv.writer(f1)
                    thewriter1.writerow([str(t), 'frame_'+ str(msg.header.stamp) + '.jpeg'])

            flag = True
        
        if(topic == topicName1):
            if(flag):
                with open(sys.argv[1] +'/steer_metadata.csv','ab') as f2:
                        thewriter2 = csv.writer(f2)
                        thewriter2.writerow([str(t), str(msg)[-5:]])
                flag = False

            
    bag.close()
    # rospy.spin()

if __name__ == "__main__":
    main()
    print "Done."