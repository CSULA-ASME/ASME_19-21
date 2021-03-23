#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('sensor', anonymous=False)
    pub = rospy.Publisher('sensor2smach', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
        sensor2smach_str = "sensor values"
        rospy.loginfo(sensor2smach_str)
        pub.publish(sensor2smach_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
