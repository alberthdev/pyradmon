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
# Data File Enumeration Library -
#   library for enumerating all of the applicable data files in a
#   directory, given certain conditions
# 

import os
import sys

from dictr import *
from core import *

import datetime

import re

# Variables to determine what to look for!
# These are the default variables - the actual variables can be
# changed with the call to enumerate().
DATA_PATH_FORMAT  = "MERRA2/%EXPERIMENT_ID%/obs/Y%YEAR4%/M%MONTH2%/D%DAY2%/H%HOUR2%/%EXPERIMENT_ID%.diag_%INSTRUMENT_SAT%_%DATA_TYPE%.%YEAR4%%MONTH2%%DAY2%_%HOUR2%z.txt"
EXPERIMENT_ID     = "d5124_m2_jan91"
START_YEAR        = "1991"
START_MONTH       = "01"
START_DAY         = "01"
START_HOUR        = "00"
END_YEAR          = "1991"
END_MONTH         = "02"
END_DAY           = "28"
END_HOUR          = "18"
INSTRUMENT_SAT    = "ssmi_f08"
DATA_TYPE         = "anl|ges"

# Ignore warnings?
ALLOW_WARN_PASS    = True

def make_subst_variable(year, month, day, hour, experiment_id, instrument_sat, data_type):
    syear  = str(year).zfill(2)
    smonth = str(month).zfill(2)
    sday   = str(day).zfill(2)
    shour  = str(hour).zfill(2)
    
    # Quick sanity check
    if (len(syear) != 4) or (len(smonth) != 2) or (len(sday) != 2) or (len(shour) != 2):
        print "ERROR: Date is invalid!"
        sys.exit(1)
    
    subst_var = {}
    
    subst_var["YEAR"]  = syear
    subst_var["YEAR4"] = syear
    subst_var["YEAR2"] = syear[2:]
    
    subst_var["MONTH"]  = smonth
    subst_var["MONTH2"] = smonth
    
    subst_var["DAY"]  = sday
    subst_var["DAY2"] = sday
    
    subst_var["HOUR"]  = shour
    subst_var["HOUR2"] = shour
    
    subst_var["EXPERIMENT_ID"] = experiment_id
    
    subst_var["INSTRUMENT_SAT"] = instrument_sat
    
    subst_var["DATA_TYPE"] = data_type
    
    return subst_var

def path_substitute(path_format, variables):
    final_path = path_format
    for variable in variables:
        var_re = re.compile(re.escape('%' + variable + '%'), re.IGNORECASE)
        final_path = var_re.sub(variables[variable], final_path)
    return final_path

def enumerate(**opts):
    """Returns a list of files that matches the given search range.

    Searches a given folder and returns a list of files that matches
    the given search range.
    
    Arguments are keywords arguments; some, none, or all of them may
    be specified. For arguments not specified, the default capital
    letter version of the variable will be used instead. See the
    source file (enumerate.py) for capital variable defaults.

    Args:
        base_directory=: The base directory where the data files are
            located, indicated as a string.
        experiment_id=: The experiment ID, indicated as a string.
        start_year=: The start year, indicated as a string.
        start_month=: The start month, indicated as a string.
        start_day=: The start day, indicated as a string.
        start_hour=: The start hour, indicated as a string.
        end_year=: The end year, indicated as a string.
        end_month=: The end month, indicated as a string.
        end_day=: The end day, indicated as a string.
        end_hour=: The end hour, indicated as a string
        instrument_sat=: Instrument satellite, indicated as a string or
            array of strings.
        data_type=: "anl", "ges", or "anl|ges" string to indicate
            analyzed or guessed data.
        time_delta=: datetime.timedelta object to increment the date
            with. Default is one hour.
        allow_warn_pass=: boolean to determine whether to ignore
            warnings or halt if a warning is found.
        
        For all variables except time_delta, the default value is the
        capitalized global variable version specified in this file.
        
    Returns:
        A list with the list of file dicts that matches the given
        search range. Each file is returned as a dictionary, with
        'instrument_sat' and 'type' of the file specified in the dict,
        along with the file name 'filename'.

    Raises:
        Exception(...) - error exception when either:
            - the directory specified does not exist
            - file validation failed and ALLOW_WARN_PASS is False
    """
    # Depending on the inputs, assign variables to input or defaults!
    data_path_format = opts["data_path_format"] if "data_path_format" in opts \
        else DATA_PATH_FORMAT
    
    experiment_id = opts["experiment_id"] if "experiment_id" in opts \
        else EXPERIMENT_ID
    
    start_year = opts["start_year"] if "start_year" in opts \
        else START_YEAR
    
    start_month = opts["start_month"] if "start_month" in opts \
        else START_MONTH
    
    start_day = opts["start_day"] if "start_day" in opts \
        else START_DAY
    
    start_hour = opts["start_hour"] if "start_hour" in opts \
        else START_HOUR
    
    end_year = opts["end_year"] if "end_year" in opts \
        else END_YEAR
    
    end_month = opts["end_month"] if "end_month" in opts \
        else END_MONTH
    
    end_day = opts["end_day"] if "end_day" in opts \
        else END_DAY
    
    end_hour = opts["end_hour"] if "end_hour" in opts \
        else END_HOUR
    
    instrument_sat = opts["instrument_sat"] if "instrument_sat" in opts \
        else INSTRUMENT_SAT
    
    data_type = opts["data_type"] if "data_type" in opts \
        else DATA_TYPE
    
    time_delta = opts["time_delta"] if "time_delta" in opts \
        else None
    
    if data_type:
        if len(data_type.split('|')) > 1:
            data_type = data_type.split('|')
        else:
            data_type = [ data_type ]
    else:
        data_type = [ "" ]
    
    
    allow_warn_pass = opts["allow_warn_pass"] if "allow_warn_pass" in opts \
        else ALLOW_WARN_PASS
    
    # Make reference datetimes
    cur_date = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour))
    end_date = datetime.datetime(int(end_year), int(end_month), int(end_day), int(end_hour))
    
    old_month = 0
    old_year = 0
    
    found_correct_range = False
    
    year_re = re.compile(r'^Y\d{4}$')
    month_re = re.compile(r'^M\d{2}$')
    day_re = re.compile(r'^D\d{2}$')
    hour_re = re.compile(r'^H\d{2}$')
    
    # Now loop and generate a list of files to read!
    files_to_read = []
    
    # Data vars
    available_instrument_sat = []
    available_data_type = []
    interval_count = 0
    interval_measurements = 0
    
    total_files = 0
    criteria_total_files = 0
    
    average_interval = 0
    
    if time_delta:
        info("Using custom delta for file enumeration.")
    
    while 1:
        if (cur_date <= end_date):
            # Rebuild formatted parts
            syear  = str(cur_date.year).zfill(2)
            smonth = str(cur_date.month).zfill(2)
            sday   = str(cur_date.day).zfill(2)
            shour  = str(cur_date.hour).zfill(2)
            
            for indv_data_type in data_type:
                subs_var = make_subst_variable(syear, smonth, sday, shour, experiment_id, instrument_sat, indv_data_type)
                
                file_path = path_substitute(data_path_format, subs_var)
                
                if check_file(file_path):
                    # Success! Calculate the interval average!
                    average_interval = ((average_interval * interval_measurements) + interval_count) / (interval_measurements + 1)
                    
                    # Reset interval count and increment measurement count.
                    interval_count = 0
                    interval_measurements += 1
                    
                    # Add new entry
                    newdatdict = { "instrument_sat" : instrument_sat, "type" : indv_data_type, "filename" : file_path, "date" : cur_date }
                    
                    # BUGFIX: If using minutes or less, this will cause duplicate entries.
                    # Check to make sure we're not adding dups!
                    
                    if not newdatdict in files_to_read:
                        files_to_read.append(newdatdict)
                    
                    if not instrument_sat in available_instrument_sat:
                        available_instrument_sat.append(instrument_sat)
                    
                    if not indv_data_type in available_data_type:
                        available_data_type.append(indv_data_type)
                        
                    criteria_total_files += 1
                    total_files += 1
                else:
                    interval_count += 1
                    pass
                
            # Increment time
            if time_delta:
                cur_date = cur_date + time_delta
            else:
                cur_date = cur_date + datetime.timedelta(hours=1)
        else:
            break
    
    stats_dict = {}
    stats_dict["start_year"]               = int(start_year)
    stats_dict["start_month"]              = int(start_month)
    stats_dict["start_day"]                = int(start_day)
    stats_dict["start_hour"]               = int(start_hour)
                                           
    stats_dict["end_year"]                 = int(end_year)
    stats_dict["end_month"]                = int(end_month)
    stats_dict["end_day"]                  = int(end_day)
    stats_dict["end_hour"]                 = int(end_hour)
    
    stats_dict["available_instrument_sat"] = available_instrument_sat
    stats_dict["available_data_type"]      = available_data_type
    stats_dict["average_interval"]         = average_interval
    
    stats_dict["total_files"]              = total_files
    stats_dict["criteria_total_files"]     = criteria_total_files
    
    # Done!
    return (files_to_read, stats_dict)

if __name__ == "__main__":
    import pprint
    pprint.pprint(enumerate())
