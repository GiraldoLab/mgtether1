#!/usr/bin/env python
from __future__ import print_function
import threading
import roslib
import rospy
from basic_led_strip import BasicLedStrip
from basic_led_strip_ros.msg import StripLEDInfo
from basic_led_strip_ros.srv import SetStripLED
from basic_led_strip_ros.srv import SetStripLEDResponse 

class BasicLedStripNode(object):

    def __init__(self):
        rospy.init_node('basic_led_strip')
        self.port = rospy.get_param('/basic_led_strip/port', '/dev/sun_strip')
        self.led_strip = BasicLedStrip(self.port)
        self.led_strip.off()
        self.set_led_srv = rospy.Service('set_strip_led', SetStripLED, self.set_led_srv_callback)
        self.led_info_pub = rospy.Publisher('strip_led_info', StripLEDInfo, queue_size=10)


    def set_led_srv_callback(self,req):
        success = True
        message = ''
        if req.led_number >= 0:
            try:
                self.led_strip.set(req.led_number, (req.red, req.green, req.blue), mode='inclusive')#changed from 'exclusive' to show multiple leds 2/15/24 HP
            except Exception, e:
                success = False
                message = str(e)
        else:
            try:
                self.led_strip.set_all((req.red, req.green, req.blue))
            except Exception, e:
                success = False
                message = str(e)

        msg = StripLEDInfo()
        msg.header.stamp = rospy.Time.now()
        msg.led_number = req.led_number
        msg.red = req.red
        msg.green = req.green
        msg.blue = req.blue
        msg.success = success
        msg.message = message
        self.led_info_pub.publish(msg)

        return SetStripLEDResponse(success, message)

    def run(self):
        while not rospy.is_shutdown():
            rospy.sleep(0.1)
            
    def all_off(self):
        self.led_strip = BasicLedStrip(self.port)
        self.led_strip.off()


# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = BasicLedStripNode()
    node.run()

