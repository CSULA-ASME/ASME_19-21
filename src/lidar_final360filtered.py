#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from ros_nodes.msg import lidar2smach

def lidar_2_smach(all_lidar_data):
   distances = all_lidar_data.ranges
   angles = range (360)
   both = zip(distances, angles)
   previousMax = False
   appendNeeded = False
   previousDetection = False
   for i in both:
      if (i[0] < 0.3):
         if (previousMax == False):
            newMin = i[1]
            newMax = i[1]
            previousMax = True
            appendNeeded = True
         else:
            newMax = i[1]
      else:
         if (appendNeeded == False):
            pass
         elif (previousDetection == False):
            angleRange.angles_w_objects.extend([newMin, newMax])
            firstMin = newMin
            previousMax = False
            appendNeeded = False
            previousDetection = True
         else:
            if ((newMin - angleRange.angles_w_objects[len(angleRange.angles_w_objects) - 1]) <= 2):
               angleRange.angles_w_objects[len(angleRange.angles_w_objects) - 1] = newMax
               previousMax = False
               appendNeeded = False
            if ((newMax >= 358) and (firstMin == 0)):
               angleRange.angles_w_objects[0] = newMin
            else:
               angleRange.angles_w_objects.extend([newMin, newMax])
               previousMax = False
               appendNeeded = False
   print (angleRange)
   lidar_2_smach_pub.publish(angleRange)
   del angleRange.angles_w_objects[:]

def the_main():

   rate = rospy.Rate(5)
   while not rospy.is_shutdown():
      rospy.Subscriber('scan', LaserScan, lidar_2_smach)
      rate.sleep()

if __name__ == '__main__':

   rospy.init_node('LIDAR')
   lidar_2_smach_pub = rospy.Publisher('lidar2smach', lidar2smach, queue_size=10)
   angleRange = lidar2smach()
   try:
      the_main()
   except rospy.ROSInterruptException:
      pass
