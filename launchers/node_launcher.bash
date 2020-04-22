#!/bin/bash
#Use this to see all 5 nodes in separate terminals
gnome-terminal -- sh -c "cd ..; cd src/; python cameras.py; bash"
gnome-terminal -- sh -c "cd ..; cd src/; python controls.py; bash"
gnome-terminal -- sh -c "cd ..; cd src/; python lidar.py; bash"
gnome-terminal -- sh -c "cd ..; cd src/; python sensors.py; bash"
gnome-terminal -- sh -c "cd ..; cd src/; python smach.py; bash"
