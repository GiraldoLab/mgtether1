#!/usr/bin/env python
import time
import sys
import rospy
import numpy as np

from std_msgs.msg import String
from  basic_led_strip_proxy import BasicLedStripProxy
from basic_led_strip_ros.msg import SunInfo

from basic_led_strip_ros.msg import StripLEDInfo

class ShuffleSun:


    def __init__(self):

        rospy.init_node('shuffle_sun', anonymous=True)
        self.sun_position_pub = rospy.Publisher('sun_position', SunInfo, queue_size=10) #not sure if this is right 
        rate = rospy.Rate(10)#Rate we want to publish message in Hz #added 1/20

        #Create message data structure template & fill in with relevant information
        #sun_msg = SunInfo()
        # Fill in the header information
        #sun_msg.header.stamp = rospy.Time.now()
        #Fill in the
        #sun_msg.sun_position = sun_position
 

        self.led_strip = BasicLedStripProxy(use_thread=True)
        self.led_index_list = range(144)
        self.sun_position = [22, 59, 92, 130]   #sun position in terms of actual LED number
        #np.random.shuffle(self.sun_position)

    def publish_suninfo(self, sun_position, sun_status, time):
        for sun_status in led_strip:
            if sun_status = self.led_strip.set_all(0,128,0)
                sun_status = True
                print('led_on')
            else:
                sun_status = False
                print('led_off')

        sun_msg = SunInfo()
        sun_msg.header.stamp = rospy.Time.now()
        sun_msg.sun_position = sun_position
        sun_msg.sun_status = sun_status
        sun_msg.time = time
        self.sun_position_pub.publish(sun_msg)
        #self.sun_position_pub.publish(StripLEDInfo(header, led_pos, red, green, blue))

        #msg = SunInfo()
        #msg.header.stamp = rospy.Time.now()
        #msg.sun_position = sun_position
        #msg.time = time
        #msg.led_on = led_on
        #self.sun_position_pub.publish(sun_info)

    def run(self):

        while not rospy.is_shutdown():

            #dark period for 'time.sleep' seconds
            self.led_strip.set_all((  0,   0,   0))
            print('dark')
            self.publish_suninfo(self, sun_position, sun_status, time)
            time.sleep (5)

            np.random.shuffle(self.sun_position)
            self.led_strip.set_led(self.sun_position[0],(0,128,0))
            print('sun position = ' + str(self.sun_position[0]))
            self.publish_suninfo(self, sun_position, sun_status, time)
            time.sleep (5)
            #led_color = led_strip.set_all(0,128,0)

            self.led_strip.set_led(self.sun_position[1],(0,128,0))
            print('sun position = ' + str(self.sun_position[1]))
            self.publish_suninfo(self, sun_position, sun_status, time)
            time.sleep (5)

            #dark period for 'time.sleep' seconds
            self.led_strip.set_all((  0,   0,   0))
            self.publish_suninfo(self, sun_position, sun_status, time)
            print('dark')
            time.sleep (5)

            sys.exit()

#-------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = ShuffleSun()
    node.run()


