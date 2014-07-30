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
from multiprocessing import Process, Queue
import logging
import psutil
import datetime
import os
import sys
import time

global __version__
__version__ = "0.5a1"

global dummymp_queues, dummymp_procs, dummymp_start_procs
dummymp_queues = []
dummymp_procs = []
dummymp_start_procs = []

global total_procs, total_completed, total_running
total_procs = 0
total_completed = 0
total_running = 0

global max_processes
max_processes = 0

# Job running modes
DUMMYMP_GENEROUS    = -1
DUMMYMP_NORMAL      = -2
DUMMYMP_AGGRESSIVE  = -3
DUMMYMP_EXTREME     = -4
DUMMYMP_NUCLEAR     = -9999

# CPU Thresholds
DUMMYMP_THRESHOLD = {
                        DUMMYMP_GENEROUS    : 20,
                        DUMMYMP_NORMAL      : 30,
                        DUMMYMP_AGGRESSIVE  : 50,
                        DUMMYMP_EXTREME     : 80,
                        DUMMYMP_NUCLEAR     : float("inf"),
                    }

# CPU Usage Measurement Intervals
DUMMYMP_MINTERVAL = {
                        DUMMYMP_GENEROUS    : 0.5,
                        DUMMYMP_NORMAL      : 0.35,
                        DUMMYMP_AGGRESSIVE  : 0.2,
                        DUMMYMP_EXTREME     : 0.1,
                        DUMMYMP_NUCLEAR     : 0.1,
                    }

# CPU Usage Measurement Cycles
DUMMYMP_MCYCLE = {
                        DUMMYMP_GENEROUS    : 3,
                        DUMMYMP_NORMAL      : 2,
                        DUMMYMP_AGGRESSIVE  : 2,
                        DUMMYMP_EXTREME     : 1,
                        DUMMYMP_NUCLEAR     : 0,
                 }

DUMMYMP_MREFRESH = {
                        DUMMYMP_GENEROUS    : 5,
                        DUMMYMP_NORMAL      : 10,
                        DUMMYMP_AGGRESSIVE  : 20,
                        DUMMYMP_EXTREME     : 30,
                        DUMMYMP_NUCLEAR     : False,
                   }

# String versions of modes
DUMMYMP_STRING = {
                        DUMMYMP_GENEROUS    : "Generous",
                        DUMMYMP_NORMAL      : "Normal",
                        DUMMYMP_AGGRESSIVE  : "Aggressive",
                        DUMMYMP_EXTREME     : "Extreme",
                        DUMMYMP_NUCLEAR     : "Nuclear",
                 }

DUMMYMP_STDOUT_ID = 30
DUMMYMP_STDERR_ID = 31

ORIGINAL_STDOUT = sys.stdout
ORIGINAL_STDERR = sys.stderr

# Current job running mode
global DUMMYMP_MODE
DUMMYMP_MODE = DUMMYMP_NUCLEAR

global CPU_AVAIL, LAST_CPU_CHECK, CPU_CHECK_TIMEDELTA_THRESHOLD
CPU_AVAIL = psutil.cpu_count()
LAST_CPU_CHECK = datetime.datetime(1900, 1, 1)

if DUMMYMP_MODE != DUMMYMP_NUCLEAR:
    CPU_CHECK_TIMEDELTA_THRESHOLD = datetime.timedelta(seconds=DUMMYMP_MREFRESH[DUMMYMP_MODE])
else:
    CPU_CHECK_TIMEDELTA_THRESHOLD = None

# Process callbacks
global PROCESS_START_CALLBACK, PROCESS_END_CALLBACK
PROCESS_START_CALLBACK = None
PROCESS_END_CALLBACK = None

class DummyMPLogHandler(logging.Handler):
    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue
    
    def emit(self, record):
        try:
            # Format: [ [queueMsgID, PID], record ]
            self.queue.put([[1, os.getpid()], record])
        except:
            self.handleError(record)

class DummyMPStringQueue(object):
    def __init__(self, queue, qid, data = None):
        self.l_buffer = []
        self.s_buffer = ""
        
        self.queue = queue
        self.qid = qid
        
        if data:
            self.write(data)

    def write(self, data):
        #check type here, as wrong data type will cause error on self.read,
        #which may be confusing.
        if type(data) != type(""):
            raise TypeError, "argument 1 must be string, not %s" % type(data).__name__
        #append data to list, no need to "".join just yet.
        self.l_buffer.append(data)
        self.push_read()

    def _build_str(self):
        #build a new string out of list
        new_string = "".join(self.l_buffer)
        #join string buffer and new string
        self.s_buffer = "".join((self.s_buffer, new_string))
        #clear list
        self.l_buffer = []

    def __len__(self):
        #calculate length without needing to _build_str
        return sum(len(i) for i in self.l_buffer) + len(self.s_buffer)

    def push_read(self):
        #if string doesnt have enough chars to satisfy caller, or caller is
        #requesting all data
        if count > len(self.s_buffer) or count==None: self._build_str()
        #if i don't have enough bytes to satisfy caller, return nothing.
        if count > len(self.s_buffer): return ""
        #get data requested by caller
        result = self.s_buffer[:count]
        #remove requested data from string buffer
        self.s_buffer = self.s_buffer[len(result):]
        
        self.queue.put([ [self.qid, os.getpid()], result])


def _runner(func, dummymp_queue, *args):
    # Switch out the logging handler...
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    hdlrs = logger.handlers
    for hdlr in hdlrs:
        logger.removeHandler(hdlr)
    
    dmp_handler = DummyMPLogHandler(dummymp_queue)
    
    logger.addHandler(dmp_handler)
    
    # Call the function!
    func(*args)

def set_max_processes(max_proc):
    global max_processes
    max_processes = max_proc

def get_max_processes():
    global max_processes
    return max_processes

def set_priority_mode(mode):
    global DUMMYMP_MODE
    DUMMYMP_MODE = mode

def get_priority_mode():
    global DUMMYMP_MODE
    return DUMMYMP_MODE

def get_version():
    global __version__
    return __version__

def run(func, args):
    global dummymp_queues, dummymp_procs, dummymp_start_procs
    global total_procs
    q = Queue()
    
    # Backup sys.stdout, sys.stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Set them to our new queue based object!
    #sys.stdout = DummyMPStringQueue(q, DUMMYMP_STDOUT_ID)
    #sys.stderr = DummyMPStringQueue(q, DUMMYMP_STDERR_ID)
    
    final_args = map(list, args)
    final_args.insert(0, q)
    final_args.insert(0, func)
    p = Process(target = _runner, args = final_args)
    
    dummymp_queues.append(q)
    dummymp_procs.append(p)
    dummymp_start_procs.append(p)
    
    total_procs += 1

def process_queue():
    global dummymp_queues
    logger = logging.getLogger()
    for dummymp_queue in dummymp_queues:
        if not dummymp_queue.empty():
            qout = dummymp_queue.get(timeout = 0.001)
            if qout[0][0] == 1:
                # Append PID info
                qout[1].msg = ("[PID %i] " % qout[0][1]) + qout[1].msg
                logger.handle(qout[1])
            elif qout[0][0] == DUMMYMP_STDOUT_ID:
                ORIGINAL_STDOUT.write(qout[1])
                ORIGINAL_STDOUT.flush()
            elif qout[0][0] == DUMMYMP_STDERR_ID:
                ORIGINAL_STDERR.write(qout[1])
                ORIGINAL_STDERR.flush()

def process_process():
    global total_procs, total_completed, total_running
    global PROCESS_START_CALLBACK, PROCESS_END_CALLBACK
    global dummymp_procs, dummymp_start_procs
    global max_processes
    nproc = 0
    while nproc < len(dummymp_procs):
        dummymp_proc = dummymp_procs[nproc]
        
        if (not dummymp_proc in dummymp_start_procs) and (not dummymp_proc.is_alive()):
            process_queue()
            pi = dummymp_procs.index(dummymp_proc)
            dummymp_queues.pop(pi)
            dummymp_procs.pop(pi)
            logging.debug("Process complete!")
            
            total_completed += 1
            total_running -= 1
            
            if PROCESS_END_CALLBACK:
                PROCESS_END_CALLBACK(total_completed, total_running, total_procs)
            
            nproc -= 1
        
        nproc += 1
    
    avail_cpus = getCPUAvail()
    #print "PROCS:", dummymp_start_procs
    
    nproc = 0
    while nproc < len(dummymp_start_procs):
        dummymp_proc = dummymp_start_procs[nproc]
        
        if (max_processes == 0) or (total_running < max_processes):
            if avail_cpus > 0:
                logging.debug("%i CPUs available, spawning process!" % avail_cpus)
                avail_cpus -= 1
                dummymp_proc.start()
                dummymp_start_procs.remove(dummymp_proc)
                
                total_running += 1
                
                if PROCESS_START_CALLBACK:
                    PROCESS_START_CALLBACK(total_running)
                
                nproc -= 1
        else:
            logging.debug("Max processes limit of %i reached, waiting for process to terminate." % max_processes)
        
        nproc += 1
    
    if len(dummymp_procs) == 0:
        logging.debug("All processes complete, returning True.")
        return False
    return True

def getCPUAvail():
    global DUMMYMP_MODE
    global CPU_AVAIL, LAST_CPU_CHECK, CPU_CHECK_TIMEDELTA_THRESHOLD
    
    logging.debug("Querying CPUs (%s mode)..." % (DUMMYMP_STRING[DUMMYMP_MODE]))
    
    if (DUMMYMP_MODE == DUMMYMP_NUCLEAR) or (datetime.datetime.now() - LAST_CPU_CHECK <= CPU_CHECK_TIMEDELTA_THRESHOLD):
        return CPU_AVAIL
    
    ncpus = psutil.cpu_count()
    avg = []
    
    for i in xrange(0, DUMMYMP_MCYCLE[DUMMYMP_MODE] - 1):
        percent = psutil.cpu_percent(interval=DUMMYMP_MINTERVAL[DUMMYMP_MODE], percpu=True)
        
        if len(avg) == 0:
            avg = percent
        else:
            for n in xrange(0, len(percent)):
                avg[n] = (avg[n] + percent[n]) / 2
    
    # Threshold
    avail_cpus_arr = []
    for n in xrange(0, len(percent)):
        if avg[n] < DUMMYMP_THRESHOLD[DUMMYMP_MODE]:
            avail_cpus_arr.append(True)
        else:
            avail_cpus_arr.append(False)
    
    available_num_cpus = avail_cpus_arr.count(True)
    logging.debug("%i / %i CPUs available!" % (available_num_cpus, ncpus))
    
    CPU_AVAIL = available_num_cpus
    return available_num_cpus

def process_until_done():
    while process_process():
        process_queue()
        time.sleep(0.001)

def test():
    #print "Hello"
    for i in xrange(0, 10000000):
        pass
    #print logging.getLogger().handlers
    logging.info("Hi there from logging!")
    num = random.randint(2,7)
    logging.info("Sleeping for %i secs..." % num)
    time.sleep(num)
    logging.info("Bye bye from logging!")
    #print "Test"

if __name__ == "__main__":
    import random
    getCPUAvail()
    
    set_max_processes(2)
    
    run(test, [])
    run(test, [])
    run(test, [])
    
    process_until_done()
    
