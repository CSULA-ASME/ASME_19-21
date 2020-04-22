#!/usr/bin/env python
import roslib
import rospy
import smach
import smach_ros
import time
import math
from ros_nodes.msg import sensors2smach
from ros_nodes.msg import smach2controls
from btest import Subscribe_to

class Waypoint_Navigation(smach.State):
	def __init__(self):
		print("starting")
		smach.State.__init__(self, outcomes=['Finished', 'Failed'], input_keys=['goal'])

		self.sensors_sub = Subscribe_to('sensors2smach')
		self.controls_pub = rospy.Publisher('smach2controls', smach2controls, queue_size=1)
		self.setpoints = smach2controls()
		self.counter = 0
		time.sleep(2)

	def execute(self, userdata):
		sensors_data_sent = self.sensors_sub.was_data_sent()
		print (sensors_data_sent)
		while (sensors_data_sent == False): #If no data received in 6 seconds, Failed
			time.sleep(0.01)
			sensors_data_sent = self.sensors_sub.was_data_sent()
			if (self.counter > 600):
				return 'Failed'
			self.counter = self.counter + 1
		sensors_data = self.sensors_sub.get_data()

		goal_lat = 34.066010     #34 degs, 03.9606 mins (N) || 34 degs, 03 mins, 57.6 s (N)
		goal_lon = -118.167300  #118 degs, 10.0380 mins (W) || 118 degs, 10 mins, 02.3 s (W)

		current_lat_deg_part = int(str(sensors_data.current_latitude)[:2])
		current_lat_min_part = float(str(sensors_data.current_latitude)[2:])
		current_lat = (current_lat_deg_part + (current_lat_min_part/60)) #In pure degrees

		current_lon_deg_part = int(str(sensors_data.current_longitude)[:3])
		current_lon_min_part = float(str(sensors_data.current_longitude)[3:])
		current_lon = (current_lon_deg_part + (current_lon_min_part/60)) #In pure degrees

		current_lon = (current_lon * (-1))   #We will be dealing with the West values only
		Y_error = (goal_lat - current_lat)   #Y axis is Earth's N & S (unit of Lat degrees)
		X_error = (goal_lon - current_lon)   #X axis is Earth's E & W (unit of Lon degrees)
		#For Reference: one side of a field to another is about .001 degrees
		#One degree of Latitude remains mostly constant at 364,000 ft or ~110947.2 meters
		#One degree of Longitude depends on Latitude and average constant of 11319.488 meters
		#USGS says one deg of Lon at 38 degrees Lat is 288,200 ft or ~87843.36 meters
		Y_error = (Y_error * 110947.2)	  #Convert units of Lat & Lon Degrees to real meters
		X_error = (X_error * (111319.488 * (math.cos(math.radians(current_lat)))))
		print Y_error
		print X_error

		ang_from_Earths_X = math.degrees(math.atan(Y_error / X_error))
		if (X_error < 0):		#atan returns only between -90 to 90
			ang_from_Earths_X = ang_from_Earths_X + 180
		elif (Y_error < 0):
			ang_from_Earths_X = ang_from_Earths_X + 360
						#this makes sure that the correct angles are returned
		ang_from_Earths_M = ang_from_Earths_X - 102    #Mag field (M) is 12 degrees left of Y
		if (ang_from_Earths_M < 0):
			ang_from_Earths_M = ang_from_Earths_M + 360
		CW_ang_M = ((ang_from_Earths_M * (-1)) + 360)	#Change CCW to CW angle from Earths M
		ang_Error = CW_ang_M - sensors_data.current_mag_yaw	#Calculate ang Error to turn
		self.setpoints.yaw_setpoint = sensors_data.current_yaw + ang_Error
			   				           #Setpoint = Current Angle + Error
		if (self.setpoints.yaw_setpoint > 360):
			self.setpoints.yaw_setpoint = self.setpoints.yaw_setpoint - 360
		elif (self.setpoints.yaw_setpoint < 0):
			self.setpoints.yaw_setpoint = self.setpoints.yaw_setpoint + 360

		#self.setpoints.distance_setpoint = 0 #Dont move forward, only turn to angle for now
		self.setpoints.distance_setpoint = math.sqrt((Y_error ** 2) + (X_error ** 2))

		self.controls_pub.publish(self.setpoints)
		time.sleep(1)
		return 'Finished'

def code():
	rospy.init_node('sm')
	main = smach.StateMachine(outcomes=['Done', 'Not_Done'])
	main.userdata.lat_lon = []
	with main:
		smach.StateMachine.add('Waypoint_Nav', Waypoint_Navigation(), transitions={
		'Finished':'Done', 'Failed':'Not_Done'}, remapping={'goal':'lat_lon'})

	sis = smach_ros.IntrospectionServer('server', main, '/tester')
	sis.start()
	outcome = main.execute()
	sis.stop()
	rospy.spin()
	#sis.stop()

if __name__ == '__main__':
	code()
