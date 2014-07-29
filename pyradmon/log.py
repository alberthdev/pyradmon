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
# Logging Library -
#   library for logging everything
# 
import logging

# Set things up
global logger, has_init
has_init = False
logger = logging.getLogger()

# FUNCTION:
#     init()
#         Initialize logging for general use.
#     ARGUMENTS:
#         None
#     RETURNS:
#         None
# TODO:
#     Maybe add returns when log can't be written to?
#     Add additional logging options?
def init(loglevel=logging.DEBUG, logstream=None, logpath=None):
    global logger, has_init
    logger.setLevel(loglevel)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        '%m/%d/%Y %I:%M:%S %p'
        )
    
    if (not logpath) and (not logstream):
        # Disable logging entirely
        logger.disabled = True
        logger.propagate = False
    
    # Check to see if a file path is defined.
    if logpath:
        fh = logging.FileHandler(logpath)
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    # Check to see if a stream type (like sys.stdout/sys.stderr) is
    # defined.
    if logstream and type(logstream) == list:
        for logstr in logstream:
            if type(logstr) == file:
                sh = logging.StreamHandler(logstr)
                sh.setLevel(loglevel)
                sh.setFormatter(formatter)
                logger.addHandler(sh)
    else:
        if type(logstream) == file:
            sh = logging.StreamHandler(logstream)
            sh.setLevel(loglevel)
            sh.setFormatter(formatter)
            logger.addHandler(sh)
    
    has_init = True
    
    # Old statement:
    #logging.basicConfig(filename=logpath,
    #	level=loglevel,
    # 	format='[%(asctime)s] [%(levelname)s] %(message)s',
    #	datefmt='%m/%d/%Y %I:%M:%S %p'
    #	)

def check_init():
    global has_init
    return has_init

