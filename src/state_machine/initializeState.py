#!/usr/bin/env python
import roslib
import rospy
import smach
import smach_ros
import time
from ros_nodes.msg import sensors2smach
from ros_nodes.msg import lidar2smach
from ros_nodes.msg import cameras2smach
from ros_nodes.msg import controls2smach
from Subscriber import Subscribe_to

class Initialize(smach.State):
	def __init__(self):
		print("starting")
		smach.State.__init__(self, outcomes=['Finished', 'Failed'])
		#Subscribe to all nodes that publish to smach
		self.sensors_sub = Subscribe_to('sensors2smach')
		self.lidar_sub = Subscribe_to('lidar2smach')
		self.cameras_sub = Subscribe_to('cameras2smach')
		self.controls_sub = Subscribe_to('controls2smach')
		self.counter = 0
		time.sleep(2)

	def execute(self, userdata):
		#Check if all nodes have published data
		sensors_data_sent = self.sensors_sub.was_data_sent()
		lidar_data_sent = self.lidar_sub.was_data_sent()
		cameras_data_sent = self.cameras_sub.was_data_sent()
		controls_data_sent = self.controls_sub.was_data_sent()

		print (sensors_data_sent, lidar_data_sent, cameras_data_sent, controls_data_sent)
		#If any of the nodes are not publishing, stay in this loop
		while ((sensors_data_sent == False) or (lidar_data_sent == False) or
			       (cameras_data_sent == False) or (controls_data_sent == False)):

			time.sleep(0.01)
			#Continue checking if all nodes have published data
			sensors_data_sent = self.sensors_sub.was_data_sent()
			lidar_data_sent = self.lidar_sub.was_data_sent()
			cameras_data_sent = self.cameras_sub.was_data_sent()
			controls_data_sent = self.controls_sub.was_data_sent()
			print (sensors_data_sent, lidar_data_sent, cameras_data_sent, controls_data_sent)
			#If any nodes have failed to publish after ~15 seconds, return failed
			if (self.counter > 1500):
				return 'Failed'
			self.counter = self.counter + 1

		#When all nodes are publishing data, return Finished
		return 'Finished'

def code():
        rospy.init_node('sm')
        main = smach.StateMachine(outcomes=['Done', 'Not_Done'])
        with main:
                smach.StateMachine.add('Initialize', Initialize(), transitions={ 'Finished':'Done',
										'Failed':'Not_Done'})

        sis = smach_ros.IntrospectionServer('server', main, '/tester')
        sis.start()
        outcome = main.execute()
        sis.stop()
        rospy.spin()
        #sis.stop()

if __name__ == '__main__':
        code()


