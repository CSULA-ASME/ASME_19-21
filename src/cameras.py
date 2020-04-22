#! /usr/bin/env python
import rospy
from ros_nodes.msg import cameras2smach

while True:
	rospy.init_node('CAMERAS')
	cameras_2_smach_pub = rospy.Publisher('cameras2smach', cameras2smach, queue_size=10)
	rate = rospy.Rate(10)
	final_message = cameras2smach()
	while not rospy.is_shutdown():
		final_message.something = 0

		cameras_2_smach_pub.publish(final_message)
		rate.sleep()

	else:
		exit()
