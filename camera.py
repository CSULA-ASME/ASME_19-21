#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('camera', anonymous=False)
    pub = rospy.Publisher('camera2smach', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
        camera2smach_str = "camera values"
        rospy.loginfo(camera2smach_str)
        pub.publish(camera2smach_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
