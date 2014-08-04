#!/usr/bin/env python
# DummyMP - Multiprocessing Library for Dummies!
# Copyright 2014 Albert Huang.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# 
# DummyMP Library -
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

from _version import *
from loghandler import *
from process import *
from detect import *
from interface import *
from taskmgr import *
from config import *

import time
import sys

# Just a test function.
def test():
    for i in xrange(0, 10000000):
        pass
    logging.info("Hi there from logging!")
    num = random.randint(2,7)
    logging.info("Sleeping for %i secs..." % num)
    time.sleep(num)
    if num > 5:
        logging.info("Returning the random number %i!" % num)
    logging.info("Bye bye from logging!")
    if num > 5:
        return num

# Just a test function, with args.
def test2(jellybean):
    logging.info("Hi there! Magical jelly bean number arg is %i - sleeping for %i!" % (jellybean, jellybean))
    time.sleep(jellybean)

# Just a test function, with kwargs.
def test3(**kwargs):
    if "jellybean" in kwargs:
        jb = kwargs["jellybean"]
    else:
        jb = 1
    
    logging.info("Hi there! Magical jelly bean number is kwarg %i - sleeping for %i!" % (jb, jb))
    time.sleep(jb)

# Just a test function, with BOTH args and kwargs!
def test4(jellybean, **kwargs):
    if "jellybean2" in kwargs:
        jb = kwargs["jellybean2"]
    else:
        jb = 1
    
    logging.info("Hi there! Magical jelly bean number is arg %i - but sleeping for kwarg %i!" % (jellybean, jb))
    time.sleep(jb)

# If run directly, run some tests using the test function above.
if __name__ == "__main__":
    import random
    
    # Simple running test
    getCPUAvail()
    
    set_max_processes(2)
    
    run(test)
    run(test)
    run(test)
    
    process_until_done()
    
    print get_returns()
    
    if len(get_returns().keys()) != 3:
        print 'ERROR: Could not get all returns!'
        sys.exit(1)
    
    # Run with arguments
    run(test2, 5)
    run(test3, jellybean = 5)
    run(test4, 1, jellybean2 = 5)
    process_until_done()
    
    # Configuration reset test - this should clear max_processes
    print "Resetting..."
    reset()
    run(test)
    run(test)
    run(test)
    
    process_until_done()
    
    # Termination test - this should not run all the way through!
    print "Resetting once more..."
    reset()
    set_max_processes(1)
    run(test)
    run(test)
    run(test)
    
    process_process()
    time.sleep(2)
    reset()
    process_until_done()
    
