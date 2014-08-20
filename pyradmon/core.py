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
# Core Library -
#   library for misc functions
# 

try:
    import termios, fcntl
    KEYPRESS_ENABLED = True
except:
    KEYPRESS_ENABLED = False
    
import traceback
import logging

import time
import os
import sys
import errno

import types

try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        print "ERROR: OrderedDict not found! It is required to run this script."
        sys.exit(1)

def isset(key, thedict):
    if key in thedict:
        if thedict[key] != None:
            return True
    return False

def isset_obj(key, theobj):
    if hasattr(theobj, key):
        if getattr(theobj, key) != None:
            return True
    return False

def isgen(gen):
    return isinstance(gen, types.GeneratorType)

def get_key_press():
    if KEYPRESS_ENABLED:
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            sys.stdout.write("[Press any key to continue...]")
            sys.stdout.flush()
            while 1:
                try:
                    c = sys.stdin.read(1)
                    
                    #print "Got character", repr(c)
                    break
                except IOError: pass
        except KeyboardInterrupt:
            sys.stdout.write(len("[Press any key to continue...]") * "\b" + \
                        len("[Press any key to continue...]") * " " + \
                        len("[Press any key to continue...]") * "\b")
            sys.stdout.flush()
            print "CTRL-C detected, exiting.\n"
            sys.exit(0)
        finally:
            sys.stdout.write(len("[Press any key to continue...]") * "\b" + \
                        len("[Press any key to continue...]") * " " + \
                        len("[Press any key to continue...]") * "\b")
            sys.stdout.flush()
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    else:
        raw_input("[Press ENTER to continue...]")

def sortOD(od):
    res = OrderedDict()
    for k, v in sorted(od.items()):
        if isinstance(v, dict):
            res[k] = sortOD(v)
        else:
            res[k] = v
    return res

def sortODShallow(od):
    res = OrderedDict()
    for k, v in sorted(od.items()):
        res[k] = v
    return res

def die(reason):
    logging.critical(reason)
    sys.exit(1)

def edie(reason):
    logging.critical(reason)
    raise Exception(reason)

def critical(c):
    logging.critical(c)

def error(err):
    logging.error(err)

def exception(err):
    logging.exception(err)

def warn(w):
    logging.warning(w)

def info(i):
    logging.info(i)

def debug(d):
    logging.debug(d)

def pprinter(obj):
    import pprint
    pprint.pprint(obj)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# Recurisve unset
def delete_keys_from_dict(dict_del, lst_keys):
    if type(lst_keys) == list:
        for lst in lst_keys:
            if type(lst) == list:
                if len(lst) > 1:
                    d_ptr = dict_del
                    for k in lst[:-1]:
                        d_ptr = d_ptr[k]
                    d_ptr.pop(lst[-1], None)
                else:
                    dict_del.pop(lst[0], None)
            else:
                dict_del.pop(lst, None)
    else:
        dict_del.pop(lst_keys, None)
    return dict_del

# Math func
def mode(list):
    d = {}
    for elm in list:
        try:
            d[elm] += 1
        except(KeyError):
            d[elm] = 1
    
    keys = d.keys()
    max = d[keys[0]]
    
    for key in keys[1:]:
        if d[key] > max:
            max = d[key]
    
    max_k = []
    for key in keys:
        if d[key] == max:
            max_k.append(key),
    return max_k,max

def check_file(file_path):
    if not os.path.isfile(file_path):
        return False
    
    # Try opening the file, just to make sure!
    try:
        fh = open(file_path, "r")
        fh.close()
    except IOError:
        return False
    except:
        print "ERROR: Strange magic occurred when trying to check to see if a file"
        print "exists! File: %s" % file_path
        import traceback
        traceback.format_exc()
    
    return True

def identicalEleListCheck(lst):
    return not lst or lst.count(lst[0]) == len(lst)

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()
