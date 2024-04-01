#!/usr/bin/env python
import time
import numpy as np

from  basic_led_strip_proxy import BasicLedStripProxy

led_strip = BasicLedStripProxy(use_thread=False)

led_index_list = range(144)

#sun position in terms of actual LED number
sun_position = [22, 59, 92, 130]
random_sun = np.random.shuffle(sun_position)

#dark period for 'time.sleep' seconds
led_strip.set_all((  0,   0,   0))
print('dark')
time.sleep (30)

#randomized shuffled sun stimulus (four positions 90 degrees apart) for 'time.sleep' seconds each
for random_sun in sun_position:
    led_strip.set_led(random_sun,(0,128,0)) #made more green from (0,255,55)
    print('sun position = ' + str(random_sun))
    time.sleep(30)

led_strip.set_all((  0,   0,   0))
print('dark')

# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    node = ShuffleSunCommand()
    node.run()


