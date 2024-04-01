###NOTE: MIN_LED = 1 (Aprox. 165 degrees), MAX_LED = 141 (Aprox. -165 degrees) 6/22


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
from basic_led_strip_ros.msg import JumpingSunInfo
from collections import Iterable
import random

#from datetime import datetime

class JumpingSun:


    def __init__(self):

        rospy.init_node('jumping_sun')
        rospy.on_shutdown(self.sunset)
        self.jumping_sun_position_pub = rospy.Publisher('jumping_sun_position', JumpingSunInfo, queue_size=10)
        rate = rospy.Rate(5) #Rate we want to publish message in Hz #added 1/20
        self.led_strip = BasicLedStripProxy(use_thread=True) #True? False?
        self.led_index_list = range(144)
        self.current_sun_position = 0
        
    def sunset(self):
        print('Sun is setting')
        self.led_strip.set_all(( 0, 0, 0))
        sys.exit()

    def publish_sun_position(self):
        jumping_sun_msg = JumpingSunInfo()
        jumping_sun_msg.header.stamp = rospy.Time.now()
        jumping_sun_msg.jumping_sun_position = self.current_sun_position
        #rospy.loginfo('Sun Info:' + str(sun_msg)) #shows what is being published as a message
        self.jumping_sun_position_pub.publish(jumping_sun_msg)
    
    def dark(self):
        self.led_strip.set_all((  0,   0,   0))
        self.current_sun_position = 0

    def starting_sun(self, specific_sun_position=None):
        if specific_sun_position is not None:
            self.current_sun_position = specific_sun_position
        else:
            start, end = 1, 141 # when we want to keep it in the range of 57, 129
            self.current_sun_position = random.randint(start,end)
        return self.current_sun_position

    def jumping_sun(self, specific_sun_position = None):
        if specific_sun_position is not None:   ##6/22 is this right? 
            self.current_sun_position = specific_sun_position
            
        else:
            operation = random.choice([-1,1])
            potential_next_position = self.current_sun_position + 6 * operation
        #Ensure the next sun position is within range
            if potential_next_position< 1:
                self.current_sun_position += 6
            elif potential_next_position > 141:
                self.current_sun_position -= 6
            else:
                self.current_sun_position = potential_next_position
        return self.current_sun_position

    def first_sun(self):
        sun_position = self.starting_sun()
        self.led_strip.set_led(sun_position, (0,8,0))
        self.current_sun_position = sun_position
    
    def next_sun(self, specific_sun_position = None):
        sun_position  = self.jumping_sun(specific_sun_position)
        self.led_strip.set_led(sun_position, (0,8,0))
        self.current_sun_position = sun_position


    def run(self):

        while not rospy.is_shutdown():

            #first_sun_position = self.starting_sun()
            first_sun_position = self.first_sun()

            #second_sun_position = self.jumping_sun(first_sun_position)
            second_sun_position = self.next_sun(first_sun_position)

            """
            This experiment consists of the following procedure:
                1) Dark period                                                              - 30 seconds
                2) Random light from range(1, 141)                                          - 5 minute
                3) Light moves 15 degrees clockwise(-6 LED) / counterclockwise (+6 LED)     - 5 minute

                4) Light moves 15 degrees clockwise(-6 LED) / counterclockwise (+6 LED)     - 5 minute
            
            
            """
            
            #print('same sun sampling', same_sun_sampling)
            procedure = [
                            [self.dark,3],
                            [ first_sun_position, 6],
                            [ second_sun_position, 6]
                           
                           
                            # [self.first_sun,300],
                            # [self.next_sun, 300], 
                            # [self.next_sun, 300]
                            


                            
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

    # def experiment(self,procedure):
    #     last_return = None
    #     for step, timestep in procedure:
    #         if isinstance(step,Iterable):
    #             if any(step):
    #                 last_return = next(step)
    #             else:
    #                 print("step {} is no longer iterable".format(step.__name__))
    #         else:
    #             last_return = step() if last_return is None else step (last_return)
    #         self.publish_sun_position()
    #         #print(f'Sun position set to  {self.current_sun_position}')##6/21
    #         print('sun_position: ' + str(self.current_sun_position))
    #         time.sleep(timestep)

#-------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = JumpingSun()
    #node.starting.sun()
    #node.jumping_sun()

    node.run()


