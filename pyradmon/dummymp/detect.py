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
# DummyMP Library - CPU availability checker
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import psutil
import logging
import datetime
import config

def getCPUAvail():
    """Get number of CPUs available.
    
    Fetch the number of CPUs available based on the current priority
    and limit configuration.
    
    Args:
        None
    
    Returns:
        An integer with the number of CPUs that are available.
    """
    
    logging.debug("Querying CPUs (%s mode)..." % (config.DUMMYMP_STRING[config.DUMMYMP_MODE]))
    
    if (config.DUMMYMP_MODE == config.DUMMYMP_NUCLEAR) or (datetime.datetime.now() - config.LAST_CPU_CHECK <= config.CPU_CHECK_TIMEDELTA_THRESHOLD):
        return config.CPU_AVAIL
    
    ncpus = psutil.cpu_count()
    avg = []
    
    for i in xrange(0, config.DUMMYMP_MCYCLE[config.DUMMYMP_MODE] - 1):
        percent = psutil.cpu_percent(interval=config.DUMMYMP_MINTERVAL[config.DUMMYMP_MODE], percpu=True)
        
        if len(avg) == 0:
            avg = percent
        else:
            for n in xrange(0, len(percent)):
                avg[n] = (avg[n] + percent[n]) / 2
    
    # Threshold
    avail_cpus_arr = []
    for n in xrange(0, len(percent)):
        if avg[n] < config.DUMMYMP_THRESHOLD[config.DUMMYMP_MODE]:
            avail_cpus_arr.append(True)
        else:
            avail_cpus_arr.append(False)
    
    available_num_cpus = avail_cpus_arr.count(True)
    logging.debug("%i / %i CPUs available!" % (available_num_cpus, ncpus))
    
    config.CPU_AVAIL = available_num_cpus
    config.LAST_CPU_CHECK = datetime.datetime.now()
    return available_num_cpus
