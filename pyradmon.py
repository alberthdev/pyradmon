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
# Main Program
# 

import os
import pyradmon.wrapper
import pyradmon.debug

try:
    pyradmon.wrapper.main()
except Exception, e:
    debug_env_var = os.environ.get('PYRADMON_DEBUG')
    if debug_env_var:
        print "PYRADMON_DEBUG defined, calling for help!\n"
        pyradmon.debug.kaboom()
        
