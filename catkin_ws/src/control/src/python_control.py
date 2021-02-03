#! /usr/bin/env python

import rospy
from std_msgs.msg import Int16
from curtsies import Input

rospy.init_node('ros_control_publisher')
pubSteer = rospy.Publisher('/car1/auto_cmd/steer',Int16,queue_size=1)
pubThrottle = rospy.Publisher('/car1/auto_cmd/throttle',Int16,queue_size=1)
rate = rospy.Rate(10) # Publish at 2Hz
steer = Int16()
throttle = Int16()

steer.data = 1500
throttle.data = 1500

def wasd2nubmers(key):
    if key == "w":
        throttle.data += 100
        throttle.data = max(1100, throttle.data)
        throttle.data = min(1900, throttle.data)
        return
    elif key == "s":
        throttle.data -= 100
        throttle.data = max(1100, throttle.data)
        throttle.data = min(1900, throttle.data)
        return
    elif key == "a":
        steer.data -= 100
        steer.data = max(1100, steer.data)
        steer.data = min(1900, steer.data)
        return
    elif key == "d":
        steer.data += 100
        steer.data = max(1100, steer.data)
        steer.data = max(1900, steer.data)
        return
    else:
        return

if __name__ == '__main__':
    # while not rospy.is_shutdown():     # Endless loop until Ctrl+C
    with Input(keynames='curses') as input_generator:
        for e in input_generator:
            # print(repr(e))
            wasd2nubmers(e)
            pubSteer.publish(steer)
            pubThrottle.publish(throttle)
            # var.data += 1
            rate.sleep()