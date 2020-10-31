#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    print(data.data)
    
def listener_talker():
    rospy.init_node('smach', anonymous=True)

    rospy.Subscriber("controls2smach", String, callback)
    rospy.Subscriber("lidar2smach", String, callback)
    rospy.Subscriber("sensor2smach", String, callback)
    rospy.Subscriber("camera2smach", String, callback)
#    rospy.spin()

    pub = rospy.Publisher('smach2controls', String, queue_size = 10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
	smach2controls_str = "smach2controls values"
	rospy.loginfo(smach2controls_str)
	pub.publish(smach2controls_str)
	rate.sleep()


if __name__ == '__main__':
    listener_talker()
