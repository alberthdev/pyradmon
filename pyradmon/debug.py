#!/usr/bin/env python
# PyRadmon - Python Radiance Monitoring Tool
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
# Bug Report Library -
#   library for detecting and reporting bugs
# 

import sys
import traceback
from pprint import pprint
from _version import __version__

def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if not exc is None:  # i.e. if an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
                            # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if not exc is None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr

def kaboom():
    print "KABOOM! Looks like something went wrong."
    print "We're collecting some debug information, please wait...\n"
    stack = full_stack()
    
    fh = open("debug.log", "w")
    
    fh.write("PyRadmon v%s Debug Log\n" % __version__)
    fh.write(("=" * 60) + "\n\n")
    
    fh.write("Stack trace:\n")
    fh.write("================\n")
    fh.write(stack)
    fh.write("\n\n")
    fh.write("Variables:\n")
    fh.write("================\n")
    fh.write("Local Variables:\n")
    pprint(locals(), fh)
    
    fh.write(("=" * 50) + "\n\n")
    
    fh.write("Global Variables:\n")
    pprint(globals(), fh)
    fh.write(("=" * 50) + "\n\n")
    fh.close()
    
    print "A debug log, debug.log, has been written. Please send this"
    print "log to the developer. With it, please include a description"
    print "of your problem and how you got to this bug."
    print ""
    print "Thanks!"
    
    sys.exit(1)
