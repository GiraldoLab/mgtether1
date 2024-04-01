#!/usr/bin/env python
import datetime
import time
import sys
import rospy
import numpy as np
from copy import copy
from std_msgs.msg import Header #Need this for SunInfo? 2/9
from std_msgs.msg import String
from  basic_led_strip_proxy import BasicLedStripProxy
from basic_led_strip import BasicLedStrip
from basic_led_strip_ros.msg import StripLEDInfo
from basic_led_strip_ros.msg import SunInfo
from collections import Iterable

#from datetime import datetime

class ShuffleSun:


    def __init__(self):

        rospy.init_node('shuffle_sun')
        rospy.on_shutdown(self.sunset)
        self.sun_position_pub = rospy.Publisher('sun_position', SunInfo, queue_size=10)
        rate = rospy.Rate(5) #Rate we want to publish message in Hz #added 1/20
        self.led_strip = BasicLedStripProxy(use_thread=True) #True? False?
        self.led_index_list = range(144)
        self.sun_positions = [19, 57, 93, 129]  #sun position in terms of actual LED number 
        self.current_sun_position = 0
        np.random.shuffle(self.sun_positions)

    def sunset(self):
        print('Sun is setting')
        self.led_strip.set_all(( 0, 0, 0))
        sys.exit()

    def publish_sun_position(self):
        sun_msg = SunInfo()
        sun_msg.header.stamp = rospy.Time.now()
        sun_msg.sun_position = self.current_sun_position
        #rospy.loginfo('Sun Info:' + str(sun_msg)) #shows what is being published as a message
        self.sun_position_pub.publish(sun_msg)
    
    def dark(self):
        self.led_strip.set_all((  0,   0,   0))
        self.current_sun_position = 0
    def sun_sample_no_replacement1(self):
        for sun_position in self.sun_positions:
            self.current_sun_position = self.sun_positions[0] 
            self.led_strip.set_led(self.sun_positions[0],(0,8,0)) #original (0,128,0)
            yield self.sun_positions[0]

    def sun_sample_no_replacement2(self):
        for sun_position in self.sun_positions:
            self.current_sun_position = self.sun_positions[0] 
            self.led_strip.set_led(self.sun_positions[0],(0,50,0)) #original (0,128,0)
            yield self.sun_positions[0]

    def run(self):

        while not rospy.is_shutdown():

            """
            This experiment consists of the following procedure:
                1) Dark period                                                        - 30 seconds
                2) Random light from positions [19(135), 57(45), 93(-45), 129(-135)]  - 5 minute
                3) Random light from positions [19, 57, 93, 129] w/o replacement      - 5 minute
                4) Dark period                                                        - 30 seconds
            
            """
            sun_sampling1 = self.sun_sample_no_replacement1()
            sun_sampling2 = self.sun_sample_no_replacement2()
            procedure = [
                            [self.dark,2],
                            [sun_sampling1,4],
                            [self.dark,3],
                            [sun_sampling2,6],

                            

                            
                        ]
            self.experiment(procedure)
            self.sunset() # sys.exit()

    def experiment(self,procedure):
        for step, timestep in procedure:
            if isinstance(step,Iterable):
                if any(step):
                    next(step)
                else:
                    print("step {} is no longer iterable".format(step.__name__))
            else:
                step()
            self.publish_sun_position()
            print('sun_position: ' + str(self.current_sun_position))
            time.sleep(timestep)

#-------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = ShuffleSun()
    node.run()


