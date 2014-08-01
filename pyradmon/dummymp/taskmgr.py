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
# DummyMP Library - Task Manager
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import logging
import config
import time
from detect import *

def process_queue():
    """Process inter-process messages.
    
    Process the inter-process Queue objects, which receive messages from
    the spawned process for logging events and function returns.
    
    Args:
        None
    
    Raises:
        None, but warnings are emitted to log if an invalid message is
        received.
    """
    logger = logging.getLogger()
    for dummymp_queue in config.dummymp_queues:
        if not dummymp_queue.empty():
            qout = dummymp_queue.get(timeout = 0.001)
            
            if type(qout) != list:
                logger.warning("WARNING: Received invalid message from process! This may be a bug! Message: %s" % str(qout))
                continue
            
            # Format: [ [ DUMMYMP_MSG_TYPE_ID, SYSTEM_PID, INTERNAL_ID ], DATA... ]
            if qout[0][0] == config.DUMMYMP_LOG_ID:
                # Append PID info
                qout[1].msg = ("[PID %i] " % qout[0][1]) + qout[1].msg
                logger.handle(qout[1])
            elif qout[0][0] == config.DUMMYMP_RET_ID:
                config.dummymp_rets[qout[0][2]] = qout[1]
            else:
                logger.warning("WARNING: Received invalid message from process! (Invalid message type ID!) This may be a bug! Message: %s" % str(qout))

def process_process():
    """Process the execution queue and inter-process messages.
    
    Process the execution queue by starting processes in said queue,
    handle processes that have completed, and process inter-process
    messages via process_queue(). (In plain English: start the queued
    processes, check processes to see if they are done running, and grab
    any inter-process messages sent from the spawned process.)
    
    Args:
        None
    
    Returns:
        A boolean indicating whether the execution queue has completed
        or not. Returns True if it has completed, False if it has not.
        This return value can be used in a while loop to block until
        processes have completed. (This is somewhat similar to
        multiprocessing's join().)
    """
    nproc = 0
    while nproc < len(config.dummymp_procs):
        dummymp_proc = config.dummymp_procs[nproc]
        
        if (not dummymp_proc in config.dummymp_start_procs) and (not dummymp_proc.is_alive()):
            process_queue()
            pi = config.dummymp_procs.index(dummymp_proc)
            config.dummymp_queues.pop(pi)
            config.dummymp_procs.pop(pi)
            logging.debug("Process complete!")
            
            config.total_completed += 1
            config.total_running -= 1
            
            if config.PROCESS_END_CALLBACK:
                config.PROCESS_END_CALLBACK(config.total_completed, config.total_running, config.total_procs)
            
            nproc -= 1
        
        nproc += 1
    
    avail_cpus = getCPUAvail()
    #print "PROCS:", dummymp_start_procs
    
    nproc = 0
    while nproc < len(config.dummymp_start_procs):
        dummymp_proc = config.dummymp_start_procs[nproc]
        
        if (config.max_processes == 0) or (config.total_running < config.max_processes):
            if ((avail_cpus == 0) and (config.total_running == 0) and (config.DUMMYMP_MODE != config.DUMMYMP_GENEROUS)):
                avail_cpus += 1
                logging.debug("Not in generous mode, so forcing one task to run.")
            
            if avail_cpus > 0:
                logging.debug("%i CPUs available, spawning process!" % avail_cpus)
                avail_cpus -= 1
                dummymp_proc.start()
                config.dummymp_start_procs.remove(dummymp_proc)
                
                config.total_running += 1
                
                if config.PROCESS_START_CALLBACK:
                    config.PROCESS_START_CALLBACK(config.total_completed, config.total_running, config.total_procs)
                
                nproc -= 1
        else:
            logging.debug("Max processes limit of %i reached, waiting for process to terminate." % config.max_processes)
        
        nproc += 1
    
    if len(config.dummymp_procs) == 0:
        logging.debug("All processes complete, returning True.")
        return True
    return False

def process_until_done():
    """Process the execution queue until all have been completed.
    
    Process the execution queue until it has indicated that all
    processes in the queue have been completed. (This is somewhat
    similar to multiprocessing's join().)
    
    Args:
        None
    """
    while not process_process():
        process_queue()
        time.sleep(0.001)
