import multiprocessing

# The API is similar to Threading. To make interchangeability easier.
# Threading good for tasks with a lot of IO, but not for CPU heavy things
# Processes have NO shared memory.

def worker(i):
    print("Worker working: ", i)


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()


# Protect your code by wrapping it in main expression or taking it from another module
# Otherwise you'll get recursive spinning

# Naming, Daemon, join, etc. work the same as in Threads

# Process can be sometimes deadlocked or otherwise stuck. You can kill those
import time
def slow_worker():
    print('Starting Worker')
    time.sleep(0.1)
    print('Finished Worker')

if __name__ == '__main__':
    p = multiprocessing.Process(target=slow_worker)
    print('BEFORE:', p, p.is_alive())

    p.start()
    print('DURING:', p, p.is_alive())

    p.terminate()
    print('TERMINATED:', p, p.is_alive())

    p.join()
    print('JOINED:', p, p.is_alive())
    print('Exitcode: ', p.exitcode)

# Termination is not reflected instantly. Add a p.join() to update the processes.
# Get exitcodes with j.exitcode
# Logging and subclassing work the same as with Threads