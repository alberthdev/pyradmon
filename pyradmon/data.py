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
from core import *

import datetime
from decimal import Decimal

import copy
import re

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
    """Create a relative channel mapping dict from list of channels.
    
    Given a list of channels, create a relative channel mapping dict
    relating a relative channel number to the actual data channel
    number.
    
    Relative channels start at 1, and end at the total length of the
    channels. For instance::
    
        rel_channels([1, 5, 8, 7, 11])
    
    ...will return::
    
        { 1 : 1, 2 : 5, 3 : 7, 4 : 8, 5 : 11 }
    
    Args:
        chans (list): An array of data channel integers to generate
            a relative channel dictionary from.
    
    Returns:
        dict: Dictonary with the keys being the relative channels, and
        the values being the actual data channel corresponding to each
        relative channel, respectively.
        
    """
    # Make a copy of the channel list
    ordered_chans = list(chans)
    
    # ...and then sort it!
    ordered_chans.sort()
    
    # Initialize a relative channel dict!
    rel_chan_dict = {}
    
    # Go through each channel, and assign relative chans -> data chans.
    # Since the data chans are ordered, the numbering should line up.
    # (E.g. 1 -> first data chan, 2 -> second data chan, etc.)
    for i in xrange(1, len(ordered_chans) + 1):
        rel_chan_dict[i] = ordered_chans[i - 1]
    
    # Return the relative channel mapping dict!
    return rel_chan_dict

def template_to_regex(template):
    """Convert a string template to a parsable regular expression.
    
    Given a data_path_format string template, parse the template into
    a parsable regular expression string for extracting each %VAR%
    variable.
    
    Supported %VAR% variables:
    
    * %EXPERIMENT_ID% - experiment ID (str)
    * %INSTRUMENT_SAT% - instrument/satellite ID (str)
    * %DATA_TYPE% - data type (str)
    * %YEAR% - full year (int, 4 digits)
    * %YEAR4% - full year (int, 4 digits)
    * %YEAR2% - last two digits of year (int, 2 digits)
    * %MONTH% - integer month (int, 2 digits)
    * %MONTH2% - integer month (int, 2 digits)
    * %DAY% - integer day (int, 2 digits)
    * %DAY2% - integer day (int, 2 digits)
    * %HOUR% - integer hour (int, 2 digits)
    * %HOUR2% - integer hour (int, 2 digits)
    
    The returned values are generally passed into 
    :py:func:`extract_fields_via_template` for final field extraction.
    
    Args:
        template (str): A string with the data_path_format template to
            be converted to a parsable regular expression.
    
    Returns:
        tuple: Tuple with the first element being a parsable regular 
        expression string, and the second element being a list of the 
        detected %VAR%s, in order found (from left to right).
        
    """
    # Initialize the final template regex string
    template_final = ""
    
    # Initialize the final matching group list
    matching_groups = []
    
    # Define the variables to replace, with their corresponding regex
    # capturing patterns.
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
    
    # Search for %VAR% variables with a %VAR% matching pattern
    matches = re.findall(r'(.*?)(%.*?%)(.*?)', template)
    
    # Loop through each match!
    for match in matches:
        # Grab the %VAR% part in the match.
        # (match returns a tuple with 3 elements - the misc string on
        # the left side, the %VAR% part in the middle, and the misc
        # string on the right side)
        template_part = match[1]
        
        # Check to see if this %VAR% is in our replacement table!
        if template_part in regex_replace_dict.keys():
            # Add it to the matching group list for future indexing
            # reference!
            matching_groups.append(template_part)
            
            # Then make the variable to regex replacement.
            template_part = template_part.replace(template_part, regex_replace_dict[template_part])
        
        # Finally, assemble the string back together.
        template_final += re.escape(match[0]) + template_part + re.escape(match[2])
    
    # Return the regex template and the list of matching groups!
    return (template_final, matching_groups)

def extract_fields_via_template(template_regex, matching_groups, input_str, suppress_warnings = False):
    """Extract field data from an input string given regex and groups.
    
    Given an input string, extract the field data values from the input 
    string given the parsable regular expression string and a list of 
    %VAR%s, in order found (from left to right), to connect regex 
    matches with fields.
    
    Args:
        template_regex (str): A string with a parsable regular
            expression to be run on the input string.
        matching_groups (list): A list of %VAR%s, in the matching group
            order of template_regex.
        input_str (str): An input string to parse with the regex given
            in template_regex.
        suppress_warnings (bool, optional): A boolean determining
            whether to suppress warnings or not. By default, this is 
            set to False - warnings are not suppressed.
    
    Returns:
        dict: Dictionary with the keys being the %VAR% variables, and 
        the values being the corresponding values, respectively. 
        Integer value types will be integers, while string value types 
        will be strings.
        
        If the template regular expression is unable to match the input
        string, this will return None.
    
    Example:
        Given the following template regex string, matching group list,
        and input string::
        
            template_regex = r"MERRA2/(.*)/(\d{4})"
            matching_groups = [ "%EXPERIMENT_ID%", "%YEAR4%" ]
            input_string = "MERRA2/d5124_m2_jan91/Y1991"
           
        The resulting dictionary should look like this::
        
            {
                "%EXPERIMENT_ID%"   : "d5124_m2_jan91",
                "%YEAR4%"           : 1991,
            }
    
    """
    # Run the regex on the input string.
    match = re.match(template_regex, input_str)
    
    # If it doesn't produce any matches, return None.
    if not match:
        return None
    
    # Initialize the field data dict
    field_data = {}
    
    # Loop through each matching group!
    for group in matching_groups:
        # Check to see if the field/group exists in multiple places
        # (e.g. "data/%YEAR4%/dat/%YEAR4%")
        # If it does, validate that they are consistent!
        if matching_groups.count(group) > 1:
            # Consistent group validation
            tmp_groups = []
            
            # Loop through each group and grab the indexes for each
            # group that matches the current group. Then loop through
            # each returned index!
            for i in [n for (n, m_group) in enumerate(matching_groups) if m_group == group]:
                # ...and append the value for each match at that index!
                tmp_groups.append(match.groups()[i])
            
            # Check to see if the values are the same within the list!
            if not identicalEleListCheck(tmp_groups):
                if not suppress_warnings:
                    warn("WARNING: Detected inconsistency with variable %s! (Values detected: %s)" % (group, str(tmp_groups)))
        
        # Check to see if we have grabbed the value for the field yet
        if group not in field_data:
            # Grab the first index for the group
            rel_index = matching_groups.index(group)
            
            # Sanity check to ensure we are within the match object's
            # bounds
            if rel_index <= (len(match.groups()) - 1):
                field_data[group] = match.groups()[rel_index]
            else:
                # Oops! Not enough matches to grab the value
                if not suppress_warnings:
                    warn("WARNING: Could not fetch value from match! (Variable: %s)" % group)
    
    # Return the final field data dict!
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
        all_channels (bool, optional): A boolean specifying whether to 
            use all of the data or not. This overrides the 
            selected_channel option. By default, this is set to False.
        data_assim_only (bool, optional): A boolean specifying whether 
            to only use assimilated data or not. (Determined by iuse > 
            0!) By default, this is set to False.
        suppress_warnings (bool, optional): A boolean specifying whether to
            suppress warnings or not. This will hide potentially 
            important warnings about data consistency, so only use if 
            you're 100% sure the data is valid! By default, this is set 
            to False - warnings are not suppressed.

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
    # Use set to create a unique list of duplicate data variables.
    data_vars_dups_l = list(set([x for x in data_vars if data_vars.count(x) > 1]))
    
    # Check to see if any duplicate variables exist!
    # If so, raise an Exception...
    if len(data_vars_dups_l) > 0:
        edie("ERROR: Duplicate variables found - %s!" % \
                    (data_vars_dups_l[0] + " is a duplicate" if len(data_vars_dups_l) == 1 else \
                        " and ".join(data_vars_dups_l) + " are duplicates" if len(data_vars_dups_l) == 2 else (", ".join(data_vars_dups_l[:-1]) + ", and " + data_vars_dups_l[-1] + " are duplicates")))
    
    # Initialize an empty data dictionary!
    data_dict = {}
    
    # A dict in case we have multiple channels:
    channel_data_dict = {}
    
    # Initialize the dictionary's keys and values based on the data
    # variables specified.
    # NOTE: all_channels will be handled below!
    
    # Check selected channel - is it a list with more than one element?
    # (Basically, is there more than one channel to deal with?)
    if (type(selected_channel) == list) and (len(selected_channel) > 1):
        # If so, loop through each channel!
        for channel in selected_channel:
            # Initialize a dict for each channel!
            channel_data_dict[channel] = {}
            # Now loop through each data variable...
            for data_var in data_vars:
                # If the data variable is special, initialize it the
                # special data variable with a copy.deepcopy.
                # (Especially for lists and dicts, this is a must!)
                # If not, just initialize it as an ordinary array.
                if data_var in SPECIAL_FIELDS:
                    channel_data_dict[channel][data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                else:
                    channel_data_dict[channel][data_var] = []
    else:
        # Check to make sure that we are not grabbing all channels...
        if not all_channels:
            # Loop through each data variable...
            for data_var in data_vars:
                # If the data variable is special, initialize it with a
                # the special data variable with a copy.deepcopy.
                # (Especially for lists and dicts, this is a must!)
                # If not, just initialize it as an ordinary array.
                if data_var in SPECIAL_FIELDS:
                    data_dict[data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                else:
                    data_dict[data_var] = []
    
    # Initialize ignored channels array
    ignore_channels = []
    
    # Get the number of total files
    total_files = len(files_to_read)
    
    # ...and initialize the file counter!
    file_counter = 0
    
    # Create the template regex and the matching groups from the
    # data_path_format template.
    (template_regex, matching_groups) = template_to_regex(data_path_format)
    
    # Iterate through all of the files!
    for file_to_read in files_to_read:
        # Increment internal file counter
        file_counter += 1
        
        # Extract the path field data from the filename
        field_data = extract_fields_via_template(template_regex, matching_groups, file_to_read["filename"], suppress_warnings)
        
        # Check if we have enough date info.
        # If we do, build the date tag! If not, show an error.
        if ("%YEAR4%" in field_data) and ("%MONTH2%" in field_data) and ("%DAY2%" in field_data) and ("%HOUR2%" in field_data):
            date_tag = field_data["%YEAR4%"] + field_data["%MONTH2%"] + field_data["%DAY2%"] + "_" + field_data["%HOUR2%"] + "z"
        else:
            die("Not enough date information found to build date tag...")
        
        # Every 100 files, print a message to indicate status
        if file_counter % 100 == 0:
            info("Processed %i/%i files... (date tag: %s)" % (file_counter, total_files, date_tag))
        
        debug("PHASE 4: %s" % file_to_read)
        
        # with structure auto-closes the file...
        with open(file_to_read["filename"], 'r') as data_file:
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
            
            # Loop through each line in the data file...
            for data_line in data_file:
                # Increment the line counter
                data_line_counter += 1
                
                # Grab the line, clean extra whitespace with strip(),
                # and split() by space.
                data_elements = data_line.strip().split()
                
                # Check to see if we're on the second line...
                if data_line_counter == 2:
                    # Perform validation on the file's metadata
                    # First, ensure that we only have 3 things to look
                    # at! If not, warn about it!
                    if len(data_elements) == 3:
                        # Check the first element - it should match the
                        # file's instrument_sat tag. If it doesn't
                        # match, warn about it!
                        if (data_elements[0] != file_to_read["instrument_sat"]):
                            if not suppress_warnings:
                                warn("Instrument and satellite data inside file does not match file name tag!")
                        
                        # Build the file date tag from the file
                        # metadata
                        data_file_date_tag = data_elements[1][:-2] + "_" + data_elements[1][-2:] + "z"
                        
                        # Compare it to the file's date tag - if they
                        # don't match, warn about it!
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
                        # Get the column reader going, if not already.
                        if not column_reader:
                            column_reader = ColumnReadPipes(column_reader_data)
                        
                        counted_channels += 1
                        
                        # Check to make sure our channel number field
                        # is a digit.
                        if check_int(data_elements[0]):
                            data_channel = int(data_elements[0])
                            
                            # Here, check if we have multiple channels
                            # enabled, or if we want to retrieve all
                            # channels. 
                            if all_channels or ((type(selected_channel) == list) and (len(selected_channel) > 1)):
                                # If the data channel doesn't exist,
                                # initialize everything!
                                # 
                                # We do this here for all_channels
                                # because we don't have any idea how
                                # many channels (or even what channels)
                                # exist! When looping through, we then
                                # have a good idea of which channel to
                                # use!
                                if not data_channel in channel_data_dict:
                                    # Initialize a dict for each
                                    # channel!
                                    channel_data_dict[data_channel] = {}
                                    # Now loop through each data
                                    # variable...
                                    for data_var in data_vars:
                                        # If the data variable is
                                        # special, initialize the
                                        # special data variable with a
                                        # copy.deepcopy. (Especially
                                        # for lists and dicts, this is
                                        # a must!) If not, just
                                        # initialize it as an ordinary
                                        # array.
                                        if data_var in SPECIAL_FIELDS:
                                            channel_data_dict[data_channel][data_var] = copy.deepcopy(SPECIAL_FIELDS[data_var])
                                        else:
                                            channel_data_dict[data_channel][data_var] = []
                                
                                # Finally, regardless of all_channels
                                # status, set our data_dict to the
                                # current channel dict!
                                data_dict = channel_data_dict[data_channel]
                                debug("Multi-channel mode - RESET triggered. (At channel: %i)" % data_channel)
                            
                            # Match the channel with the desired
                            # one(s).
                            if all_channels or ((type(selected_channel) == int) and (data_channel == selected_channel)) or \
                                ((type(selected_channel) == list) and (data_channel in selected_channel)):
                                
                                # iuse enforcement - check if the
                                # data_assim_only option is set!
                                if data_assim_only:
                                    # Grab the data_column from our
                                    # column reader - this returns an
                                    # integer index. Warnings are NOT
                                    # suppressed.
                                    data_column = column_reader.getColumnIndex("iuse", False)
                                    
                                    # Check if the resulting iuse data
                                    # is an integer...
                                    if check_int(data_elements[data_column]):
                                        # Check if the iuse data is
                                        # less than 0, indicating that
                                        # the data is not assimilated!
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
                                    # Create datetime object
                                    timestamp = datetime.datetime(int(date_tag[:4]), int(date_tag[4:6]), int(date_tag[6:8]), int(date_tag[-3:-1]))
                                    # If it doesn't exist yet, add it
                                    # in!
                                    if not timestamp in data_dict["timestamp"]:
                                        data_dict["timestamp"].append(timestamp)
                                    debug("TIMESTAMP! %s (channel: %i) (file: %s)" % (data_var, data_channel, file_to_read["filename"]))
                                
                                # Loop through data variables
                                for data_var in data_vars:
                                    # Ignore special fields - they are
                                    # already handled.
                                    if data_var in SPECIAL_FIELDS:
                                        continue
                                    
                                    # Split the data variable to get
                                    # the type.
                                    data_var_type = data_var.split('|')[0]
                                    
                                    # Ensure that data types are
                                    # consistent.
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
                                    
                                    # Check to see if we've already
                                    # found the frequency
                                    if (data_dict["frequency"] != ""):
                                        # If we found it, does it match
                                        # the new one? If not, show a
                                        # warning!
                                        if (data_elements[data_column] != data_dict["frequency"]):
                                            if not suppress_warnings:
                                                warn("Frequency within same channel differs from before!")
                                                warn("(Old frequency: %s, new frequency: %s, file: %s)" % (data_dict["frequency"], data_elements[data_column], file_to_read["filename"]))
                                    else:
                                        # Save the frequency for the
                                        # first (and final) time
                                        data_dict["frequency"] = data_elements[data_column]
                                
                                # iuse (assimilated) data variable
                                # handling
                                if "iuse" in data_vars:
                                    # Grab the iuse column index
                                    data_column = column_reader.getColumnIndex("iuse", False)
                                    
                                    # Check to see if we've already
                                    # found iuse (from the above check)
                                    if (len(data_dict["iuse"][file_to_read["type"]]) != 0):
                                        # If we found it, does it match
                                        # the new one? If not, show a
                                        # warning!
                                        if (int(data_elements[data_column]) != data_dict["iuse"][file_to_read["type"]][0]):
                                            debug("iuse within same channel differs from before!")
                                            debug("(Old iuse: %i, new iuse: %s, file: %s)" % (int(data_dict["iuse"][file_to_read["type"]][0]), data_elements[data_column], file_to_read["filename"]))
                                    
                                    # Save the iuse!
                                    if check_int(data_elements[data_column]):
                                        data_dict["iuse"][file_to_read["type"]].append(int(data_elements[data_column]))
                                    else:
                                        warn("iuse is not a digit! Setting to unknown. (iuse = %s)" % data_elements[data_column])
                                        data_dict["iuse"][file_to_read["type"]].append(-1)
                                
                                # Save our data!
                                if (all_channels) or (type(selected_channel) == list) and (len(selected_channel) > 1):
                                    # If it doesn't exist, initialize a
                                    # new one!
                                    if not data_channel in channel_data_dict:
                                        channel_data_dict[data_channel] = {}
                                    channel_data_dict[data_channel].update(data_dict)
                                else:
                                    # Only one channel, so break.
                                    break
                        else:
                            # Channel number field isn't a number...
                            # not good. Go boom!
                            edie("ERROR: Data format seems corrupt (first element is non-int)...")
                    else:
                        # Parse the comment lines (prefixed with !)...
                        # Both metadata and column header are comment
                        # lines!
                        
                        # Read in the column header... but only if
                        # we've read the first two lines, aka the
                        # metadata. Those are NOT part of the column
                        # header!
                        if data_line_counter > 2:
                            column_reader_data += data_line
    
    # Print one last message when complete!
    # ...but only if the number of files is not divisible by 100!
    # (Since we print anyway every 100 files, if it's divisible by 100,
    # it'll be already printed!)
    if file_counter % 100 != 0:
        info("Processed %i/%i files... (date tag: %s)" % (file_counter, total_files, date_tag))
    
    # Post-process iuse data
    for prefix in VALID_PREFIX:
        if prefix in data_dict["iuse"]:
            data_dict[prefix+"|iuse"] = data_dict["iuse"][prefix]
    
    if (all_channels) or ((type(selected_channel) == list) and (len(selected_channel) > 1)):
        # Return multi-channel data dict...
        
        # ...but first, remove channels that failed the iuse test!
        if data_assim_only and len(ignore_channels) > 0:
            for chan in ignore_channels:
                del channel_data_dict[chan]
        
        # ...and finally, return!
        return channel_data_dict
    else:
        # Return single channel data dict...
        return data_dict

def get_data_columns(files_to_read):
    """Returns a dict of the data columns in a file.

    Given a list of dicts containing information on files to read, scan
    each file and return all of the column names in the files.

    Args:
        files_to_read (list): A list of file dicts, returned by
            :py:func:`.enumerate()`. See :py:func:`.enumerate()` for 
            more information about the file dict format.

    Returns:
        dict: Column dictionary whose keys are the column names, and 
        whose values are the column indexes, respectively.
    
    Note:
        Warnings will be printed when inconsistencies with the data
        are detected. No exception will be raised. However, these
        warnings are important, as they can affect the data's
        quality, so make sure to check for and correct any issues
        mentionned by warnings!
    """
    # Create the template regex and the matching groups from the
    # data_path_format template.
    (template_regex, matching_groups) = template_to_regex(data_path_format)
    
    # Iterate through all of the files!
    for file_to_read in files_to_read:
        # Increment internal file counter
        file_counter += 1
        
        # Extract the path field data from the filename
        field_data = extract_fields_via_template(template_regex, matching_groups, file_to_read["filename"], suppress_warnings)
        
        # Check if we have enough date info.
        # If we do, build the date tag! If not, show an error.
        if ("%YEAR4%" in field_data) and ("%MONTH2%" in field_data) and ("%DAY2%" in field_data) and ("%HOUR2%" in field_data):
            date_tag = field_data["%YEAR4%"] + field_data["%MONTH2%"] + field_data["%DAY2%"] + "_" + field_data["%HOUR2%"] + "z"
        else:
            die("Not enough date information found to build date tag...")
        
        # with structure auto-closes the file...
        with open(file_to_read["filename"], 'r') as data_file:
            # Count the lines we've read so that we can do specific
            # things for certain lines.
            data_line_counter = 0
            
            # Save the number of total channels.
            total_channels = 0
            
            # Column reader instance - set to None so we can set it up
            # when we've read in enough column header data.
            column_reader = None
            
            # And the column header data variable itself!
            column_reader_data = ""
            
            # Loop through each line in the data file...
            for data_line in data_file:
                # Increment the line counter
                data_line_counter += 1
                
                # Grab the line, clean extra whitespace with strip(),
                # and split() by space.
                data_elements = data_line.strip().split()
                
                # Check to see if we're on the second line...
                if data_line_counter == 2:
                    # Perform validation on the file's metadata
                    if len(data_elements) == 3:
                        # Check the first element - it should match the
                        # file's instrument_sat tag. If it doesn't
                        # match, warn about it!
                        if (data_elements[0] != file_to_read["instrument_sat"]):
                            warn("Instrument and satellite data inside file does not match file name tag!")
                        
                        # Build the file date tag from the file
                        # metadata
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
                        # Get the column reader going, if not already.
                        if not column_reader:
                            column_reader = ColumnReadPipes(column_reader_data)
                        
                        # Get the column dictionary, and return it!
                        columns_found = column_reader.getColumnDict()
                        return columns_found
                    else:
                        # Parse the comment lines (prefixed with !)...
                        # Both metadata and column header are comment
                        # lines!
                        
                        # Read in the column header... but only if we've read the
                        # first two lines, aka the metadata. Those are NOT part of
                        # the column header!
                        if data_line_counter > 2:
                            column_reader_data += data_line
    
    # If all else fails, return nothing. (None)
    return None

def post_data_columns(data_columns):
    """Add important data columns to the column list and return them.

    Given a dict of data columns containing a list of data columns to 
    read, add additional important data columns to the column list, and 
    return the changed list.
    
    Note that a data columns dict is given as input, and a simple data 
    column list is given as output.
    
    This function is generally used when just dumping all of the
    columns, and not doing any plotting.
    
    Args:
        data_columns (dict): A dict containing the data columns that 
            need to be extracted.

    Returns:
        list: The list of strings containing the data columns that need 
        to be extracted, with any additional required columns that were 
        missing from the original list.
    
    """
    # Initialize data column list
    data_columns_list = []
    
    # Loop through each column
    for col in data_columns:
        # Check if the column selected is the raw frequency column.
        # If it is, replace it with "frequency" instead.
        if col == "freq/wavenum":
            if "frequency" not in data_columns_list:
                data_columns_list.append("frequency")
            continue
        
        # Check if there are any subcolumns.
        # If so, loop through each subcolumn, and create entries for
        # each subcolumn in the COL|SUBCOL format.
        if len(data_columns[col]['subcolumns']) > 0:
            for subcol in data_columns[col]['subcolumns']:
                if (col + "|" + subcol) not in data_columns_list:
                    data_columns_list.append(col + "|" + subcol)
        else:
            # Check if it exists. If not, just append it in!
            if col not in data_columns_list:
                data_columns_list.append(col)
    
    # Ensure that the "timestamp" column exists. If not, add it!
    if "timestamp" not in data_columns_list:
        data_columns_list.append("timestamp")
    
    # Return the final list!
    return data_columns_list

if __name__ == "__main__":
    # Use test data
    from enumerate import enumerate
    from test import *
    
    en = enumerate()
    dat = get_data(en, TEST_DATA_VARS, 4)
