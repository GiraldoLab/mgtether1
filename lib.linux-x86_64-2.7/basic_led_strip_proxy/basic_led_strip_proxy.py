from __future__ import print_function
import time
import rospy

import threading
import Queue

from basic_led_strip_ros.srv import SetStripLED


class BasicLedStripProxyException(Exception):
    pass


class BasicLedStripProxy(object):

    def __init__(self,namespace=None, use_thread=True):

        self.namespace = namespace
        self.use_thread = use_thread
        self.service_name = 'set_strip_led'

        if self.namespace is not None:
            self.service_name = '/{}/{}'.format(self.namespace,self.service_name)
        rospy.wait_for_service(self.service_name)
        
        if self.use_thread:
            self.lock = threading.Lock()
            self.stop_thread = False
            self.proxy_queue = Queue.Queue()
            self.proxy_thread = threading.Thread(target=self.proxy_target)
            self.proxy_thread.daemon = True
            self.proxy_thread.start()
        else:
            self.set_led_proxy = rospy.ServiceProxy(self.service_name,SetStripLED)

    def stop(self):
        """ Required for cleanup when using thread """
        if self.use_thread:
            with self.lock:
                self.stop_thread = True
            self.proxy_thread.join()

    def set_all(self, rgb_values):
        data = (-1, rgb_values[0], rgb_values[1], rgb_values[2])
        if self.use_thread:
            self.proxy_queue.put(data)
        else:
            rsp = self.set_led_proxy(*data)
    
    def set_led(self, led_num, rgb_values):
        if led_num >= 0:
            data = (led_num, rgb_values[0], rgb_values[1], rgb_values[2])
        else:
            data = (led_num, 0, 0, 0)
        if self.use_thread:
            self.proxy_queue.put(data)
        else:
            rsp = self.set_led_proxy(*data)

    def proxy_target(self):
        set_led_proxy = rospy.ServiceProxy(self.service_name,SetStripLED)
        done = False
        while not done: 
            with self.lock:
                done = self.stop_thread
            try:
                data = self.proxy_queue.get_nowait()
            except Queue.Empty:
                continue
            rsp = set_led_proxy(*data)


# Testing
# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    proxy = BasicLedStripProxy()

    f = 5.0

    for i in range(10):

        t0 = time.time()
        proxy.set_led(i, (100,0,0))
        proxy.set_led(i+1, (0,0,100))
        t1 = time.time()
        dt = t1 - t0
        print(i,1/dt)
        time.sleep(1/f)
        proxy.set_led(i, (0,0,0))
        proxy.set_led(i+1, (0,0,0))


    time.sleep(2.0)
    proxy.stop()











