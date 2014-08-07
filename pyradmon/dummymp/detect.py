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

def needUpdateCPUAvail():
    return not ( \
            (config.DUMMYMP_MODE == config.DUMMYMP_NUCLEAR) or \
            (datetime.datetime.now() - config.LAST_CPU_CHECK <= config.CPU_CHECK_TIMEDELTA_THRESHOLD))

def checkProcRunning():
    running = 0
    for proc in config.dummymp_procs:
        if proc.is_alive():
            running += 1
    return running

def getTotalCPUs():
    return psutil.cpu_count()

def getCPUAvail():
    """Get number of CPUs available.
    
    Fetch the number of CPUs available based on the current priority
    and limit configuration.
    
    Args:
        None
    
    Returns:
        An integer with the number of CPUs that are available.
    """
    
    # Initial check
    cur_running_initial = checkProcRunning()
    
    # If the time threshold is met, OR we are in NUCLEAR mode, just
    # return the cached CPU availability.
    if (config.DUMMYMP_MODE == config.DUMMYMP_NUCLEAR) or (datetime.datetime.now() - config.LAST_CPU_CHECK <= config.CPU_CHECK_TIMEDELTA_THRESHOLD):
        return config.CPU_AVAIL
    
    # Get number of CPUs!
    ncpus = psutil.cpu_count()
    
    # Initialize array...
    avg = []
    
    # Check to make sure we aren't looking at ourselves!
    if config.total_running == config.CPU_AVAIL:
        return config.CPU_AVAIL
    
    logging.debug("Querying CPUs (%s mode)..." % (config.DUMMYMP_STRING[config.DUMMYMP_MODE]))
    
    # Get measurements for the specified number of times
    for i in xrange(0, config.DUMMYMP_MCYCLE[config.DUMMYMP_MODE] - 1):
        # Gather CPU percentages list, given a specified interval
        percent = psutil.cpu_percent(interval=config.DUMMYMP_MINTERVAL[config.DUMMYMP_MODE], percpu=True)
        
        # If the current avg array is empty...
        if len(avg) == 0:
            # ...just copy the current percent list over.
            avg = percent
        else:
            # Otherwise, average them together!
            for n in xrange(0, len(percent)):
                avg[n] = (avg[n] + percent[n]) / 2
    
    # Threshold
    avail_cpus_arr = []
    for n in xrange(0, len(percent)):
        # If CPU percentage meets the specified thresold, add a True.
        if avg[n] < config.DUMMYMP_THRESHOLD[config.DUMMYMP_MODE]:
            avail_cpus_arr.append(True)
        else:
            avail_cpus_arr.append(False)
    
    # Count the number of [True]s!
    available_num_cpus = avail_cpus_arr.count(True)
    logging.debug("%i / %i CPUs available!" % (available_num_cpus, ncpus))
    
    # If the number of processes running isn't zero, compute difference
    # and update CPU availability.
    cur_running = checkProcRunning()
    
    if cur_running != 0:
        logging.debug("Entering alternative process mode...")
        
        # If no CPUs available, return the current number and wait for
        # process count to go down!
        if available_num_cpus == 0:
            return config.CPU_AVAIL
        
        # Theoretial empty slots = 
        #   Previous availability - Currently running procs
        empty_slots = config.CPU_AVAIL - cur_running
        
        logging.debug("Old setting: %i" % config.CPU_AVAIL)
        logging.debug("Cur running: %i" % cur_running)
        logging.debug("Cur running initial: %i" % cur_running_initial)
        
        logging.debug("Empty slots: %i" % empty_slots)
        
        # Correction
        # if cur_running != cur_running_initial:
        #     logging.debug("Correction needed!")
        #     if cur_running < cur_running_initial:
        #         logging.debug("Correction: +++ %i" % (cur_running_initial - cur_running))
        #         empty_slots += (cur_running_initial - cur_running)
        #     else:
        #         logging.debug("Correction: --- %i" % (cur_running - cur_running_initial))
        #         empty_slots -= (cur_running - cur_running_initial)
        #     logging.debug("New empty slots: %i" % empty_slots)
        
        # Validate against found result
        if available_num_cpus == empty_slots:
            logging.debug("Available CPUs == empty slots")
            available_num_cpus = config.CPU_AVAIL
        elif available_num_cpus > empty_slots:
            logging.debug("Available CPUs > empty slots")
            # Add difference
            available_num_cpus = config.CPU_AVAIL + (available_num_cpus - empty_slots)
            # SANITY CHECK
            if available_num_cpus > ncpus:
                logging.warn("Number of available CPUs greater than the total number of CPUs! Capping.")
                available_num_cpus = ncpus
            logging.debug("Available CPUs now set to: %i" % available_num_cpus)
        else:
            # <
            logging.debug("Available CPUs < empty slots")
            available_num_cpus = config.CPU_AVAIL - (empty_slots - available_num_cpus)
            # SANITY CHECK
            if available_num_cpus < 0:
                logging.warn("Number of available CPUs is less than zero! Fixing.")
                available_num_cpus = 0
            logging.debug("Available CPUs now set to: %i" % available_num_cpus)
        
        logging.debug("Updated CPU availability - %i / %i CPUs available!" % (available_num_cpus, ncpus))
    
    # Update state
    config.CPU_AVAIL = available_num_cpus
    config.LAST_CPU_CHECK = datetime.datetime.now()
    
    # Return number of CPUs available!
    return available_num_cpus
