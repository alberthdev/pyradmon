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
# Plot Generation Library -
#   library for making plots from data
# 

import matplotlib
matplotlib.use('Agg', warn=False)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import math

from core import *
from data import VALID_PREFIX

import datetime
import re
import copy
import warnings

# Filter out consistent warnings...
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", "No labeled objects found. Use label='...' kwarg on individual plots.", UserWarning)

def fetch_key_from_subplot_dict(subplot_dict):
    """Fetch the subplot key from the subplot dict.
    
    Given the subplot dictionary, fetch and return the subplot key from
    the subplot dict.
    
    Args:
        plot_dict: The plot dictionary to substitute values into. See
            plot() help for more information on its format.
        data_dict: The data dictionary to retrieve values from. See
            get_data() help (in data.py) for more information on its
            format.
    
    Returns:
        A string containing the subplot key from the subplot dict,
        needed to access the subplot dict.
    
    Raises:
        Exception: Occurs when there are more than one key (or no keys)
            within the subplot dictionary.
    """
    keys = subplot_dict.keys()
    
    if len(keys) != 1:
        edie("Subplot dict doesn't have the correct number of keys! (%i keys found!)" % len(keys))
    
    return "".join(keys)

def subst_data(plot_dict, data_dict):
    """Substitute data from the data dict into the specified plot dict.
    
    Go through the plot dictionary, and for each variable that doesn't
    have the actual values, substitute the correct values in using
    data_dict.
    
    Args:
        plot_dict: The plot dictionary to substitute values into. See
            plot() help for more information on its format.
        data_dict: The data dictionary to retrieve values from. See
            get_data() help (in data.py) for more information on its
            format.
    
    Returns:
        A plot dictionary with all of its values substituted in. See
        plot() help for more information on its format.
    """
    # Make a full copy of the plot dictionary so that we can work on
    # our own copy (and not modify the original).
    plot_dict_new = copy.deepcopy(plot_dict)
    
    # Loop through each plot ID...
    for plot_id in plot_dict_new:
        # Convenience variable
        plot = plot_dict_new[plot_id]
        
        # Loop through all of the plots... at least their index first!
        for subplotIndex in xrange(0, len(plot["plots"])):
            # Then fetch their key - there should only be one key.
            subplotIDKey = fetch_key_from_subplot_dict(plot["plots"][subplotIndex])
            
            # Convenience variable
            subplot = plot["plots"][subplotIndex][subplotIDKey]
            
            # Check to make sure this subplot has a "data" element
            if isset("data", subplot):
                # Check to make sure this subplot has an "x" axis element
                if isset("x", subplot["data"]):
                    # If str, turn into a list of single str
                    if type(subplot["data"]["x"]) == str:
                        subplot["data"]["x"] = [ subplot["data"]["x"] ]
                    
                    # Loop through each element ID
                    for eleID in xrange(0, len(subplot["data"]["x"])):
                        # Ensure that it's not already substituted in!
                        if (type(subplot["data"]["x"][eleID]) == list):
                            warn("Conversion from ID to list attempted, but data is already a list! (x)")
                        else:
                            subplot["data"]["x"][eleID] = data_dict[subplot["data"]["x"][eleID]]
                
                # Check to make sure this subplot has an "x" axis element
                if isset("y", subplot["data"]):
                    # If str, turn into a list of single str
                    if type(subplot["data"]["y"]) == str:
                        subplot["data"]["y"] = [ subplot["data"]["y"] ]
                    for eleID in xrange(0, len(subplot["data"]["y"])):
                        # Ensure that it's not already substituted in!
                        if (type(subplot["data"]["y"][eleID]) == list):
                            warn("Conversion from ID to list attempted, but data is already a list! (y)")
                        else:
                            subplot["data"]["y"][eleID] = data_dict[subplot["data"]["y"][eleID]]
            else:
                warn("No data found to convert!")
    
    return plot_dict_new

def title_output_replace(input_title_output, metadata_dict, data_dict, rel_channels_dict, is_title = False, custom_vars = None):
    """Substitute %VAR% variables with provided values and constants.
    
    Given a title (or output path) string template, replace %VAR%
    variables with the appropriate value or constant.
    
    Variables supported include:
        %EXPERIMENT_ID% - Experiment ID, sourced from metadata_dict.
        %INSTRUMENT_SAT% - Instrument/satellite ID, sourced from
            metadata_dict.
        %CHANNEL% - Channel number, sourced from metadata_dict.
        %RELCHANNEL% - Relative channel number, indirectly sourced from
            rel_channels_dict.
        %FREQUENCY% - Frequency of the selected channel, sourced from
            the frequency field in data_dict.
        %ASSIMILATION_STATUS% - Placeholder for the assimilation status,
            which is determined from the iuse field in data_dict (not
            done here).
        %START_DATE% - Start date in YYYYMMDD format, sourced from
            metadata_dict.
        %END_DATE% - End date in YYYYMMDD format, sourced from
            metadata_dict.
        Additional custom %VARS% sourced from custom_vars, if specified.
    
    Args:
        input_title_output: The string with the title (or output path)
            template.
        metadata_dict: The metadata dictionary containing data source
            information.
        data_dict: The data dictionary to retrieve values from for
            certain %VAR% variables. See get_data() help (in data.py)
            for more information on its format.
        rel_channels_dict: The relative channels dictionary to map
            relative channels to actual data channels. Its keys are the
            relative channels, and its values are the actual data
            channels. (In this case, the mapping is reversed later to
            allow easy conversion from data channel to relative
            channel.)
        is_title: Boolean indicating whether the string templace is a
            title or not. This affects how and what variables are
            replaced. By default, this is set to False.
        custom_vars: Dictionary containing custom variables to be
            replaced. Its keys are %VAR% variables without the percent
            sign, and its values are what should take their places.
            For instance, given { "TESTVAR": "test123" }, the template
            "%TESTVAR%" should be replaced with "test123". By default,
            this is set to None - this argument is optional if there
            are no custom variables.
    
    Returns:
        A string with %VAR% variables replaced with the appropriate
        value or constant. Some %VAR% variables may not be replaced if
        they do not exist, or certain conditions are not met.
    """
    # Replace experiment ID variable
    input_title_output = input_title_output.replace("%EXPERIMENT_ID%", metadata_dict["experiment_id"])
    
    # Capitalize %INSTRUMENT_SAT% if we're using it in a title.
    if is_title:
        input_title_output = input_title_output.replace("%INSTRUMENT_SAT%", metadata_dict["instrument_sat"].upper())
    else:
        input_title_output = input_title_output.replace("%INSTRUMENT_SAT%", metadata_dict["instrument_sat"])
    
    # Replace data channel variable
    input_title_output = input_title_output.replace("%CHANNEL%", str(metadata_dict["channel"]))
    
    # Reverse the channel map
    # Original: rel_channel -> actual data channel
    # Inverted: actual data channel -> rel_channel
    rel_channels_inv_map = dict(zip(rel_channels_dict.values(), rel_channels_dict.keys()))
    input_title_output = input_title_output.replace("%RELCHANNEL%", str(rel_channels_inv_map[metadata_dict["channel"]]))
    
    # Ensure that we have adequate data to determine frequency.
    # If we do, replace the frequency variable!
    if data_dict and "frequency" in data_dict:
        input_title_output = input_title_output.replace("%FREQUENCY%", str(data_dict["frequency"]))
    
    # Replace assimilation status placeholder... only if it's a title.
    if is_title:
        input_title_output = input_title_output.replace("%ASSIMILATION_STATUS%", "    .......................")
    
    # Replace date variables
    input_title_output = input_title_output.replace("%START_DATE%", str(metadata_dict['start_year']).zfill(4) + str(metadata_dict['start_month']).zfill(2) + str(metadata_dict['start_day']).zfill(2))
    input_title_output = input_title_output.replace("%END_DATE%", str(metadata_dict['end_year']).zfill(4) + str(metadata_dict['end_month']).zfill(2) + str(metadata_dict['end_day']).zfill(2))
    
    # Custom vars
    if custom_vars:
        for custom_var in custom_vars:
            # Do a case insensitive replace
            replace_re = re.compile(re.escape('%'+custom_var+'%'), re.IGNORECASE)
            input_title_output = replace_re.sub(custom_vars[custom_var], input_title_output)
    
    return input_title_output

def plot(plot_dict, data_dict, metadata_dict, rel_channels_dict, custom_vars = None, make_dirs = False):
    """Given plot settings and data/constants, produce a plot.
    
    Given plot settings defined in a special plot dict, and various data
    and constants sourced from other dicts, plot specified data and
    save the resulting plot.
    
    The plot dictionary takes on a hierarchical format:
    {
      'PLOT_ID' : {
                   'output': OUTPUT_PATH_TEMPLATE,
                   'settings': 
                     {
                       'dpi': PLOT_DPI,
                       'target_size': TARGET_SIZE,
                     },
                   'title': PLOT_TITLE,
                   'plots':
                      [
                        {
                          'SUBPLOT_ID' : 
                            {
                              'axes':
                                {
                                  'x':
                                    {
                                      'label': AXIS_LABEL,
                                      'ticks': NUM_OF_TICKS,
                                    },
                                  'y':
                                    {
                                      'label': AXIS_LABEL,
                                      'ticks': NUM_OF_TICKS,
                                    },
                                }
                              'data':
                                {
                                  'color': LINE_COLORS,
                                  'labels': DATA_LABELS,
                                  'x': DATA_FIELD or RAW_DATA,
                                  'y': DATA_FIELD or RAW_DATA,
                                  'post_processing': {
                                     'x': POST_PROCESSING_FUNC,
                                     'y': POST_PROCESSING_FUNC,
                                   },
                                }
                              'legend':
                                {
                                  'title': LEGEND_TITLE,
                                }
                              'title': SUBPLOT_TITLE,
                            },
                        }
                      ],
                  },
    }
    
    Fields:
        PLOT_ID: The ID of the plot you wish to make. This can be
            anything - whether something simple as "plot1" or something
            creative as "whackyplot". The ID of the plot should be
            unique. (String)
        OUTPUT_PATH_TEMPLATE: The path template specifying where the
            plot should be saved to. This can either be a regular path
            or a path template, with variables that can be replaced at
            runtime. See title_output_replace() for the variables that
            can be used. (String)
        PLOT_DPI: The DPI, or Dots Per Inch, of the output image that
            matplotlib should render to. The larger the DPI, the larger
            the text/graphics will be. (Integer)
        TARGET_SIZE: A two element list/array specifying the target size
            of the resulting plot image, in pixels. Both the X and the Y
            part of TARGET_SIZE will be divided by PLOT_DPI to calculate
            the proper scaling of the plot. NOTE - TARGET_SIZE will
            attempt to get the nearest size specified. Due to matplotlib
            limitations, the size specified here may not be the final
            image output size. (List/array of integers)
        PLOT_TITLE: The plot title. This can be either a regular title
            string, or a title template, with variables that can be
            replaced at runtime. See title_output_replace() for the
            variables that can be used. (String)
        SUBPLOT_ID: The ID of the subplot you wish to make. This can be
            anything - whether something simple as "subplot1" or
            something creative as "hellosubplot". The ID of the subplot
            should be unique. (String)
        AXIS_LABEL: The axis label for the corresponding axis. (String)
        NUM_OF_TICKS: An integer number of ticks for the corresponding
            axis. (Integer)
        LINE_COLORS: A list/array of color strings specifying the color
            for each Y data plotted, respectively. Colors include blue,
            green, red, cyan, magenta, yellow, black, and white. (You
            can also specify the first letter of the color.) (List/array
            of strings)
        DATA_LABELS: A list/array of labels specifying the label for
            each Y data plotted, respectively. The labels will be shown
            in a legend, if enabled. Each label includes minimal
            templating: "%AVERAGE%" will be replaced with the data
            average, and "%STDDEV%" will be replaced with the data
            standard deviation. (List/array of strings)
        DATA_FIELD: A list/array of data fields specifying which data
            field should be plotted for the corresponding axis. This is
            dependent on the data available in data_dict. (List/array of
            strings)
        RAW_DATA: An array of floats, Decimals, datetime objects,or
            integers containing the raw data to be plotted to the
            respective axis. (datetime objects should be limited to the
            X axis. While it's technically possible to plot datetime
            objects on the Y axis, it may not be fully supported.)
            (List/array of floats, Decimals, datetime objects, or
            integers)
        POST_PROCESSING_FUNC: An array of strings defining lambda
            functions, without the lambda definition. The lamba is
            defined as:
                lambda data,x,y: FUNCTION_GOES_HERE
            The "data" variable provides the entire data_dict, which is
            a dictionary whose keys are the data fields, and whose
            values are a list of the respective data. (Note that this is
            a single channel data_dict, NOT a multichannel one, since
            plot only plots one channel.) The "x" and "y" variable
            provides the currently used data for their axes,
            respectively. Examples:
              x: "[(date-datetime.timedelta(days=1)) for date in x]"
                Equiv: lambda data,x,y: \
                  [ (date - datetime.timedelta(days=1)) for date in x ]
                Subtract one day from each timestamp in the X data.
              x: "y"
                Equiv: lambda data,x,y: y
                Return the y data in place of the x data.
              y: "[ y_item + 1 for y_item in y ]"
                Equiv: lambda data,x,y: \
                  [ y_item + 1 for y_item in y ]
                Increment each value of y by one.
              y: '[(data["bla"][i]+y[i]) for i in xrange(0, len(y))]'
                Equiv: lambda data,x,y: \
                  [ (data["bla"][i] + y[i]) for i in xrange(0, len(y)) ]
                Add data from data field "bla" to the y data.
            Note that the strings would be in an array/list for each
            data point!
        LEGEND_TITLE: The legend title. (String)
        SUBPLOT_TITLE: The subplot title. (String)
    
    Args:
        plot_dict: The plot dictionary with information on how to make
            the plots. Format details can be found above.
        data_dict: The data dictionary to retrieve the values to plot
            from. See get_data() help (in data.py) for more information
            on its format.
        metadata_dict: The metadata dictionary containing data source
            information. This dictionary should include the following
            elements: instrument_sat, experiment_id, channel,
            start_year, start_month, start_day, start_hour, end_year,
            end_month, end_day, and end_hour. The dictionary is used for
            template replacement in plot titles and output paths.
        rel_channels_dict: The relative channels dictionary to map
            relative channels to actual data channels. Its keys are the
            relative channels, and its values are the actual data
            channels. (In this case, the mapping is reversed later to
            allow easy conversion from data channel to relative
            channel.)
        custom_vars: Dictionary containing custom variables to be
            replaced in title and output path templates. Its keys are
            %VAR% variables without the percent sign, and its values are
            what should take their places. For instance, given
            { "TESTVAR": "test123" }, the template "%TESTVAR%" should be
            replaced with "test123". By default, this is set to
            None - this argument is optional if there are no custom
            variables.
        make_dirs: Boolean indicating whether to automatically create
            output path directories or not. This defaults to False to
            ensure that the path specified is correct.
    
    Returns:
        A string with %VAR% variables replaced with the appropriate
        value or constant. Some %VAR% variables may not be replaced if
        they do not exist, or certain conditions are not met.
    """
    # Make a working copy for our use.
    plot_dict_copy = copy.deepcopy(plot_dict)
    plot_dict = plot_dict_copy
    
    # Check for iuse - if it doesn't exist, warn about the inability
    # to check data assimilation.
    if not isset("iuse", data_dict):
        warn("No iuse found in data_dict!")
        warn("Note that to cull any invalid values or display assimilation")
        warn("status, iuse must be part of the data to be read.")
    
    # Loop through the plot IDs
    for plot_id in plot_dict:
        # Keep track of the total number of plots
        total_plots = len(plot_dict[plot_id]["plots"])
        
        # Convenience variable
        plot = plot_dict[plot_id]
        
        # Pull plot sizing settings
        plot_dpi = plot["settings"]["dpi"]
        plot_target_size = plot["settings"]["target_size"]
        
        # Solve for correct figsize and set it up
        fig = plt.figure(figsize=(plot_target_size[0] / plot_dpi, plot_target_size[1] / plot_dpi), dpi = plot_dpi)
        
        # Check for a title
        if isset("title", plot):
            # Convenience variable
            plot_title = plot["title"]
            
            # Perform title template replace
            plot_title = title_output_replace(plot_title, metadata_dict, data_dict, rel_channels_dict, True, custom_vars)
            
            # Do we have an %ASSIMILATION_STATUS% placeholder?
            if "%ASSIMILATION_STATUS%" in plot["title"]:
                # Check for iuse
                if isset("iuse", data_dict):
                    # Initialize a variable for storing 
                    iuse_state = None
                    
                    # Read iuse and determine if there are any conflicts
                    for prefix in VALID_PREFIX:
                        if data_dict["iuse"][prefix][-1] == -1:
                            if iuse_state and iuse_state != -1:
                                warn("Assimilation state mismatch - last element uses %i instead of %i! (Changing to former value.)" % (data_dict["iuse"][prefix][-1], iuse_state))
                            iuse_state = -1
                        else:
                            if iuse_state and iuse_state == -1:
                                warn("Assimilation state mismatch - last element uses %i instead of %i! (Changing to former value.)" % (data_dict["iuse"][prefix][-1], iuse_state))
                            iuse_state = data_dict["iuse"][prefix][-1]
                    
                    # Check to ensure iuse_state has been set!
                    if not iuse_state:
                        die("Assimilation state could not be updated! (No prefixes found?)")
                    
                    # Now check the last element - if -1, it's not assimilated!
                    if iuse_state == -1:
                        fig.text(0.67, 0.948, "Not Assimilated", ha="center", va="bottom", size="x-large",color="red")
                    else:
                        fig.text(0.67, 0.948, "Assimilated", ha="center", va="bottom", size="x-large",color="green")
                else:
                    # No iuse, so we can't figure out assimilation...
                    warn("Unable to determine assimilation!")
                    fig.text(0.67, 0.948, "Unknown (??)", ha="center", va="bottom", size="x-large",color="orange")
        
        # Add the plot title to the plot
        fig.suptitle(plot_title, fontsize=18)
        
        # Adjust spacing so that the plot title has some room!
        #   hspace - the amount of height reserved for white space
        #            between subplots
        #   left - the left side of the subplots of the figure
        #   top - the top of the subplots of the figure
        plt.subplots_adjust(hspace = 1.2, left=0.15, top=0.88)
        
        # Loop through subplot indexes
        for subplotIndex in xrange(0, len(plot["plots"])):
            # Add a subplot - select position of subplot based on index
            axe = fig.add_subplot(total_plots, 1, subplotIndex + 1)
            
            # Grab the correct subplot ID (aka the key)
            subplotIDKey = fetch_key_from_subplot_dict(plot["plots"][subplotIndex])
            
            # Convenience variable
            subplot = plot["plots"][subplotIndex][subplotIDKey]
            
            # Do we have axes defined?
            if isset("axes", subplot):
                # Do we have an X axis defined?
                if isset("x", subplot["axes"]):
                    # Note: X axis ticks setting disabled for now - setting
                    # number of ticks for the X axis tends to mess up the
                    # dates!
                    
                    # Check if a label is defined, and if so, make a label!
                    if isset("label", subplot["axes"]["x"]):
                        axe.xaxis.set_label_text(subplot["axes"]["x"]["label"])
                
                # Do we have a Y axis defined?
                if isset("y", subplot["axes"]):
                    # Check if number of ticks is defined, and if so, change # of ticks accordingly!
                    if isset("ticks", subplot["axes"]["y"]):
                        axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))
                    
                    # Check if a label is defined, and if so, make a label!
                    if isset("label", subplot["axes"]["y"]):
                        axe.yaxis.set_label_text(subplot["axes"]["y"]["label"])
            
            # Do we have the plot data defined?
            if isset("data", subplot):
                # Is the data for the X axis defined?
                # Without an X axis, we can't make a plot!
                if isset("x", subplot["data"]):
                    # Check to make sure the data is substituted!
                    # Validate by ensuring that the element is a list!
                    verify_x_data = True
                    
                    for eleID in xrange(0, len(subplot["data"]["x"])):
                        if (type(subplot["data"]["x"][eleID]) != list):
                            verify_x_data = False
                            break
                    
                    # If there's no data substituted in, substitute it
                    # in now.
                    if not verify_x_data:
                        plot_dict = subst_data(plot_dict, data_dict)
                        plot = plot_dict[plot_id]
                        subplot = plot["plots"][subplotIndex][subplotIDKey]
                    
                    # Is the data for the Y axis defined?
                    if isset("y", subplot["data"]):
                        # Check to make sure data has been substituted!
                        # Validate by ensuring that the element is a list!
                        verify_y_data = True
                        for eleID in xrange(0, len(subplot["data"]["y"])):
                            if (type(subplot["data"]["y"][eleID]) != list):
                                verify_y_data = False
                                break
                        
                        # If there's no data substituted in, substitute
                        # it in now.
                        if not verify_y_data:
                            plot_dict = subst_data(plot_dict, data_dict)
                            plot = plot_dict[plot_id]
                            subplot = plot["plots"][subplotIndex][subplotIDKey]
                        
                        # Check for post_processing functions
                        if isset("post_processing", subplot["data"]):
                            # Check if there is a post_processing
                            # function for the X data
                            if isset("x", subplot["data"]["post_processing"]):
                                # Apply the lambda function to the data!
                                subplot["data"]["x"][eleID_x] = post_processing_func_x(data_dict, subplot["data"]["x"][eleID_x], subplot["data"]["y"][eleID_y])
                                
                                # Apply the lambda function to the data,
                                # piece by piece! This takes each
                                # subarray in the X data array and
                                # applies the function to it.
                                for eleID_x in xrange(0, len(subplot["data"]["x"])):
                                    for eleID_y in xrange(0, len(subplot["data"]["y"])):
                                        if eleID_x < len(subplot["data"]["post_processing"]["x"]):
                                            # Define the function...
                                            exec "post_processing_func_x = lambda data,x,y: %s" % subplot["data"]["post_processing"]["x"]
                                            # ...and run it!
                                            subplot["data"]["x"][eleID_x] = post_processing_func_x(data_dict, subplot["data"]["x"][eleID_x], subplot["data"]["y"][eleID_y])
                                        else:
                                            warn("WARNING: Not enough post_processing functions for the X data.")
                            
                            # Check if there is a post_processing
                            # function for the Y data
                            if isset("y", subplot["data"]["post_processing"]):
                                # Warn about mutliple X
                                if len(subplot["data"]["x"]) > 1:
                                    warn("WARNING: Substitution of Y data may be unreliable if you use X due to multiple X.")
                                
                                # Apply the lambda function to the data,
                                # piece by piece! This takes each
                                # subarray in the Y data array and
                                # applies the function to it.
                                for eleID_x in xrange(0, len(subplot["data"]["x"])):
                                    for eleID_y in xrange(0, len(subplot["data"]["y"])):
                                        if eleID_y < len(subplot["data"]["post_processing"]["y"]):
                                            # Define the function...
                                            exec "post_processing_func_y = lambda data,x,y: %s" % subplot["data"]["post_processing"]["y"]
                                            # ...and run it!
                                            subplot["data"]["y"][eleID_x] = post_processing_func_y(data_dict, subplot["data"]["x"][eleID_x], subplot["data"]["y"][eleID_y])
                                        else:
                                            warn("WARNING: Not enough post_processing functions for the Y data.")
                        
                        plot_kwargs = {}
                        y_id = 0
                        plotted_graphs = 0
                        debug("y_id and plotted_graphs RESET to zero")
                        
                        # Loop through Y data arrays
                        for y_dat in subplot["data"]["y"]:
                            # Validate data length
                            if len(y_dat) != len(subplot["data"]["x"][0]):
                                warn("WARNING: Data length for X differs from data length for Y!")
                                warn("(Data length for X: %i; Data length for Y: %i)" % (len(subplot["data"]["x"][0]), len(y_dat)))
                            
                            # Check if the colors attribute was set!
                            if isset("colors", subplot["data"]):
                                # If the color is a string, make it into
                                # a list.
                                if type(subplot["data"]["colors"]) == str:
                                    subplot["data"]["colors"] = [ subplot["data"]["colors"] ]
                                
                                # Verify that there are enough colors
                                # for the data.
                                if y_id < len(subplot["data"]["colors"]):
                                    # Grab the color, and toss it into
                                    # the plot kwargs!
                                    l_color = subplot["data"]["colors"][y_id]
                                    plot_kwargs["color"] = l_color
                                else:
                                    if len(subplot["data"]["colors"]) != len(subplot["data"]["y"]):
                                        # Emit a warning...
                                        warn("WARNING: Not enough colors specified in the colors field for the data!")
                                        warn("Colors specified vs. amount of Y data: %i vs. %i" % (len(subplot["data"]["colors"]), len(subplot["data"]["y"])))
                            
                            # Filter out any invalid data (-9999.99)...
                            # ...but ensure that "iuse" exists first!
                            if isset("iuse", data_dict):
                                # Do we need to skip graphing (due to
                                # all of the values being bad)?
                                skip_graph = False
                                
                                # Loop through prefixes...
                                for prefix in VALID_PREFIX:
                                    # Check for negative iuses
                                    if any(iuse < 0 for iuse in data_dict["iuse"][prefix]):
                                        #debug("Detected -1 in iuse field!")
                                        
                                        # Check to see if all of the
                                        # values are bad
                                        bad_vals = [ y for y in y_dat if (y <= -9999) ]
                                        
                                        # Are they all bad apples?
                                        if len(bad_vals) == len(y_dat):
                                            # Take steps to make an
                                            # empty plot
                                            axe.xaxis_date()
                                            y_id += 1
                                            
                                            skip_graph = True
                                            break
                                        
                                        # Otherwise, just filter the data!
                                        replaced_y = [ np.nan if y <= -9999 else y for y in y_dat ]
                                        y_dat = replaced_y
                                        break
                            
                            # Check for a labels attribute...
                            if isset("labels", subplot["data"]):
                                # If the label is a string, convert it
                                # into a list!
                                if type(subplot["data"]["labels"]) == str:
                                    subplot["data"]["labels"] = [ subplot["data"]["labels"] ]
                                
                                # Ensure that we have enough labels
                                # for the data!
                                if y_id < len(subplot["data"]["labels"]):
                                    # Grab the label and perform substitution
                                    l_label = subplot["data"]["labels"][y_id]
                                    l_label = l_label.replace("%COLOR%", "")
                                    l_label = l_label.replace("%ENDCOLOR%", "")
                                    
                                    # Zero division detection
                                    if len(y_dat) == 0:
                                        # Set AVG and STDDEV to zero.
                                        AVG = 0
                                        STDDEV = 0
                                    else:
                                        # Filter out NaNs from the Y data...
                                        y_dat_no_nan = [value for value in y_dat if not math.isnan(value)]
                                        
                                        # Then perform statistics!
                                        AVG = round(sum(y_dat_no_nan) / len(y_dat_no_nan), 3)
                                        STDDEV = np.std([float(val) for val in y_dat_no_nan])
                                    
                                    # Now perform substitution!
                                    l_label = l_label.replace("%AVERAGE%", str(AVG))
                                    l_label = l_label.replace("%STDDEV%", str(STDDEV))
                                    plot_kwargs["label"] = l_label
                                else:
                                    if len(subplot["data"]["labels"]) != len(subplot["data"]["y"]):
                                        # Emit a warning...
                                        warn("WARNING: Not enough labels specified in the colors field for the data!")
                                        warn("Labels specified vs. amount of Y data: %i vs. %i" % (len(subplot["data"]["labels"]), len(subplot["data"]["y"])))
                            else:
                                # Set the label to nothing
                                l_label = ""
                            
                            # Check if skip_graph was set, and if so,
                            # reset it and skip
                            if skip_graph:
                                skip_graph = False
                                continue
                            
                            # Ensure that all X values are displayed
                            axe.set_xlim(left = mdates.date2num(subplot["data"]["x"][0][0]), right = mdates.date2num(subplot["data"]["x"][0][-1]))
                            
                            # Plot the values!
                            plt.plot(np.array(subplot["data"]["x"][0]), np.array(y_dat), **plot_kwargs)
                            
                            # Increment counters...
                            y_id += 1
                            plotted_graphs += 1
            
            # Indicate if subplot is empty or not!
            if plotted_graphs == 0:
                plt.text(0.5, 0.5, 'Data not available', horizontalalignment='center',
                        verticalalignment='center', fontsize=24,
                        transform=axe.transAxes)
            
            # Check to see if we have a legend defined...
            if isset("legend", subplot):
                legend_kwargs = {}
                
                # Make some room for the legend!
                box = axe.get_position()
                axe.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.9, box.height])
                
                # Set up the position to the left side of the plot, and
                # create the legend!
                if "title" in subplot["legend"]:
                    legend_kwargs["title"] = subplot["legend"]["title"]
                # bbox_to_anchor - the "bounding box" where the legend will anchor to
                # borderaxespad - the pad between the axes and legend border
                # handlelength - the length of the legend handles
                legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0, **legend_kwargs)
                
                # Make the legend title large!
                # (But only if the legend actually exists - if there's
                # no data, it goes *poof*...)
                if legend:
                    plt.setp(legend.get_title(),fontsize='large')
                
                # If there is no data, things tend to be weird... no
                # legend will be displayed. If that's the case, let's
                # make a fake legend!
                if plotted_graphs == 0:
                    rects = []
                    labels = []
                    
                    # Loop through colors and add a Patch object with 
                    # said color!
                    for c in subplot["data"]["colors"]:
                        rects.append(matplotlib.patches.Patch(fc=c, ec=c))
                    
                    # Add the labels back in!
                    for l in subplot["data"]["labels"]:
                        labels.append(l.replace("%AVERAGE%", "N/A"))
                        labels.append(l.replace("%STDDEV%", "N/A"))
                    
                    # Finally, add the fake legend to the plot!
                    ext_leg = plt.legend(rects, labels, loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0, **legend_kwargs)
            
            # If there's a subplot title, make one!
            if isset("title", subplot):
                axe.set_title(subplot["title"], fontsize='large')
            
            # Set the date format!
            axe.xaxis.set_major_formatter(mdates.DateFormatter('%d%b\n%Y'))
        
        # Change the default gray background to white
        fig.patch.set_facecolor('white')
        
        # Set the output path for the plot
        if isset("output", plot):
            # Perform substitution on the plot output path
            plot_output = plot["output"]
            plot_output = title_output_replace(plot_output, metadata_dict, data_dict, rel_channels_dict, False, custom_vars)
            
            # Check to see if the path exists!
            # ...but make sure there IS a path to check for!
            if os.path.dirname(plot_output).strip() != "":
                if not os.path.exists(os.path.dirname(plot_output)):
                    # Check to see if make_dirs is set, and if so,
                    # create the path directory.
                    if make_dirs:
                        info("Output path %s not found, creating directory." % os.path.dirname(plot_output))
                        mkdir_p(os.path.dirname(plot_output))
                    else:
                        critical("Output path %s not found! If you want PyRadmon to create" % os.path.dirname(plot_output))
                        critical("the directory for you, add --plot-make-dirs or add and set the")
                        critical("make_dirs in the config section of the config file to true.")
                        die("Output path %s not found!" % os.path.dirname(plot_output))
        else:
            warn("Output path not specified, will save to 'magical_plot_please_specify_output_path_next_time.png'!")
            plot_output = "magical_plot_please_specify_output_path_next_time.png"
        
        # Make and save the plot!
        plt.savefig(plot_output, facecolor=fig.get_facecolor(), edgecolor='none', figsize=((plot_target_size[0] + 0.0) / plot_dpi, (plot_target_size[1] + 0.0) / plot_dpi), dpi = plot_dpi)
        
        # Free it all!
        plt.close()

if __name__ == "__main__":
    # Use test data
    from enumerate import enumerate
    from data import *
    from test import *
    
    en = enumerate()
    dat = get_data(en, TEST_DATA_VARS, 4)

    import pprint, yaml
    plot(plot_dict, dat, metadata_dict)
