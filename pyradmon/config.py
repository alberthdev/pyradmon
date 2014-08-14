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
# Configuration Library -
#   library for loading and saving configuration
# 

from core import *
from data import SPECIAL_FIELDS, VALID_PREFIX

import textwrap
import yaml
import traceback

import datetime

import copy



try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def load(config_file):
    try:
        cf_fh = open(config_file, "r")
        config_dict = yaml.load(cf_fh, Loader=Loader)
        cf_fh.close()
    except IOError:
        error("ERROR: Could not read configuration file!")
        return None
    except yaml.parser.ParserError:
        error("ERROR: Could not parse configuration file!")
        return None
    except:
        error("ERROR: Something bad occurred...")
        return None
    
    # We made it!
    # Now check for a config section...
    pyradmon_config = config_dict.pop("config", None)
    return [pyradmon_config, config_dict]

def save(config_file, pyradmon_config, config_dict):
    final_dict = copy.deepcopy(config_dict)
    if pyradmon_config:
        final_dict["config"] = pyradmon_config
    try:
        cf_fh = open(config_file, "w")
        yaml.dump(final_dict, cf_fh, Dumper=Dumper)
        cf_fh.close()
    except IOError:
        error("ERROR: Could not write configuration file!")
        return False
    except:
        exception("ERROR: Something bad occurred...")
        return False
    return True

base_directory    = "MERRA2/"
experiment_id     = "d5124_m2_jan91"

# postprocess builds 2 variables from current config:
#   -> the opts dictionary for enumerate.enumerate()
#   -> data variable list for data.get_data()
#   -> data_assim_only for data.get_data()
def postprocess_config(pyradmon_config):
    copy_vars    = [
                       'data_path_format',
                       'experiment_id',
                   ]
    process_vars = [
                    'data_start_date',
                    'data_end_date',
                    
                    'data_instrument_sat',
                    
                    'data_step',
                    'data_time_delta',
                    
                    'data_columns', # may be deprecated thanks to data variable list gen
                    'data_channels',
                    'data_assim_only',
                   ]
    #############################################
    ## Opts dictionary for enumerate.enumerate()
    #############################################
    
    if pyradmon_config == None:
        edie("ERROR: No PyRadmon configuration found! A configuration must be defined to run.")
    
    enum_opts_dict = {}
    
    if 'data_start_date' in pyradmon_config:#                                       \O/ <<^^^^^^^^^^^^^^^^^^^^^^
        # FORMAT: YYYY-MM-DD HHz                                                     |   ^ yay for alignment!  ^
        enum_opts_dict['start_year']  = int(pyradmon_config["data_start_date"][:4])#/ \  ^^^^^^^^^^^^^^^^^^^^^^^
        enum_opts_dict['start_month'] = int(pyradmon_config["data_start_date"][5:7])###
        enum_opts_dict['start_day']   = int(pyradmon_config["data_start_date"][8:10])###
        enum_opts_dict['start_hour']  = int(pyradmon_config["data_start_date"][11:13])###
    
    if 'data_end_date' in pyradmon_config:
        # FORMAT: YYYY-MM-DD HHz
        enum_opts_dict['end_year']    = int(pyradmon_config["data_end_date"][:4])
        enum_opts_dict['end_month']   = int(pyradmon_config["data_end_date"][5:7])
        enum_opts_dict['end_day']     = int(pyradmon_config["data_end_date"][8:10])
        enum_opts_dict['end_hour']    = int(pyradmon_config["data_end_date"][11:13])
    
    if 'data_instrument_sat' in pyradmon_config:
        enum_opts_dict['instrument_sat'] = pyradmon_config['data_instrument_sat']
    
    if 'data_step' in pyradmon_config:
        enum_opts_dict['data_type'] = pyradmon_config['data_step']
    
    if 'data_time_delta' in pyradmon_config:
        delta_dict = {}
        fields = [ "seconds", "minutes", "hours", "days", "weeks" ]
        # Initialize them all to zero...
        for field in fields:
            delta_dict[field] = 0
            
        # ...so that we can add them later!
        # Instead of setting them equal, we can just do this instead.
        # That way, something like "2h 5m 1s 1m" is possible.
        # (The adding way allows us to interpret this as "2h 6m 1s",
        # whereas the other way would interpret it as "2h 1m 1s".)
        for delta in pyradmon_config['data_time_delta'].split(" "):
            #  s: seconds    m: minutes    h: hours    d: days
            #  w: weeks      M: months     y: years
            if delta[-1] == "s":
                delta_dict["seconds"] += int(delta[:-1])
            if delta[-1] == "m":
                delta_dict["minutes"] += int(delta[:-1])
            if delta[-1] == "h":
                delta_dict["hours"]   += int(delta[:-1])
            if delta[-1] == "d":
                delta_dict["days"]    += int(delta[:-1])
            if delta[-1] == "w":
                delta_dict["weeks"]   += int(delta[:-1])
            if delta[-1] == "M":
                delta_dict["days"]  += int(delta[:-1]) * 30.4375
            if delta[-1] == "y":
                # Hacky - since we can't use actual years, we use
                # 365 days instead.
                delta_dict["days"] += 365
        
        enum_opts_dict['time_delta'] = datetime.timedelta(**delta_dict)
        
    for copy_var in copy_vars:
        if copy_var in pyradmon_config:
            enum_opts_dict[copy_var] = pyradmon_config[copy_var]
    
    if 'data_columns' in pyradmon_config:
        enum_opts_dict['data_columns'] = [ x.strip() for x in pyradmon_config['data_columns'].split(",") ]
    
    if 'data_all_channels' in pyradmon_config:
        enum_opts_dict['all_channels'] = pyradmon_config['data_all_channels']
    
    if 'data_channels' in pyradmon_config:
        if type(pyradmon_config['data_channels']) == str:
            enum_opts_dict['data_channels'] = [ x.strip() for x in pyradmon_config['data_channels'].split(",") ]
        else:
            enum_opts_dict['data_channels'] = str(pyradmon_config['data_channels'])
    
    if 'custom_vars' in pyradmon_config:
        enum_opts_dict['custom_vars'] = pyradmon_config['custom_vars']
        
    if 'make_dirs' in pyradmon_config:
        enum_opts_dict['make_dirs'] = pyradmon_config['make_dirs']
    
    if 'data_suppress_warnings' in pyradmon_config:
        enum_opts_dict['data_suppress_warnings'] = pyradmon_config['data_suppress_warnings']
    
    #############################################
    ## Data assim only flag for data.get_data()
    #############################################
    data_assim_only = None
    if 'data_assim_only' in pyradmon_config:
        enum_opts_dict['data_assim_only'] = pyradmon_config['data_assim_only']
    
    return enum_opts_dict

def postprocess_plot(plot_dict):
    #############################################
    ## Data variable list for data.get_data()
    #############################################
    data_var_list = []
    
    if plot_dict == None or len(plot_dict) <= 0:
        edie("ERROR: At least one plot definition is required to run.")
    
    for plotID in plot_dict:
        plot = plot_dict[plotID]
        for subplotDict in plot["plots"]:
            subplotID = subplotDict.keys()[0]
            subplot = subplotDict[subplotID]
            if not subplot["data"]["x"] in data_var_list:
                data_var_list.append(subplot["data"]["x"])
            for var in subplot["data"]["y"]:
                if not var in data_var_list:
                    data_var_list.append(var)
    
    if not "frequency" in data_var_list:
        data_var_list.append("frequency")
    
    if not "iuse" in data_var_list:
        data_var_list.append("iuse")
    
    return data_var_list

def postprocess(pyradmon_config, plot_dict):
    enum_opts_dict = postprocess_config(pyradmon_config)
    data_var_list = postprocess_plot(plot_dict)
    
    return (enum_opts_dict, data_var_list)

def gen_channel_list_generator(chan_arr):
    for chan_entry in chan_arr:
        if "-" in chan_entry:
            num_entry = [ int(num) for num in chan_entry.split("-") ]
            for i in xrange(num_entry[0], num_entry[1]+1): yield i 
        else:
            yield int(chan_entry)

def gen_channel_list(chan_arr):
    return list(gen_channel_list_generator(chan_arr))

def validate_config(pyradmon_config):
    # Validate pyradmon_config
    required_var_list = [
                            'data_path_format',
                            'experiment_id',
                            'data_start_date',
                            'data_end_date',
                            'data_instrument_sat',
                            'data_step',
                            'data_time_delta',
                            'data_columns',
                            'data_channels',
                            'data_assim_only',
                        ]
    
    if pyradmon_config == None:
        edie("ERROR: No PyRadmon configuration found! A configuration must be defined to run.")
    
    if 'data_start_date' in pyradmon_config:
        # FORMAT: YYYY-MM-DD HHz
        if not (pyradmon_config["data_start_date"][:4].isdigit() and \
            pyradmon_config["data_start_date"][5:7].isdigit() and \
            pyradmon_config["data_start_date"][8:10].isdigit() and \
            pyradmon_config["data_start_date"][11:13].isdigit()):
            edie("ERROR: Start date '%s' specified in data_start_date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_config["data_start_date"])
    
    if 'data_end_date' in pyradmon_config:
        # FORMAT: YYYY-MM-DD HHz
        if not (pyradmon_config["data_end_date"][:4].isdigit() and \
            pyradmon_config["data_end_date"][5:7].isdigit() and \
            pyradmon_config["data_end_date"][8:10].isdigit() and \
            pyradmon_config["data_end_date"][11:13].isdigit()):
            edie("ERROR: End date '%s' specified in data_end_date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_config["data_end_date"])
        
    ## Skip: data_instrument_sat
    
    if 'data_step' in pyradmon_config:
        if not ((pyradmon_config['data_step'] == "anl") or \
            (pyradmon_config['data_step'] == "ges") or \
            (pyradmon_config['data_step'] == "anl|ges") or \
            (pyradmon_config['data_step'] == "ges|anl")):
            edie("ERROR: Data step '%s' specified in data_step is not valid! Must either be 'anl', 'ges', or the two combined with a pipe ('anl|ges')." % pyradmon_config["data_step"])
    
    if 'data_time_delta' in pyradmon_config:
        dtd_split = pyradmon_config['data_time_delta'].split(" ")
        unit_valid = [ "s", "w", "m", "M", "h", "y", "d" ]
        
        for dtd in dtd_split:
            #  s: seconds    m: minutes    h: hours    d: days
            #  w: weeks      M: months     y: years
            if not ( (dtd[-1] in unit_valid) and (dtd[:-1].isdigit()) ):
                edie("ERROR: Invalid delta time '%s' specified in data_delta_time! Must be a # followed by a valid unit letter. ([s]ecs, [m]inutes, [h]ours, [d]ays, [w]eeks, [M]onths, [y]ears)" % pyradmon_config["data_delta_time"])
    
    # data_columns - may be deprecated
    if 'data_columns' in pyradmon_config:
        for data_column in pyradmon_config['data_columns'].split(","):
            data_column = data_column.strip()
            if not data_column in SPECIAL_FIELDS:
                if not ((data_column.startswith("ges|") or data_column.startswith("anl|"))):
                    edie("ERROR: Invalid data column '%s' specified in data_columns! Must have ges| or anl| as a prefix." % data_column)
    
    if 'data_channels' in pyradmon_config:
        if type(pyradmon_config['data_channels']) == str:
            for data_channel in pyradmon_config['data_channels'].split(","):
                data_channel = data_channel.strip()
                
                if not ( (data_channel.isdigit()) or \
                    ( (len(data_channel.split("-")) == 2) and data_channel.split("-")[0].isdigit() and data_channel.split("-")[1].isdigit() ) ):
                    edie("ERROR: Invalid data channel '%s' specified in data_channels! Must be a number or a numeric range (#-#)." % data_channel)
        elif type(pyradmon_config['data_channels']) == int:
            # All good!
            pass
        else:
            edie("ERROR: Invalid data channel '%s' specified in data_channels! Must be a number or a numeric range (#-#)." % data_channel)
    
    if 'custom_vars' in pyradmon_config:
        if not type(pyradmon_config['custom_vars']) == dict:
            edie("ERROR: Invalid custom_vars entry! Must be a dictionary with valid key/value pairs.")
    
    if 'data_assim_only' in pyradmon_config:
        if type(pyradmon_config['data_assim_only']) != bool:
            edie("ERROR: Invalid data assimilation selection flag '%s' specified in data_assim_only! Must be a bool." % str(pyradmon_config["data_assim_only"]))

def validate_plot(plot_dict):
    ## Plot dictionary verification
    
    # Check if we have at least one plot
    if plot_dict == None or len(plot_dict) <= 0:
        edie("ERROR: At least one plot definition is required to run.")
    
    # required
    #plot_dpi = plot["settings"]["dpi"]
    #plot_target_size = plot["settings"]["target_size"]
    
    for plotID in plot_dict:
        plot = plot_dict[plotID]
        if not ( ("dpi" in plot["settings"]) and ((type(plot["settings"]["dpi"]) == int) or (plot["settings"]["dpi"].isdigit())) ):
            edie("ERROR: Plot DPI must be specified and valid for plot '%s'." % plotID)
        if not ( ("target_size" in plot["settings"]) and (type(plot["settings"]["target_size"][0]) == int) and (type(plot["settings"]["target_size"][1]) == int) ):
            edie("ERROR: Plot size must be specified and valid for plot '%s'." % plotID)
        if isset("output", plot):
            if type(plot["output"]) != str:
                edie("ERROR: Output file '%s' is not a str for plot '%s'." % (str(plot["output"]), plotID))
        if isset("title", plot):
            if type(plot["title"]) != str:
                edie("ERROR: Title '%s' is not a str for plot '%s'." % (str(plot["title"]), plotID))
        if not (len(plot["plots"]) > 0):
            edie("ERROR: At least one inner plot definition is required to run.")
        for subplotDict in plot["plots"]:
            if len(subplotDict) != 1:
                edie("ERROR: Invalid number of subplot IDs for a single subplot field.")
            subplotID = subplotDict.keys()[0]
            subplot = subplotDict[subplotID]
            
            axes = [ "x", "y" ]
            
            if isset("axes", subplot):
                for axe in axes:
                    if isset(axe, subplot["axes"]):
                        if isset("label", subplot["axes"][axe]):
                            if type(subplot["axes"][axe]["label"]) != str:
                                edie("ERROR: Label for axis %s, '%s', is not a str for subplot '%s'." % (axe.upper(), str(subplot["axes"][axe]["label"]), subplotID))
                        if isset("ticks", subplot["axes"][axe]):
                            if type(subplot["axes"][axe]["ticks"]) != int:
                                edie("ERROR: Ticks for axis %s, '%s', is not an int for subplot '%s'." % (axe.upper(), str(subplot["axes"][axe]["ticks"]), subplotID))
            
            if not ("data" in subplot):
                edie("ERROR: No data field specified for subplot '%s'." % subplotID)
            
            if isset("labels", subplot["data"]):
                for label in subplot["data"]["labels"]:
                    if type(label) != str:
                        edie("ERROR: Label '%s' is not of type str! (Subplot '%s')" % (str(label), subplotID))
            if isset("colors", subplot["data"]):
                for color in subplot["data"]["colors"]:
                    if type(color) != str:
                        edie("ERROR: Color '%s' is not of type str! (Subplot '%s')" % (str(color), subplotID))
            if (not "x" in subplot["data"]):
                edie("ERROR: No X data specified for subplot '%s'." % subplotID)
            if (not "y" in subplot["data"]):
                edie("ERROR: No Y data specified for subplot '%s'." % subplotID)
            
            # TODO use VALID_PREFIX in the future to verify prefix, like anl/ges
            
            for axe in axes:
                if type(subplot["data"][axe]) == str:
                    if not (subplot["data"][axe] in SPECIAL_FIELDS):
                        if not (subplot["data"][axe].startswith("anl") or subplot["data"][axe].startswith("ges")):
                            edie("ERROR: %s data field '%s' does not start with 'anl' or 'ges' for subplot '%s'." % (axe.upper(), subplot["data"][axe], subplotID))
                elif type(subplot["data"][axe]) == list:
                    for field in subplot["data"][axe]:
                        if not (type(field) == str):
                            edie("ERROR: %s data field '%s' is not a str (in list of fields) for subplot '%s'." % (axe.upper(), str(field), subplotID))
                        if not (field in SPECIAL_FIELDS):
                            if not (field.startswith("anl") or field.startswith("ges")):
                                edie("ERROR: %s data field '%s' does not start with 'anl' or 'ges' for subplot '%s'." % (axe.upper(), field, subplotID))
                else:
                    edie("ERROR: %s data '%s' is not a valid type of str or list for subplot '%s'." % (axe.upper(), str(subplot["data"][axe]), subplotID))
            
            if isset("legend_title", subplot):
                if type(subplot["legend_title"]) != str:
                    edie("ERROR: Legend title '%s' is not a str for subplot '%s'." % (str(subplot["legend_title"]), subplotID))
            
            if isset("title", subplot):
                if type(subplot["title"]) != str:
                    edie("ERROR: Subplot title '%s' is not a str for subplot '%s'." % (str(subplot["title"]), subplotID))
                
def validate(pyradmon_config, plot_dict):
    validate_config(pyradmon_config)
    validate_plot(plot_dict)

if __name__ == "__main__":
    from test import *
    validate(metadata_dict, plot_dict)
    print "test.py metadata_dict and plot_dict validated"
