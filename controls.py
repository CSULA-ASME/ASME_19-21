#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    print(data.data)
    
def listener_talker():
    rospy.init_node('controls', anonymous=True)

    rospy.Subscriber("smach2controls", String, callback)



    pub = rospy.Publisher('controls2smach', String, queue_size = 10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
	controls2smach_str = "controls2smach values"
	rospy.loginfo(controls2smach_str)
	pub.publish(controls2smach_str)
	rate.sleep()


if __name__ == '__main__':
    listener_talker()
