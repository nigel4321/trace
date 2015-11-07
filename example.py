#!/usr/bin/env python
# encoding: utf-8

import threading
import time
import nitrace

io_lock = threading.Lock()
blocker = threading.Lock()


def func_above(i):
    func2(i)
    return


def func2(i):
    t = threading.current_thread()
    print "in thread"
    with io_lock:
        print '%s with ident %s going to sleep' % (t.name, t.ident)
    # acquired but never released
    blocker.acquire()
    time.sleep(4)
    with io_lock:
        print t.name, 'finishing'
    return


def block_func(i):
    t = threading.current_thread()
    print "in thread"
    with io_lock:
        print '%s with ident %s going to sleep' % (t.name, t.ident)
    if i:
        # acquired but never released
        blocker.acquire()
        time.sleep(4)
    with io_lock:
        print t.name, 'finishing'
    return

tracer = nitrace.CurrentStat()
tracer.mtprint_stack()

# Create and start several threads that "block"
threads = [threading.Thread(target=block_func, args=(i,)) for i in range(5)]
th = [threading.Thread(target=func_above, args=(i,)) for i in range(5)]
threads += th
for t in threads:
    t.setDaemon(True)
    t.start()
