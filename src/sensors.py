#! /usr/bin/env python
import rospy
from ros_nodes.msg import sensors2smach

while True:
	rospy.init_node('SENSORS')
	sensors_2_smach_pub = rospy.Publisher('sensors2smach', sensors2smach, queue_size=10)
	rate = rospy.Rate(10)
	final_message = sensors2smach()
	while not rospy.is_shutdown():
		final_message.current_yaw = 0
		final_message.current_distance = 0
		final_message.current_latitude = 3403.9663
		final_message.current_longitude = 11810.02318

		sensors_2_smach_pub.publish(final_message)
		rate.sleep()
	else:
		exit()
