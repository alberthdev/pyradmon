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

if __name__ == "__main__":
    import random
    getCPUAvail()
    
    set_max_processes(2)
    
    run(test, [])
    run(test, [])
    run(test, [])
    
    process_until_done()
    
    print get_returns()
    
    if len(get_returns().keys()) != 3:
        print 'ERROR: Could not get all returns!'
        sys.exit(1)
    
    print "Resetting..."
    reset()
    run(test, [])
    run(test, [])
    run(test, [])
    
    process_until_done()
    
    print "Resetting once more..."
    reset()
    set_max_processes(1)
    run(test, [])
    run(test, [])
    run(test, [])
    
    process_process()
    time.sleep(2)
    reset()
    process_until_done()
    
