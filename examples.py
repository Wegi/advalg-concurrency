# Simple Threading without bells and whistles
import threading


def worker(num):
    result = sum(range(num*6))
    print(result)

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()


import time
# Background Threads where it does not matter if the service dies during the operation are called daemons
def daemon():
    print('D Starting')
    time.sleep(0.2)
    print('D Ending')

def non_daemon():
    print('ND Starting')
    print('ND Ending')


d = threading.Thread(target=daemon, daemon=True)
nd = threading.Thread(target=non_daemon)

d.start()
nd.start()
d.join(0.02)

# Join is blocking indefinitely without time limit

# You can modify the behaviour of threads any time you want
import logging

class LoggingThread(threading.Thread):

    def run(self):
        logging.debug('running')

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

for i in range(5):
    t = LoggingThread()
    t.start()

# The return value of run() is ignored

# Sometimes it is neccessary for Threads to communicate with each other.
# Use flags for those. Every Thread can set and clear flags. Threads can also wait for flags.

def wait_for_event(e):
    logging.debug('waiting for event')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.is_set():
        logging.debug('waiting for event with timeout')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')

e = threading.Event()
t1 = threading.Thread(target=wait_for_event, args=(e,))
t1.start()

t2 = threading.Thread(target=wait_for_event_timeout, args=(e, 0.2))
t2.start()

logging.debug('waiting before calling Event.set()')
time.sleep(0.5)
e.set()
logging.debug('Event is set')

# Sometimes its important to make data only available in the thread where it is created.
import random
def show_value(data):
    try:
        val = data.value
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)

local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()