#!/usr/bin/env python
import rospy
from ros_nodes.msg import smach2controls
from ros_nodes.msg import controls2smach

def controls(controls_data):
	the_yaw_input = controls_data.yaw_input
	the_yaw_setpoint = controls_data.yaw_setpoint
	the_distance_input = controls_data.distance_input
	the_distance_setpoint = controls_data.distance_setpoint
	#use the variables for the pid
	print(controls_data)

while True:
	rospy.init_node('CONTROLS')
	controls_2_smach_pub = rospy.Publisher('controls2smach', controls2smach, queue_size=10)
	rospy.Subscriber('smach2controls', smach2controls, controls)
	rate = rospy.Rate(10)
	final_message = controls2smach()
	while not rospy.is_shutdown():
		final_message.stabilized = True
		controls_2_smach_pub.publish(final_message)
		rate.sleep()

	else:
		exit()
