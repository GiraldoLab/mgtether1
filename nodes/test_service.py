import time
from  basic_led_strip_proxy import BasicLedStripProxy

led_strip = BasicLedStripProxy(use_thread=False)

led_index_list = range(204)

for i in led_index_list:
    print(i)
    led_strip.set_led(i,(100,0,0))
    time.sleep(0.1)


for i in reversed(led_index_list):
    print(i)
    led_strip.set_led(i,(0,0,100))
    time.sleep(0.1)


led_strip.set_all((100, 100,   0))
time.sleep(1.0)
led_strip.set_all((  0, 100, 100))
time.sleep(1.0)
led_strip.set_all((100,   0, 100))
time.sleep(1.0)
led_strip.set_all((100,   0, 100))
time.sleep(1.0)
led_strip.set_all((  0,   0,   0))




