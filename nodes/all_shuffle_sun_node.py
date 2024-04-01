#!/usr/bin/env python



import datetime
from re import S
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
import random


class ShuffleSun:


    def __init__(self):

        rospy.init_node('shuffle_sun')
        rospy.on_shutdown(self.sunset)
        self.sun_position_pub = rospy.Publisher('sun_position', SunInfo, queue_size=10)
        rate = rospy.Rate(5) #Rate we want to publish message in Hz #added 1/20
        self.led_strip = BasicLedStripProxy(use_thread=True) #True? False?
        self.led_index_list = range(204)
        ######################################### 
        self.sun_positions = [19,57,93,129] #Green sun #sun position in terms of actual LED number 19(135)18, 57(45)56, 93(-45)92, 129(-135)128
        #self.sun_positions = [ 152, 168, 183, 198] #UV sun
        self.grn_uv_suns = [[19,183], [57,198], [93,152], [129,168]]#  [[19,152], [57,168], [93,183], [129,198]]
        ###########################                                                                                                  ##############
        #self.sun_positions = [ 93, 99, 105 ] #For testing LEDs
        ########################################
        self.current_sun_position = [57,198]####Change this when running 1hr, 2hr, 6hr #2/16/24 Changed to show 2 suns #Original self.current_sun_position = 0
        ########################################
        np.random.shuffle(self.sun_positions) #!!!comment out if you need the same sun(and put the same sun position in the very front)
        #print(self.sun_positions)
        np.random.shuffle(self.grn_uv_suns)
        print(self.grn_uv_suns)
        self.last_operation = None
        

    def sunset(self):
        print('Sun is setting')
        self.led_strip.set_all(( 0, 0, 0))
        sys.exit()

    # def publish_sun_position(self): #original
    #     sun_msg = SunInfo()
    #     sun_msg.header.stamp = rospy.Time.now()
    #     sun_msg.sun_position = self.current_sun_position
    #     #rospy.loginfo('Sun Info:' + str(sun_msg)) #shows what is being published as a message
    #     self.sun_position_pub.publish(sun_msg)
    # def combine_suns(sun1, sun2):
    #     combined_suns = int(str(sun1) +str(sun2))
    #     return combined_suns

    def publish_sun_position(self):
        sun_msg = SunInfo()
        sun_msg.header.stamp = rospy.Time.now()
        if isinstance(self.current_sun_position, int):
            sun_msg.sun_position = self.current_sun_position
        elif isinstance(self.current_sun_position, list):
            sun_msg.sun_position = int(str(self.current_sun_position[0])+ str(self.current_sun_position[1]))
        #sun_msg.sun_position = self.current_sun_position
        # if isinstance(self.current_sun_position, int):
        #     sun_msg.first_sun = self.current_sun_position
        #     sun_msg.sec_sun = 0
        # elif isinstance(self.current_sun_position, list):
        #     sun_msg.first_sun = self.current_sun_position[0]
        #     sun_msg.sec_sun = self.current_sun_position[1]

        rospy.loginfo('Sun Info:' + str(sun_msg)) #shows what is being published as a message
        self.sun_position_pub.publish(sun_msg)




    
    def dark(self):
        self.led_strip.set_all((  0,   0,   0))
        self.current_sun_position = 0 #changed to present 2 suns #Original self.current_sun_position = 0
        print('This is the dark period')
    #   for sun_position in self.sun_positions:
    #       self.current_sun_position = self.sun_positions[0]
    #       self.led_strip.set_led(self.sun_positions[0],(0,8,0)) #original (0,128,0) -lowered brightness
    #       yield self.sun_positions[0]


#original######

    def sun_sample_no_replacement(self):
          for sun_position in self.sun_positions:
              self.current_sun_position = sun_position
              #self.led_strip.set_led(sun_position,(0,8,0)) #original (0,128,0) -lowered brightness (MAX:255)
              self.led_strip.set_led(sun_position,(8,8,8)) #for uv led strip
              yield sun_position


    """
    Added 6/27 to test 'Jumping Sun' paradigm 
    starting_sun: Randomly selects a sun position between the range of (1, 141)
    jumping_sun: Moves the sun 15-degrees (~6LEDs) clockwise(-6) or counterclockwise(+6)

    """

#YG JL comment out for 2 pixel sun shift
#   def starting_sun(self):
#        start, end = 1, 141
#        return random.randint(start,end)
#
#    def jumping_sun(self): #change number according the the number of LEDs you are moving 6-->1 8/17
#        if self.last_operation is None:
#            self.last_operation = random.choice([-1,1])
#        
#        potential_next_position = self.current_sun_position + 2 * self.last_operation #change number according the the number of LEDs you are moving
#        #Ensure the next sun position is within range
#        if potential_next_position< 25:     ##change number to keep within range of 1-141
#            self.current_sun_position += 2 
#            self.last_operation = 1
#
#        elif potential_next_position > 116:    ##change number to keep within range of 1-141
#            self.current_sun_position -= 2
#            self.last_operation = -1
#        else:
#            self.current_sun_position = potential_next_position
#        return self.current_sun_position

 # CW trials
    # def starting_sun(self):
    #     start, end = 38, 141
    #     return random.randint(start,end)  ##for random sun stimulus selection between a specific range

#Original grn sun 15deg per hour sun shift experiments 12/11/23
    # def starting_sun(self): 
    #     for sun_position in self.sun_positions:
    #         return random.choice(self.sun_positions)


    # def jumping_sun(self): #change number according the the number of LEDs you are moving 6-->1 8/17
    #     ######
    #     potential_next_position = self.current_sun_position -36 #change number  (11am 15deg: ~6LEDs, 12pm 30deg:~12LEDs, 16pm 90deg: ~36LEDs) clockwise -, counterclockwise +
    #     #######
    #     self.current_sun_position = potential_next_position
    #     return self.current_sun_position

#For two suns grn&uv 180deg apart 15deg per hour sun shift experiments 3/18/24
    def starting_sun(self): 
        for sun_position in self.grn_uv_suns:
            return random.choice(self.grn_uv_suns)


    def jumping_sun(self): #change number according the the number of LEDs you are moving 6-->1 8/17
        ######
        
        next_grn= self.current_sun_position[0] -12 #change number  (11am 15deg: ~6LEDs, 12pm 30deg:~12LEDs, 16pm 90deg: ~36LEDs) clockwise -, counterclockwise +
        next_uv = self.current_sun_position[1] -5 #change number  (11am 15deg: ~3LEDs, 12pm 30deg:~5LEDs, 16pm 90deg: ~15LEDs) clockwise -, counterclockwise +
        #######
        self.current_sun_position = [next_grn, next_uv]
        print(self.current_sun_position)
        return self.current_sun_position

#CCW trials
#    def starting_sun(self):
#        start, end = 0, 104
#        return random.randint(start,end)  ##for random sun stimulus selection between a specific range

#    def jumping_sun(self): #change number according the the number of LEDs you are moving 6-->1 8/17
#        potential_next_position = self.current_sun_position + 6 #change number according the the number of LEDs you are moving
#        self.current_sun_position = potential_next_position
#        return self.current_sun_position

#Original when moving 1 green sun 15degs
    # def set_sun(self):
    #     print("Current sun position at beginning of next_sun: {}".format(self.current_sun_position))
    #     ###############
    #     #self.current_sun_position = 57 ###USE when running flight at 11, 12, 16 periods
    #     ################
    #     if self.current_sun_position ==0:
    #         sun_position = self.starting_sun()
    #     else: 
    #         sun_position = self.jumping_sun()
    #     self.led_strip.set_led(sun_position, (0,8,0))
    #     self.current_sun_position = sun_position
    #     self.publish_sun_position()

#For two suns grn&uv 180deg apart 15deg per hour sun shift experiments 3/18/24
    def set_sun(self):
        print("Current sun position at beginning of next_sun: {}".format(self.current_sun_position))
        ###############
        #self.current_sun_position = 57 ###USE when running flight at 11, 12, 16 periods
        ################
        if self.current_sun_position ==0:
            sun_position = self.starting_sun()
        else: 
            self.led_strip.set_all(( 0, 0, 0)) #since mode was changed to 'inclusive' needed to add this to turn of previous  two suns
            sun_position = self.jumping_sun()
        self.led_strip.set_led(sun_position[0], (0,8,0))
        self.led_strip.set_led(sun_position[1], (8,8,8))
        self.current_sun_position = sun_position
        self.publish_sun_position()

    
    def cue_conflict(self):

        if self.current_sun_position ==0:
            print('self.current_sun_position is ', self.current_sun_position)
            sun_position = self.grn_uv_suns[0]
            print('two sun positions', sun_position)
            self.led_strip.set_led(sun_position[0], (0,8,0))  #Edited basic_led_stripe_node.py set_led_srv_callback function to show two leds at the same time(mode='exclusive' -> 'inclusive') Change back to 'exclusive' after cue conflict experiments!
            print('sun_position1:', sun_position)
            self.led_strip.set_led(sun_position[1], (8,8,8))

            #return self.current_sun_position
            
        else:
            print('current sun position',self.current_sun_position)
            
            grn_sun_position = self.current_sun_position[0]
            self.led_strip.set_all(( 0, 0, 0)) #since mode was changed to 'inclusive' needed to add this to turn of previous  two suns
            self.led_strip.set_led(grn_sun_position, (0,8,0)) #for green
            sun_position =grn_sun_position

            # uv_sun_position = self.current_sun_position[1]
            # self.led_strip.set_all(( 0, 0, 0)) #since mode was changed to 'inclusive' needed to add this to turn of previous  two suns
            # self.led_strip.set_led(uv_sun_position, (8,8,8)) #for uv
            # sun_position = uv_sun_position 

        self.current_sun_position = sun_position

        print('current sun position',self.current_sun_position)



    def two_suns(self):
        if self.current_sun_position ==0:
            sun_position = random.choice(self.grn_uv_suns)
            self.led_strip.set_led(sun_position[0], (0,8,0))  #Edited basic_led_stripe_node.py set_led_srv_callback function to show two leds at the same time(mode='exclusive' -> 'inclusive') Change back to 'exclusive' after cue conflict experiments!
            
            self.led_strip.set_led(sun_position[1], (8,8,8))
        else:
            self.led_strip.set_all(( 0, 0, 0)) #since mode was changed to 'inclusive' needed to add this to turn of previous two suns!!!!!
            rotations ={
                (19, 183): [[129,168], [57,198]],
                (57, 198): [[19,183], [93,152]],
                (93, 152): [[57,198], [129,168]],
                (129,168): [[93,152], [19,183]]
            }
            if tuple(self.current_sun_position) in rotations:
                rotated_sun= rotations[tuple(self.current_sun_position)]
                clockwise = random.choice([True,False])
                sun_position = rotated_sun[0] if clockwise else rotated_sun[1]

                self.led_strip.set_led(sun_position[0], (0,8,0))  #Edited basic_led_stripe_node.py set_led_srv_callback function to show two leds at the same time(mode='exclusive' -> 'inclusive') Change back to 'exclusive' after cue conflict experiments!
                self.led_strip.set_led(sun_position[1], (8,8,8))
            else: 
                print("Invalid self.current_sun_position", self.current_sun_position)
        self.current_sun_position = sun_position






    def run(self):

        while not rospy.is_shutdown():

            """
            This experiment consists of the following procedure:
                1) Dark period                                                        - 30 seconds
                2) Random light from positions [19(135), 57(45), 93(-45), 129(-135)]  - 5 minute
                3) Random light from positions [19, 57, 93, 129] w/o replacement      - 5 minute
                4) Dark period                                                        - 30 seconds


            'Jumping Sun' paradigm for moving the sun 15 degrees clockwise or counterclockwise:

                1) Dark period                                                              - 30 seconds
                2) Random light from range(1, 141)                                          - 5 minute
                [5min rest period in the dark with kimwipe]
                3) Light moves 15 degrees clockwise(-6 LED) / counterclockwise (+6 LED)     - 5 minute
            
            """
            sun_sampling = self.sun_sample_no_replacement()
            #print('same sun sampling', same_sun_sampling)


            

            procedure = [
                                ##for moving two suns(grn&uv) 90degs
            
                                # [self.dark,30], 
                                # [self.two_suns,300],
                                # [self.two_suns,300] 

                                [self.dark,2],
                                [self.set_sun, 13],
                                [self.set_sun, 13]
                                # [self.dark, 30],
                                # [self.cue_conflict, 300],
                                # [self.cue_conflict,300]
                                # [self.dark, 3], 
                                # [self.set_sun, 3]

                                # [self.dark,30],
                                # [sun_sampling,300],
                                # [sun_sampling,300], 
                                # [sun_sampling,300]                          

                        # # # #for continuous flight
                              #[self.dark,30],
                              #[sun_sampling,300],
                              #[self.dark,300],                        
                              #[sun_sampling,300]
                       
                        #For moving sun 15 degrees
                            # [self.dark,30],
                            # [self.set_sun, 100],
                            # [self.set_sun, 100],
                            # [self.set_sun, 100],
                            #  [self.set_sun, 100],
                            # [self.set_sun, 100],
                            # [self.set_sun, 100],
                            #  [self.set_sun, 100],
                            # [self.set_sun, 100],
                            # [self.set_sun, 100],
                            #  [self.set_sun, 100],
                            # [self.set_sun, 100],
                            # [self.set_sun, 100]



                            

                            
                        ]
            self.experiment(procedure)
            self.sunset() # sys.exit()


    # def experiment(self,procedure):
    #     for step, timestep in procedure:
    #         #print("Before step:", step.__name__)
    #         if isinstance(step,Iterable):
    #             try:
    #                 next(step)
    #             except StopIteration:
    #                 print("step {} is no longer iterable".format(step.__name__))
    #         else:
    #             step()
    #         self.publish_sun_position()
    #         print('sun_position: ' + str(self.current_sun_position))
    #         time.sleep(timestep)
    #         print("After step:", step.__name__)
    def experiment(self,procedure):
            for step, timestep in procedure:
                print("Before step:", step.__name__)
                if isinstance(step,Iterable):
                    if any(step):
                        next(step)
                    else:
                        print("step {} is no longer iterable".format(step.__name__))
                else:
                    step()
                self.publish_sun_position()
                print('sun_position: ' + str(self.current_sun_position))
                time.sleep (timestep)
                print("After step:", step.__name__)

#-------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = ShuffleSun()
    node.run()


