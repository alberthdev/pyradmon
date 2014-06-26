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
                
# Variables to determine what to look for!
# These are the default variables - the actual variables can be
# changed with the call to enumerate().
BASE_DIRECTORY    = "MERRA2/"
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

def enumerate(**opts):
    """Returns a list of files that matches the given search range.

    Searches a given folder and returns a list of files that matches
    the given search range.
    
    Arguments are keywords arguments; some, none, or all of them may
    be specified. For arguments not specified, the default capital
    letter version of the variable will be used instead.

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
    base_directory = opts["base_directory"] if "base_directory" in opts \
        else BASE_DIRECTORY
    
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
    
    if len(data_type.split('|')) > 1:
        data_type = data_type.split('|')
    
    allow_warn_pass = opts["data_type"] if "allow_warn_pass" in opts \
        else ALLOW_WARN_PASS
    
    # Build the final data directory!
    data_dir = os.path.join(base_directory, experiment_id, "obs")
    
    # Initialize a data dictionary...
    data_dict = {}
    
    # Search for available data
    
    # Sanity check: does directory exist?
    if not os.path.isdir(data_dir):
        edie("ERROR: The directory specified does not exist!")
    
    # Make reference datetimes
    cur_date = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour))
    end_date = datetime.datetime(int(end_year), int(end_month), int(end_day), int(end_hour))
    
    old_month = 0
    old_year = 0
    
    # Iterate into directory recursively...
    for root, subfolder, files in os.walk(data_dir):
        # Split path into an array, minus the first few elements to
        # make it look like: ['Y1991', 'M01', 'D28', 'H06']
        dir_struct = root.split('/')[3:]
        
        # OPTIMIZATION - skip any data that doesn't match our timeframe!
        # Sanity check
        if len(dir_struct) != 4:
            #warn("Incomplete data set found - Y/M/D/H structure not complete! (dir_struct: %s)" % str(dir_struct))
            continue
        else:
            f_date = datetime.datetime(int(dir_struct[0][1:]), int(dir_struct[1][1:]), int(dir_struct[2][1:]), int(dir_struct[3][1:]))
            
            # If we are out of bounds, skip.
            ## TODO: maybe optimize with a flag so that when we find valid
            ## data, set the flag. When we get out of bounds, break.
            if not ((f_date >= cur_date) and (f_date <= end_date)):
                continue
            
            if (old_year != int(dir_struct[0][1:])) or (old_month != int(dir_struct[1][1:])):
                old_year  = int(dir_struct[0][1:])
                old_month = int(dir_struct[1][1:])
                info("Enumerating data for year %i, month %i..." % (int(dir_struct[0][1:], int(dir_struct[1][1:]))
        
        # Set up the recursive dict with the structure extracted,
        # aka dir_struct. Sort of like a "mkdir -p" - if it exists,
        # no worries. If it doesn't exist, it'll create it
        # automatically. It's like that, but in dict form.
        if not findKeys(data_dict, dir_struct):
            ele_list = []
            cur_dict = data_dict
            
            # Check from the left, top-most element to the right,
            # bottom-lower element.
            
            for ele in dir_struct:
                # Add element to the list
                ele_list.append(ele)
                # If it doesn't exist, create it!
                if not findKeys(cur_dict, ele_list):
                    cur_dict[ele_list[-1]] = {}
                # Recurse inwards
                cur_dict = cur_dict[ele_list[-1]]
                # Delete first element since we've cut a level from
                # the previous line
                ele_list = ele_list[1:]
        
        # Sanity check INSANITY
        for datfile in files:
            # Assume PASS is False (/guilty) until proven True (/innocent)
            PASS = False
            # Sanity check: validate timestamp on file matches folder timestamp
            ## TMP FIX - will need to add a config option for enumerating .bin OR .txt
            if datfile.endswith(".txt"):
                if datfile.startswith(experiment_id):
                    # Split the filename by periods
                    fn_split = datfile.split(".")
                    # Sanity check: validate that file starts with "diag_"
                    if fn_split[1].startswith("diag_"):
                        # Split the fields in the file name!
                        fn_split_split = fn_split[1].split("_")
                        # Sanity check: validate number of fields in filename
                        if len(fn_split_split) >= 3:
                            # Sanity check: validate if file type is ges,
                            # anl, or both...
                            # TODO: Make a list of valid types, and
                            # validate for existence of those types in 
                            # larger amounts
                            fn_ss_pipe_split = fn_split_split[-1].split("|")
                            if ( (fn_split_split[-1] == 'ges') or (fn_split_split[-1] == 'anl') ) \
                               or ( (len(fn_ss_pipe_split) == 2) and ("ges" in fn_ss_pipe_split) \
                                    and ("anl" in fn_ss_pipe_split) ):
                                # Sanity check: validate timestamp on file matches folder timestamp
                                if fn_split[2] == (dir_struct[0][1:] + dir_struct[1][1:] + dir_struct[2][1:] + "_" + dir_struct[3][1:] + "z"):
                                    # All good!
                                    PASS = True
                                else:
                                    warn("File validation failed - timestamp on file does not match folder!")
                            else:
                                warn("File validation failed - type of file is not 'ges' or 'anl'!")
                        else:
                            warn("File validation failed - too few fields in middle underscore (_) section!")
                    else:
                        warn("File validation failed - middle section does not start with diag_!")
                else:
                    warn("File validation failed - file does not start with EXPERIMENT_ID %s!" % experiment_id)
            
            # If file validation failed and ALLOW_WARN_PASS is set...
            #   OR
            # If file validation passes...
            if ((not PASS) and allow_warn_pass) or PASS:
                # ...build the final file dictionary.
                
                # Make sure that the dir dict value is a list.
                # If not, change it into one. (Usually, the recursive
                # code above makes it into a dict by default...)
                if type(getr(data_dict, dir_struct)) != list:
                    setr(data_dict, dir_struct, [])
                
                # Grab current array
                arr = getr(data_dict, dir_struct)
                
                # Build new dict
                dat_dict = {}
                dat_dict["instrument_sat"] = "_".join(fn_split_split[1:3])
                dat_dict["type"] = fn_split_split[-1]
                dat_dict["filename"] = datfile
                
                # Append to current array...
                arr.append(dat_dict)
                
                # ...and save it back to the dict!
                setr(data_dict, dir_struct, arr)
            else:
                edie("ERROR: File validation failed - see above for details.")
    
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
            syear = "Y" + str(cur_date.year).zfill(2)
            smonth = "M" + str(cur_date.month).zfill(2)
            sday = "D" + str(cur_date.day).zfill(2)
            shour = "H" + str(cur_date.hour).zfill(2)
            try:
                # Try to access it
                tmp_notmp = data_dict[syear][smonth][sday][shour]
                
                # Success! Calculate the interval average!
                average_interval = ((average_interval * interval_measurements) + interval_count) / (interval_measurements + 1)
                
                # Reset interval count and increment measurement count.
                interval_count = 0
                interval_measurements += 1
                
                for datdict in data_dict[syear][smonth][sday][shour]:
                    # Check if the variable is a string or a list. If 
                    # it's a string, match it. If it's a list, check to
                    # see if the search term is in the list.
                    # TODO: Perhaps write a function to handle this
                    # mess?!?
                    if ( ((type(instrument_sat) == str) and (datdict["instrument_sat"] == instrument_sat)) \
                       or ((type(instrument_sat) == list) and (datdict["instrument_sat"] in instrument_sat)) ) \
                      and \
                      ( ((type(data_type) == str) and (datdict["type"] == data_type)) \
                       or ((type(data_type) == list) and (datdict["type"] in data_type)) ):
                        # Get date timestamp
                        date_tag = datdict["filename"].split(".")[2]
                        # Check if timestamps match!
                        # 19910228_18z
                        if not ((int(date_tag[:4]) == cur_date.year) and \
                            (int(date_tag[4:6]) == cur_date.month) and \
                            (int(date_tag[6:8]) == cur_date.day) and \
                            (int(date_tag[-3:-1]) == cur_date.hour)):
                            warn("Timestamp on file does not match folder it is stored in!")
                        
                        # Add new entry
                        file_path = os.path.join(data_dir, syear, smonth, sday, shour, datdict["filename"])
                        newdatdict = { "instrument_sat" : datdict["instrument_sat"], "type" : datdict["type"], "filename" : file_path }
                        
                        # BUGFIX: If using minutes or less, this will cause duplicate entries.
                        # Check to make sure we're not adding dups!
                        
                        if not newdatdict in files_to_read:
                            files_to_read.append(newdatdict)
                        
                        if not datdict["instrument_sat"] in available_instrument_sat:
                            available_instrument_sat.append(datdict["instrument_sat"])
                        
                        if not datdict["type"] in available_data_type:
                            available_data_type.append(datdict["type"])
                            
                        criteria_total_files += 1
                    total_files += 1
            except KeyError:
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

def enumerate_all(**opts):
    """Returns a tuple with a list of files that matches the given
    criteria and a stats dictionary of the data found.

    Searches a given folder and returns a list of files that matches
    the given criteria.
    
    Arguments are keywords arguments; some, none, or all of them may
    be specified. For arguments not specified, the default capital
    letter version of the variable will be used instead.

    Args:
        REQUIRED:
        
        base_directory=: The base directory where the data files are
            located, indicated as a string.
        experiment_id=: The experiment ID, indicated as a string.
        
        Not required, but recommended:
        
        instrument_sat=: Instrument satellite, indicated as a string or
            array of strings.
        data_type=: "anl", "ges", or "anl|ges" string to indicate
            analyzed or guessed data.
        
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
    base_directory = opts["base_directory"] if "base_directory" in opts \
        else BASE_DIRECTORY
    
    experiment_id = opts["experiment_id"] if "experiment_id" in opts \
        else EXPERIMENT_ID
    
    instrument_sat = opts["instrument_sat"] if "instrument_sat" in opts \
        else None
    
    data_type = opts["data_type"] if "data_type" in opts \
        else None
    
    if len(data_type.split('|')) > 1:
        data_type = data_type.split('|')
    
    allow_warn_pass = opts["data_type"] if "allow_warn_pass" in opts \
        else ALLOW_WARN_PASS
    
    # Build the final data directory!
    data_dir = os.path.join(base_directory, experiment_id, "obs")
    
    # Initialize a data dictionary...
    data_dict = {}
    
    # Search for available data
    
    # Sanity check: does directory exist?
    if not os.path.isdir(data_dir):
        edie("ERROR: The directory specified does not exist!")
    
    # Iterate into directory recursively...
    for root, subfolder, files in os.walk(data_dir):
        # Split path into an array, minus the first few elements to
        # make it look like: ['Y1991', 'M01', 'D28', 'H06']
        dir_struct = root.split('/')[3:]
        
        # Set up the recursive dict with the structure extracted,
        # aka dir_struct. Sort of like a "mkdir -p" - if it exists,
        # no worries. If it doesn't exist, it'll create it
        # automatically. It's like that, but in dict form.
        if not findKeys(data_dict, dir_struct):
            ele_list = []
            cur_dict = data_dict
            
            # Check from the left, top-most element to the right,
            # bottom-lower element.
            
            for ele in dir_struct:
                # Add element to the list
                ele_list.append(ele)
                # If it doesn't exist, create it!
                if not findKeys(cur_dict, ele_list):
                    cur_dict[ele_list[-1]] = {}
                # Recurse inwards
                cur_dict = cur_dict[ele_list[-1]]
                # Delete first element since we've cut a level from
                # the previous line
                ele_list = ele_list[1:]
        
        # Sanity check INSANITY
        for datfile in files:
            # Assume PASS is False (/guilty) until proven True (/innocent)
            PASS = False
            # Sanity check: validate timestamp on file matches folder timestamp
            if datfile.startswith(experiment_id) and datfile.endswith(".txt"):
                # Split the filename by periods
                fn_split = datfile.split(".")
                # Sanity check: validate that file starts with "diag_"
                if fn_split[1].startswith("diag_"):
                    # Split the fields in the file name!
                    fn_split_split = fn_split[1].split("_")
                    # Sanity check: validate number of fields in filename
                    if len(fn_split_split) >= 3:
                        # Sanity check: validate if file type is ges,
                        # anl, or both...
                        # TODO: Make a list of valid types, and
                        # validate for existence of those types in 
                        # larger amounts
                        fn_ss_pipe_split = fn_split_split[-1].split("|")
                        if ( (fn_split_split[-1] == 'ges') or (fn_split_split[-1] == 'anl') ) \
                           or ( (len(fn_ss_pipe_split) == 2) and ("ges" in fn_ss_pipe_split) \
                                and ("anl" in fn_ss_pipe_split) ):
                            # Sanity check: validate timestamp on file matches folder timestamp
                            if fn_split[2] == (dir_struct[0][1:] + dir_struct[1][1:] + dir_struct[2][1:] + "_" + dir_struct[3][1:] + "z"):
                                # All good!
                                PASS = True
                            else:
                                warn("File validation failed - timestamp on file does not match folder!")
                        else:
                            warn("File validation failed - type of file is not 'ges' or 'anl'!")
                    else:
                        warn("File validation failed - too few fields in middle underscore (_) section!")
                else:
                    warn("File validation failed - middle section does not start with diag_!")
            else:
                warn("File validation failed - file does not start with EXPERIMENT_ID %s!" % experiment_id)
            
            # If file validation failed and ALLOW_WARN_PASS is set...
            #   OR
            # If file validation passes...
            if ((not PASS) and allow_warn_pass) or PASS:
                # ...build the final file dictionary.
                
                # Make sure that the dir dict value is a list.
                # If not, change it into one. (Usually, the recursive
                # code above makes it into a dict by default...)
                if type(getr(data_dict, dir_struct)) != list:
                    setr(data_dict, dir_struct, [])
                
                # Grab current array
                arr = getr(data_dict, dir_struct)
                
                # Build new dict
                dat_dict = {}
                dat_dict["instrument_sat"] = "_".join(fn_split_split[1:3])
                dat_dict["type"] = fn_split_split[-1]
                dat_dict["filename"] = datfile
                
                # Append to current array...
                arr.append(dat_dict)
                
                # ...and save it back to the dict!
                setr(data_dict, dir_struct, arr)
            else:
                edie("ERROR: File validation failed - see above for details.")
    
    ## OUTPUT VARIABLES
    # Now loop and generate a list of files to read!
    files_to_read = []
    
    # Make reference datetimes... by using min/max of the data!
    start_year      = min([ int(x[1:]) for x in data_dict.keys() ])
    start_year_str  = "Y" + str(start_year).zfill(4)
    
    start_month     = min([ int(x[1:]) for x in data_dict[start_year_str].keys() ])
    start_month_str = "M" + str(start_month).zfill(2)
    
    start_day       = min([ int(x[1:]) for x in data_dict[start_year_str][start_month_str].keys() ])
    start_day_str   = "D" + str(start_day).zfill(2)
    
    start_hour      = min([ int(x[1:]) for x in data_dict[start_year_str][start_month_str][start_day_str].keys() ])
    start_hour_str  = "H" + str(start_hour).zfill(2)
    
    end_year        = max([ int(x[1:]) for x in data_dict.keys() ])
    end_year_str    = "Y" + str(end_year).zfill(4)
    
    end_month       = max([ int(x[1:]) for x in data_dict[end_year_str].keys() ])
    end_month_str   = "M" + str(end_month).zfill(2)
    
    end_day         = max([ int(x[1:]) for x in data_dict[end_year_str][end_month_str].keys() ])
    end_day_str     = "D" + str(end_day).zfill(2)
    
    end_hour        = max([ int(x[1:]) for x in data_dict[end_year_str][end_month_str][end_day_str].keys() ])
    end_hour_str    = "H" + str(end_hour).zfill(2)
    
    available_instrument_sat = []
    available_data_type = []
    
    average_interval = 0
    
    total_files = 0
    criteria_total_files = 0
    
    cur_date = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour))
    end_date = datetime.datetime(int(end_year), int(end_month), int(end_day), int(end_hour))
    
    data_dict = sortOD(data_dict)
    
    for y in data_dict:
        for m in data_dict[y]:
            for d in data_dict[y][m]:
                for h in data_dict[y][m][d]:
                    for datdict in data_dict[y][m][d][h]:
                        if ( ((type(instrument_sat) == str) and (datdict["instrument_sat"] == instrument_sat)) \
                           or ((type(instrument_sat) == list) and (datdict["instrument_sat"] in instrument_sat)) ) \
                          and \
                          ( ((type(data_type) == str) and (datdict["type"] == data_type)) \
                           or ((type(data_type) == list) and (datdict["type"] in data_type)) ):
                            # Get date timestamp
                            date_tag = datdict["filename"].split(".")[2]
                            # Check if timestamps match!
                            # 19910228_18z
                            if not ((int(date_tag[:4]) == int(y[1:])) and \
                                (int(date_tag[4:6]) == int(m[1:])) and \
                                (int(date_tag[6:8]) == int(d[1:])) and \
                                (int(date_tag[-3:-1]) == int(h[1:]))):
                                warn("Timestamp on file does not match folder it is stored in!")
                            
                            # Add new entry
                            file_path = os.path.join(data_dir, y, m, d, h, datdict["filename"])
                            newdatdict = { "instrument_sat" : datdict["instrument_sat"], "type" : datdict["type"], "filename" : file_path }
                            
                            # BUGFIX: If using minutes or less, this will cause duplicate entries.
                            # Check to make sure we're not adding dups!
                            
                            if not newdatdict in files_to_read:
                                files_to_read.append(newdatdict)
                                criteria_total_files += 1
                            
                        if not datdict["instrument_sat"] in available_instrument_sat:
                            available_instrument_sat.append(datdict["instrument_sat"])
                        
                        if not datdict["type"] in available_data_type:
                            available_data_type.append(datdict["type"])
                        
                        total_files += 1
    
    interval_count = 0
    interval_measurements = 0
    
    while 1:
        if (cur_date <= end_date):
            # Rebuild formatted parts
            syear = "Y" + str(cur_date.year).zfill(2)
            smonth = "M" + str(cur_date.month).zfill(2)
            sday = "D" + str(cur_date.day).zfill(2)
            shour = "H" + str(cur_date.hour).zfill(2)
            try:
                # Try to access it
                tmp_notmp = data_dict[syear][smonth][sday][shour]
                
                # Success! Calculate the interval average!
                average_interval = ((average_interval * interval_measurements) + interval_count) / (interval_measurements + 1)
                
                # Reset interval count and increment measurement count.
                interval_count = 0
                interval_measurements += 1
                
                for datdict in data_dict[syear][smonth][sday][shour]:
                    # Check if the variable is a string or a list. If 
                    # it's a string, match it. If it's a list, check to
                    # see if the search term is in the list.
                    # TODO: Perhaps write a function to handle this
                    # mess?!?
                    if ( ((type(instrument_sat) == str) and (datdict["instrument_sat"] == instrument_sat)) \
                       or ((type(instrument_sat) == list) and (datdict["instrument_sat"] in instrument_sat)) ) \
                      and \
                      ( ((type(data_type) == str) and (datdict["type"] == data_type)) \
                       or ((type(data_type) == list) and (datdict["type"] in data_type)) ):
                        # Get date timestamp
                        date_tag = datdict["filename"].split(".")[2]
                        # Check if timestamps match!
                        # 19910228_18z
                        if not ((int(date_tag[:4]) == cur_date.year) and \
                            (int(date_tag[4:6]) == cur_date.month) and \
                            (int(date_tag[6:8]) == cur_date.day) and \
                            (int(date_tag[-3:-1]) == cur_date.hour)):
                            warn("Timestamp on file does not match folder it is stored in!")
            except KeyError:
                interval_count += 1
                pass
            
            # Increment time
            # NOTE - this assumes a timestep of no less than an hour!
            cur_date = cur_date + datetime.timedelta(hours=1)
        else:
            break
    
    stats_dict = {}
    stats_dict["start_year"]               = start_year
    stats_dict["start_month"]              = start_month
    stats_dict["start_day"]                = start_day
    stats_dict["start_hour"]               = start_hour
                                           
    stats_dict["end_year"]                 = end_year
    stats_dict["end_month"]                = end_month
    stats_dict["end_day"]                  = end_day
    stats_dict["end_hour"]                 = end_hour
    
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
