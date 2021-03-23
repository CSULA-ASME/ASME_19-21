#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('lidar', anonymous=False)
    pub = rospy.Publisher('lidar2smach', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
        lidar2smach_str = "lidar values"
        rospy.loginfo(lidar2smach_str)
        pub.publish(lidar2smach_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
