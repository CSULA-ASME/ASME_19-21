#! /usr/bin/env python
import rospy
from ros_nodes.msg import lidar2smach

while True:
	rospy.init_node('LIDAR')
	lidar_2_smach_pub = rospy.Publisher('lidar2smach', lidar2smach, queue_size=10)
	rate = rospy.Rate(10)
	final_message = lidar2smach()
	while not rospy.is_shutdown():
		final_message.angles_w_objects = [204.14, 14.616, 15.16]

		lidar_2_smach_pub.publish(final_message)
		rate.sleep()
	else:
		exit()
