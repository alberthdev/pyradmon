#!/usr/bin/env python
# PyRadmon v1.0 - Python Radience Monitor Tool
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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# DictR Library -
#   library for dynamic recursive dict value getting and setting
# 
# Dynamic recursive dictionary values:
#   Normally, you can access a dict within a dict via:
#     mydict[key1][key2]
#   An example with more levels:
#     mydict[key1][key2][key3]
#   However, what if the dictionary was N levels deep, and you only
#   want to access X levels? What if you wanted to specify different
#   keys? Using the above syntax wouldn't work.
#   Hence: getr() and setr()!
# 

def getr(thedict, key_arr):
    """Fetches the value of a recursive dict given the recursive key.

    Retrieves a recursive dict value given an array describing the
    recursive key.

    Args:
        thedict: A dictionary.
        key_arr: A list of strings that as a whole represent the
            recursive key you wish to retrieve. For instance, to
            retrieve some_dict[key1][key2][key3], key_arr should be
            [key1, key2, key3], in order.

    Returns:
        The corresponding value of the recursive key.

    Raises:
        KeyError: The recursive key specified in key_arr does not
            exist.
    """
    this_dict = thedict
    key_index = 0
    break_index = len(key_arr) - 1
    while 1:
        found = False
        key = key_arr[key_index]
        if key in this_dict:
            this_dict = this_dict[key]
            found = True
    
        if key_index == break_index:
            break
        else:
            if found:
                key_index += 1
            else:
                break
    if found:
        return this_dict
    else:
        raise KeyError("[%s]" % (", ".join([str(x) for x in key_arr])))

def setr(thedict, key_arr, val):
    """Sets the value of a recursive dict given the recursive key and
    the desired value.

    Sets a recursive dict value given an array describing the
    recursive key and the desired value.

    Args:
        thedict: A dictionary.
        key_arr: A list of strings that as a whole represent the
            recursive key you wish to retrieve. For instance, to
            retrieve some_dict[key1][key2][key3], key_arr should be
            [key1, key2, key3], in order.
        val: The desired value to set.

    Returns:
        None

    Raises:
        KeyError: The recursive key specified in key_arr does not
            exist. This will be raised by getr().
    """
    
    # How does this work? We grab the dict by removing the last key
    # from key_arr, and then set it directly with dict syntax from last key.
    
    getr(thedict, key_arr[:-1])[key_arr[-1]] = val

def findKeys(thedict, keys):
    """Determines the existence of a recursive key in a recursive
    dict.

    Searches and determines the existence of a recursive key in a
    recursive dict, given the recursive dict and the recursive key to
    search for.

    Args:
        thedict: A dictionary.
        keys: A list of strings that as a whole represent the
            recursive key you wish to retrieve. For instance, to
            retrieve some_dict[key1][key2][key3], key_arr should be
            [key1, key2, key3], in order.

    Returns:
        A bool indicating whether the recursive key was successfully
        found (exists) or not.
        
        True  - recursive key exists (and search succeeded)
        False - recursive key does NOT exist (and search failed)

    Raises:
        None
    """
    try:
        getr(thedict, keys)
        return True
    except:
        return False
