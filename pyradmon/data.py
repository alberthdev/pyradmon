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
# Dataset Enumeration Library -
#   library for enumerating all of the data from the data files found
#   from the data file enumeration library, given column parameters
#   and data specifications.
# 
from columnread import *
import datetime
from decimal import Decimal
from core import *
import copy
import re

# Test data variables
############# TODO : write code to remove dups

# Constants
# Valid prefixes (data types)
VALID_PREFIX = [ "ges", "anl" ]
# Special fields that do not follow normal data collection behavior.
SPECIAL_FIELDS = {
                    "timestamp": [],
                    "frequency": "",
                    "iuse": {},
                 }

# Additional iuse logic
for prefix in VALID_PREFIX:
    SPECIAL_FIELDS["iuse"][prefix] = []

def rel_channels(chans):
    ordered_chans = list(chans)
    ordered_chans.sort()
    rel_chan_dict = {}
    for i in xrange(1, len(ordered_chans) + 1):
        rel_chan_dict[i] = ordered_chans[i - 1]
    return rel_chan_dict

def template_to_regex(template):
    template_final = ""
    
    matching_groups = []
    
    regex_replace_dict = {
                            "%EXPERIMENT_ID%"   : r'(.*)',
                            "%INSTRUMENT_SAT%"  : r'(.*)',
                            "%DATA_TYPE%"       : r'(.*)',
                            
                            "%YEAR%"            : r'(\d{4})',
                            "%YEAR4%"           : r'(\d{4})',
                            "%YEAR2%"           : r'(\d{2})',
                            
                            "%MONTH%"           : r'(\d{2})',
                            "%MONTH2%"          : r'(\d{2})',
                            
                            "%DAY%"             : r'(\d{2})',
                            "%DAY2%"            : r'(\d{2})',
                            
                            "%HOUR%"            : r'(\d{2})',
                            "%HOUR2%"           : r'(\d{2})',
                        }
    
    matches = re.findall(r'(.*?)(%.*?%)(.*?)', template)
    for match in matches:
        template_part = match[1]
        
        if template_part in regex_replace_dict.keys():
            matching_groups.append(template_part)
            template_part = template_part.replace(template_part, regex_replace_dict[template_part])
        
        template_final += re.escape(match[0]) + template_part + re.escape(match[2])
    
    return (template_final, matching_groups)

def extract_fields_via_template(template_regex, matching_groups, input_str, suppress_warnings = False):
    match = re.match(template_regex, input_str)
    if not match:
        return None
    
    field_data = {}
    
    for group in matching_groups:
        if matching_groups.count(group) > 1:
            # Consistent group validation
            tmp_groups = []
            for i in [n for (n, m_group) in enumerate(matching_groups) if m_group == 'll']:
                tmp_groups.append(m_group)
            if not identicalEleListCheck(tmp_groups):
                if not suppress_warnings:
                    warn("WARNING: Detected inconsistency with variable %s! (Values detected: %s)" % (group, str(tmp_groups)))
        
        if group not in field_data:
            rel_index = matching_groups.index(group)
            
            if rel_index <= (len(match.groups()) - 1):
                field_data[group] = match.groups()[rel_index]
            else:
                if not suppress_warnings:
                    warn("WARNING: Could not fetch value from match! (Variable: %s)" % group)
    
    return field_data

def get_data(files_to_read, data_vars, selected_channel, data_path_format, all_channels = False, data_assim_only = False, suppress_warnings = False):
    """Returns a dict with data that matches the given specifications.

    Given a list of files to read (dict based), a list of data
    variables, and a channel specified by an integer, return a dict
    with the data specified by the data variable list.

    Args:
        files_to_read (list): A list of file dicts, returned by
            :py:func:`.enumerate()`.
        data_vars (list): A list of strings defining data variables to
            extract from the files. Special data variables include:
            
            * timestamp:
                A list of timestamps that can be used for plotting. The 
                timestamps are :py:class:`datetime.datetime` objects 
                that matplotlib can use for timeseries plots.
            * frequency:
                A single string that specifies what frequency is being 
                used for the data.
            
            All other data variables will return a decimal list of the
            data.
        selected_channel (int): An integer (or array of integers)
            specifying the data channel(s) to use for extracting the 
            data.
        all_channels (bool): A boolean specifying whether to use all of
            the data or not. This overrides the selected_channel 
            option.
        data_assim_only (bool): A boolean specifying whether to only
            use assimilated data or not. (Determined by iuse > 0!)
        suppress_warnings (bool): A boolean specifying whether to
            suppress warnings or not. This will hide potentially 
            important warnings about data consistency, so only use if 
            you're 100% sure the data is valid!

    Returns:
        dict: If there are multiple selected channels, or if 
        all_channels is True, a dict is returned whose keys are the 
        channel numbers, and whose values are regular data_dicts. (See 
        below for format.)
        
        If there's only one channel, a single data_dict is returned.
        
        The data_dict has keys with the requested data variables (from
        data_vars), and values with a list/array of Decimal objects
        corresponding to the requested data variable keys.
        
        Multi-channel example:
        
        .. code-block:: python
        
            { 1: 
                {
                    'iuse'      : [-1, 1, -1],
                    'bc_fixang' : [1.23, 1.22, 1.235, 1.201],
                    ...
                },
              2:
                {
                    'iuse'      : [-1, 1, -1],
                    'bc_fixang' : [1.23, 1.22, 1.235, 1.201],
                    ...
                },
                ...
            }
        
        Single-channel example (data_dict):
        
        .. code-block:: python
        
            {
                'iuse'      : [-1, 1, -1],
                'bc_fixang' : [1.23, 1.22, 1.235, 1.201],
                ...
            }

    Raises:
        Exception(...) - error exception when either:
            - an ambiguous variable is found
            - the column index for a data variable can not be found
              (and therefore makes the data variable invalid)
            - the channel number can't be read (and therefore the data
              is corrupt)
    
    Note:
        Warnings will be printed when inconsistencies with the data are 
        detected. No exceptions will be raised. However, these warnings 
        are important, as they can affect the data's quality, so make 
        sure to check for and correct any issues mentionned by 
        warnings!
    """
    debug("PHASE 1")
    # data_vars validation
    for data_var in data_vars:
        # Make sure the variable is not a special field, since a
        # special field variable would fail the test.
        if not data_var in SPECIAL_FIELDS:
            # Check to see if the beginning part of the data_var is a
            # valid prefix (or data type). If not, raise exception.
            if not data_var.split("|")[0] in VALID_PREFIX:
                edie("ERROR: Ambiguous variable '%s' found - %s must be prefixed before the actual var!" % \
                    (data_var, VALID_PREFIX[0] if len(VALID_PREFIX) == 1 else \
                        " or ".join(VALID_PREFIX) if len(VALID_PREFIX) == 2 else (", ".join(VALID_PREFIX[:-1]) + ", or " + VALID_PREFIX[-1])))
    # Last one - check for any dups!
    data_vars_dups = set([x for x in data_vars if data_vars.count(x) > 1])
    data_vars_dups_l = list(data_vars_dups)
    if len(data_vars_dups_l) > 0:
        edie("ERROR: Duplicate variables found - %s!" % \
                    (data_vars_dups_l[0] + " is a duplicate" if len(data_vars_dups_l) == 1 else \
                        " and ".join(data_vars_dups_l) + " are duplicates" if len(data_vars_dups_l) == 2 else (", ".join(data_vars_dups_l[:-1]) + ", and " + data_vars_dups_l[-1] + " are duplicates")))
    debug("PHASE 2")
    # Initialize an empty data dictionary!
    data_dict = {}
    
    # A dict in case we have multiple channels:
    channel_data_dict = {}
    
    # Initialize the dictionary's keys and values based on the data
    # variables specified.
    # NOTE: all_channels will be handled below!
    if (type(selected_channel) == list) and (len(selected_channel) > 1):
        for channel in selected_channel:
            channel_data_dict[channel] = {}
            for data_var in data_vars:
                if data_var in SPECIAL_FIELDS:
                    channel_data_dict[channel][data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                else:
                    channel_data_dict[channel][data_var] = []
    else:
        if not all_channels:
            for data_var in data_vars:
                if data_var in SPECIAL_FIELDS:
                    data_dict[data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                else:
                    data_dict[data_var] = []
    debug("PHASE 3")
    
    #debug(data_dict)
    
    ignore_channels = []
    
    total_files = len(files_to_read)
    file_counter = 0
    
    # Iterate through all of the files!
    for file_to_read in files_to_read:
        # with structure auto-closes the file...
        file_counter += 1
        
        (template_regex, matching_groups) = template_to_regex(data_path_format)
        field_data = extract_fields_via_template(template_regex, matching_groups, file_to_read["filename"], suppress_warnings)
        
        if ("%YEAR4%" in field_data) and ("%MONTH2%" in field_data) and ("%DAY2%" in field_data) and ("%HOUR2%" in field_data):
            date_tag = field_data["%YEAR4%"] + field_data["%MONTH2%"] + field_data["%DAY2%"] + "_" + field_data["%HOUR2%"] + "z"
        else:
            die("Not enough date information found to build date tag...")
        
        if file_counter % 100 == 0:
            info("Processed %i/%i files... (date tag: %s)" % (file_counter, total_files, date_tag))
        
        debug("PHASE 4: %s" % file_to_read)
        with open(file_to_read["filename"], 'r') as data_file:
            #print "Reading file: %s" % file_to_read["filename"]
            
            # Count the lines we've read so that we can do specific
            # things for certain lines.
            data_line_counter = 0
            
            # Save the number of total channels.
            total_channels = 0
            
            # Keep track of the number of channels found.
            # (Unused for efficiency, since we break after we find the
            # desired channel.)
            counted_channels = 0
            
            # Column reader instance - set to None so we can set it up
            # when we've read in enough column header data.
            column_reader = None
            
            # And the column header data variable itself!
            column_reader_data = ""
            
            for data_line in data_file:
                data_line_counter += 1
                data_elements = data_line.strip().split()
                #print data_elements
                if data_line_counter == 2:
                    # Perform validation on the file's metadata
                    if len(data_elements) == 3:
                        if (data_elements[0] != file_to_read["instrument_sat"]):
                            if not suppress_warnings:
                                warn("Instrument and satellite data inside file does not match file name tag!")
                        
                        # 19910228_18z
                        data_file_date_tag = data_elements[1][:-2] + "_" + data_elements[1][-2:] + "z"
                        
                        if date_tag != data_file_date_tag:
                            if not suppress_warnings:
                                warn("Timestamp inside file does not match file name timestamp!")
                        
                        # Channel validation will happen later
                        # ... or not, to be efficient. May remove.
                        total_channels = int(data_elements[2])
                    else:
                        if not suppress_warnings:
                            warn("Number of elements inside the metainfo of the file is invalid. Can't verify contents of metainfo!")
                elif len(data_elements) > 2:
                    # Parse non-comments - basically actual file data.
                    if not data_line.strip().startswith("!"):
                        #print " * Parse data"
                        # Get the column reader going, if not already.
                        if not column_reader:
                            #print " * Column reader trigger"
                            column_reader = ColumnReadPipes(column_reader_data)
                        
                        counted_channels += 1
                        
                        # Check to make sure our channel number field
                        # is a digit.
                        if check_int(data_elements[0]):
                            data_channel = int(data_elements[0])
                            
                            if all_channels or ((type(selected_channel) == list) and (len(selected_channel) > 1)):
                                if not data_channel in channel_data_dict:
                                    channel_data_dict[data_channel] = {}
                                    for data_var in data_vars:
                                        if data_var in SPECIAL_FIELDS:
                                            channel_data_dict[data_channel][data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                                        else:
                                            channel_data_dict[data_channel][data_var] = []
                                data_dict = channel_data_dict[data_channel]
                                debug("Multi-channel mode - RESET triggered. (At channel: %i)" % data_channel)
                            
                            # Match the channel with the desired one.
                            if all_channels or ((type(selected_channel) == int) and (data_channel == selected_channel)) or \
                                ((type(selected_channel) == list) and (data_channel in selected_channel)):
                                #print " * Channel found trigger"
                                # iuse enforcement
                                if data_assim_only:
                                    data_column = column_reader.getColumnIndex("iuse", False)
                                    
                                    if check_int(data_elements[data_column]):
                                        if int(data_elements[data_column]) < 0:
                                            debug("SKIP: %s (channel: %i) (file: %s)" % (data_var, data_channel, file_to_read["filename"]))
                                            data_dict["iuse"][file_to_read["type"]].append(int(data_elements[data_column]))
                                            if not data_channel in ignore_channels:
                                                ignore_channels.append(data_channel)
                                            continue
                                    else:
                                        if not suppress_warnings:
                                            warn("iuse is not a digit! Skipping. (iuse = %s)" % data_elements[data_column])
                                        continue
                                debug("NOSKIP: %s (channel: %i) (file: %s)" % (data_var, data_channel, file_to_read["filename"]))
                                
                                # Timestamp data variable handling
                                if ("timestamp" in data_vars):
                                    timestamp = datetime.datetime(int(date_tag[:4]), int(date_tag[4:6]), int(date_tag[6:8]), int(date_tag[-3:-1]))
                                    if not timestamp in data_dict["timestamp"]:
                                        data_dict["timestamp"].append(timestamp)
                                    debug("TIMESTAMP! %s (channel: %i) (file: %s)" % (data_var, data_channel, file_to_read["filename"]))
                                for data_var in data_vars:
                                    # Ignore special fields
                                    if data_var in SPECIAL_FIELDS:
                                        continue
                                    
                                    # Split the data variable to get
                                    # the type.
                                    data_var_type = data_var.split('|')[0]
                                    
                                    #print "%s vs %s" % (data_var_type, file_to_read["type"])
                                    
                                    # Ensure that data types are consistent
                                    if data_var_type == file_to_read["type"]:
                                        # Remove the data variable type
                                        real_data_var = '|'.join(data_var.split('|')[1:])
                                        
                                        # Now fetch the column index!
                                        data_column = column_reader.getColumnIndex(real_data_var, False)
                                        if data_column == None:
                                            edie("ERROR: Unable to fetch column index. See above for details.")
                                        
                                        # Finally, nab the real data!
                                        data_dict[data_var].append(Decimal(data_elements[data_column]))
                                
                                # Frequency data variable handling
                                if "frequency" in data_vars:
                                    data_column = column_reader.getColumnIndex("freq/wavenum", False)
                                    
                                    # Check to see if we've already found the frequency
                                    if (data_dict["frequency"] != ""):
                                        # If we found it, does it match the new one? If not, show a warning!
                                        if (data_elements[data_column] != data_dict["frequency"]):
                                            if not suppress_warnings:
                                                warn("Frequency within same channel differs from before!")
                                                warn("(Old frequency: %s, new frequency: %s, file: %s)" % (data_dict["frequency"], data_elements[data_column], file_to_read["filename"]))
                                    else:
                                        # Save the frequency for the first (and final) time
                                        data_dict["frequency"] = data_elements[data_column]
                                
                                # iuse (assimilated) data variable handling
                                if "iuse" in data_vars:
                                    data_column = column_reader.getColumnIndex("iuse", False)
                                    
                                    debug("DATA_VAR: "+data_var+" | DATA_VAR_TYPE: "+data_var_type)
                                    # Check to see if we've already found iuse
                                    if (len(data_dict["iuse"][file_to_read["type"]]) != 0):
                                        # If we found it, does it match the new one? If not, show a warning!
                                        if (int(data_elements[data_column]) != data_dict["iuse"][file_to_read["type"]][0]):
                                            debug("iuse within same channel differs from before!")
                                            debug("(Old iuse: %i, new iuse: %s, file: %s)" % (int(data_dict["iuse"][file_to_read["type"]][0]), data_elements[data_column], file_to_read["filename"]))
                                    
                                    # Save the iuse!
                                    if check_int(data_elements[data_column]):
                                        data_dict["iuse"][file_to_read["type"]].append(int(data_elements[data_column]))
                                    else:
                                        warn("iuse is not a digit! Setting to unknown. (iuse = %s)" % data_elements[data_column])
                                        data_dict["iuse"][file_to_read["type"]].append(-1)
                                
                                if (all_channels) or (type(selected_channel) == list) and (len(selected_channel) > 1):
                                    if not data_channel in channel_data_dict:
                                        channel_data_dict[data_channel] = {}
                                    channel_data_dict[data_channel].update(data_dict)
                                else:
                                    # Only one channel, so break.
                                    break
                        else:
                            # Channel number field isn't a number... not good. Go boom!
                            edie("ERROR: Data format seems corrupt (first element is non-int)...")
                    else:
                        #print " * Parse comment"
                        
                        # Read in the column header... but only if we've read the
                        # first two lines, aka the metadata. Those are NOT part of
                        # the column header!
                        if data_line_counter > 2:
                            column_reader_data += data_line
    
    info("Processed %i/%i files... (date tag: %s)" % (file_counter, total_files, date_tag))
    
    # Post-process iuse data
    for prefix in VALID_PREFIX:
        if prefix in data_dict["iuse"]:
            data_dict[prefix+"|iuse"] = data_dict["iuse"][prefix]
    
    #raw_input()
    if (all_channels) or ((type(selected_channel) == list) and (len(selected_channel) > 1)):
        #print "Returning multi-channel data dict..."
        
        # Remove channels that failed the iuse test!
        if data_assim_only and len(ignore_channels) > 0:
            for chan in ignore_channels:
                del channel_data_dict[chan]
        
        return channel_data_dict
    else:
        #print "Returning single channel data dict..."
        return data_dict

def get_data_columns(files_to_read):
    """Returns a dict of the data columns in a file.

    TODO

    Args:
        files_to_read: A list of file dicts, returned by enumerate().

    Returns:
        TODO

    Raises:
        Exception(...) - error exception when either:
            - an ambiguous variable is found
            - the column index for a data variable can not be found
              (and therefore makes the data variable invalid)
            - the channel number can't be read (and therefore the data
              is corrupt)
    
    Note:
        Warnings will be printed when inconsistencies with the data
        are detected. No exception will be raised. However, these
        warnings are important, as they can affect the data's
        quality, so make sure to check for and correct any issues
        mentionned by warnings!
    """
    
    # Iterate through all of the files!
    for file_to_read in files_to_read:
        (template_regex, matching_groups) = template_to_regex(data_path_format)
        field_data = extract_fields_via_template(template_regex, matching_groups, file_to_read["filename"], suppress_warnings)
        
        if ("%YEAR4%" in field_data) and ("%MONTH2%" in field_data) and ("%DAY2%" in field_data) and ("%HOUR2%" in field_data):
            date_tag = field_data["%YEAR4%"] + field_data["%MONTH2%"] + field_data["%DAY2%"] + "_" + field_data["%HOUR2%"] + "z"
        else:
            die("Not enough date information found to build date tag...")
        
        # with structure auto-closes the file...
        with open(file_to_read["filename"], 'r') as data_file:
            #print "Reading file: %s" % file_to_read["filename"]
            
            # Count the lines we've read so that we can do specific
            # things for certain lines.
            data_line_counter = 0
            
            # Save the number of total channels.
            total_channels = 0
            
            # Keep track of the number of channels found.
            # (Unused for efficiency, since we break after we find the
            # desired channel.)
            counted_channels = 0
            
            # Column reader instance - set to None so we can set it up
            # when we've read in enough column header data.
            column_reader = None
            
            # And the column header data variable itself!
            column_reader_data = ""
            
            for data_line in data_file:
                data_line_counter += 1
                data_elements = data_line.strip().split()
                #print data_elements
                if data_line_counter == 2:
                    # Perform validation on the file's metadata
                    if len(data_elements) == 3:
                        if (data_elements[0] != file_to_read["instrument_sat"]):
                            warn("Instrument and satellite data inside file does not match file name tag!")
                        
                        # 19910228_18z
                        data_file_date_tag = data_elements[1][:-2] + "_" + data_elements[1][-2:] + "z"
                        
                        if date_tag != data_file_date_tag:
                            warn("Timestamp inside file does not match file name timestamp!")
                        
                        # Channel validation will happen later
                        # ... or not, to be efficient. May remove.
                        total_channels = int(data_elements[2])
                    else:
                        warn("Number of elements inside the metainfo of the file is invalid. Can't verify contents of metainfo!")
                elif len(data_elements) > 2:
                    # Parse non-comments - basically actual file data.
                    if not data_line.strip().startswith("!"):
                        #print " * Parse data"
                        # Get the column reader going, if not already.
                        if not column_reader:
                            #print " * Column reader trigger"
                            column_reader = ColumnReadPipes(column_reader_data)
                        
                        columns_found = column_reader.getColumnDict()
                        return columns_found
                    else:
                        #print " * Parse comment"
                        
                        # Read in the column header... but only if we've read the
                        # first two lines, aka the metadata. Those are NOT part of
                        # the column header!
                        if data_line_counter > 2:
                            column_reader_data += data_line

def post_data_columns(data_columns):
    data_columns_list = []
    for col in data_columns:
        if col == "freq/wavenum":
            if "frequency" not in data_columns_list:
                data_columns_list.append("frequency")
            continue
        if len(data_columns[col]['subcolumns']) > 0:
            for subcol in data_columns[col]['subcolumns']:
                if (col + "|" + subcol) not in data_columns_list:
                    data_columns_list.append(col + "|" + subcol)
        else:
            if col not in data_columns_list:
                data_columns_list.append(col)
    if "timestamp" not in data_columns_list:
        data_columns_list.append("timestamp")
    return data_columns_list

if __name__ == "__main__":
    # Use test data
    from enumerate import enumerate
    from test import *
    import pprint
    en = enumerate()
    dat = get_data(en, TEST_DATA_VARS, 4)
    #pprint.pprint(dat)
