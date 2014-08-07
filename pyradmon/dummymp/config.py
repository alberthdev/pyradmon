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
# DummyMP Library - Internal Configuration
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import datetime
import psutil

#######################################################################
# Constants
#######################################################################

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

# Interval to refresh CPU usage measurement
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

# Queue IDs
DUMMYMP_LOG_ID = 1
DUMMYMP_RET_ID = 2

# Deepcopy Flags
DUMMYMP_ARGS_DEEPCOPY = True
DUMMYMP_KWARGS_DEEPCOPY = True

#######################################################################
# State Variables
#######################################################################

# Queues, processes, process queue, returns
global dummymp_queues, dummymp_procs, dummymp_start_procs, dummymp_rets
dummymp_queues = []
dummymp_procs = []
dummymp_start_procs = []
dummymp_rets = {}

# Counters for processes
global total_procs, total_completed, total_running
total_procs = 0
total_completed = 0
total_running = 0

# Max processes configuration
global max_processes
max_processes = 0

# Current job running mode
global DUMMYMP_MODE
DUMMYMP_MODE = DUMMYMP_NORMAL

# CPU availability, and checking interval threshold
global CPU_AVAIL, LAST_CPU_CHECK, CPU_CHECK_TIMEDELTA_THRESHOLD
CPU_AVAIL = psutil.cpu_count()
LAST_CPU_CHECK = datetime.datetime(1900, 1, 1)

# If not NUCLEAR, make a threshold. If NUCLEAR, don't.
if DUMMYMP_MODE != DUMMYMP_NUCLEAR:
    CPU_CHECK_TIMEDELTA_THRESHOLD = datetime.timedelta(seconds=DUMMYMP_MREFRESH[DUMMYMP_MODE])
else:
    CPU_CHECK_TIMEDELTA_THRESHOLD = None

# Process callbacks
global PROCESS_START_CALLBACK, PROCESS_END_CALLBACK
PROCESS_START_CALLBACK = None
PROCESS_END_CALLBACK = None
