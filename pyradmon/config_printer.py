#!/usr/bin/env python
# PyRadmon v1.0 - Python Radiance Monitoring Tool
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
# Configuration Display Library -
#   library for displaying currently loaded configuration
# 

from config import validate
from core import isset, get_key_press
import textwrap


# Some constants
PYRADMON_CONFIG_DICT = {
                            "base_directory"     : "Base data directory",
                            "experiment_id"      : "Experiment ID",
                            "data_start_date"    : "Start date (YYYY-MM-DD HHz)",
                            "data_end_date"      : "End date (YYYY-MM-DD HHz)",
                            "data_instrument_sat": "Instrument/Satellite ID",
                            "data_step"          : "Data type/step",
                            "data_time_delta"    : "Data time interval",
                            "data_columns"       : "Data columns",
                            "data_channels"      : "Data channels",
                            "data_assim_only"    : "Use assimilated data only?",
                       }

# For your sanity and my sanity, please do not read this code.
# It is really messy, hacky, and it may make you want to do a headdesk.
# If you decide to proceed past this point, I am not liable for your
# insanity!
# 
# ...I'm kidding. But it's a real mess down there, so beware!
def print_table(table_dict, pause = True, table_debug = False):
    max_widths = []
    max_cols = 0
    for row in table_dict:
        cols = 0
        for col in row:
            if col != "!":
                cols += 1
        if max_cols < cols:
            max_cols = cols
    
    for colIndex in xrange(0, max_cols):
        max_arr = []
        for row in table_dict:
            if len(row) - 1 >= colIndex:
                col_str = str(row[colIndex])
                if "\n" in col_str:
                    #print "Using parts: %i" % max([len(col_part) for col_part in col_str.split("\n")])
                    max_arr.append(max([len(col_part) for col_part in col_str.split("\n")]))
                else:
                    max_arr.append(len(str(row[colIndex])))
                #print len(str(row[colIndex]))
        max_widths.append(max(max_arr))
                
        #max_widths.append(max([len(str(row[colIndex])) if len(row) - 1 >= colIndex else 0 for row in table_dict]) + 2)
    #print max_widths
    
    # Find the "true" maximums
    line_max_widths = []
    for row in table_dict:
        col_id = 0
        line_max_widths.append(sum([len(str(x)) for x in row]))
    
    line_max_width = max(line_max_widths)
    
    # col
    col_max_widths = []
    for colIndex in xrange(0, max_cols):
        max_arr = []
        for row in table_dict:
            if len(row) - 1 >= colIndex:
                col_str = str(row[colIndex])
                if "\n" in col_str:
                    #print "Using parts: %i" % max([len(col_part) for col_part in col_str.split("\n")])
                    max_arr.append(max([len(col_part) for col_part in col_str.split("\n")]))
                else:
                    max_arr.append(len(str(row[colIndex])))
                #print len(str(row[colIndex]))
        col_max_widths.append(max(max_arr))
    
    max_widths = [ width+1 for width in max_widths ]
    
    total_width = sum(max_widths)
    
    boldline = ("=" * (sum(max_widths) + 11))
    line = ("-" * (sum(max_widths) + 11))
    plusline = ("+" * (sum(max_widths) + 11))
    
    print boldline
    print "| " + "Plot Configuration".ljust(sum(max_widths)+8) + "|"
    print boldline
    
    col_buffer = {}
    
    row_i = 0
    col_i = 0
    
    for row in table_dict:
        col_i = 0
        
        row = [ str(x) for x in row ]
        
        for col in row:
            if col == "":
                col_i += 1
                continue
            if col_i not in col_buffer:
                col_buffer[col_i] = []
            if "\n" in col:
                col_split = col.split("\n")
                #print col_split
                for col_part in col_split:
                    col_buffer[col_i].append(col_part)
            else:
                col_buffer[col_i].append(col)
            col_i += 1
        
        col_i = 0
        print_str = ""
        done_printing = False
        print_plusline = False
        line_mask = [ True if (x in col_buffer) and (len(col_buffer[x]) > 0) and (col_buffer[x][0] != "") \
                        else False for x in xrange(0, len(max_widths)) ]
        #print line_mask
        #raw_input()
        while not done_printing:
            print_str = "| "
            all_len = [ len(col_buffer[x]) if x in col_buffer else 0 for x in xrange(0, len(max_widths)) ]
            
            if sum(all_len) == 0:
                done_printing = True
                break
            
            for col_i in xrange(0, len(max_widths)):
                #print col_buffer
                blank = False
                #raw_input()
                #all_len = [ len(col_buffer[x]) if x in col_buffer else 0 for x in xrange(0, len(max_widths)) ]
                
                #if sum(all_len) == 0:
                #    done_printing = True
                    #break
                
                if (col_i in col_buffer) and (len(col_buffer[col_i]) > 0):
                    #print "part"
                    if col_buffer[col_i][0] == "!":
                        print_plusline = True
                        line_mask[col_i] = False
                        print_str += " ".ljust(max_widths[col_i])
                        col_buffer[col_i].pop(0)
                    else:
                        print_str += (col_buffer[col_i].pop(0)).ljust(max_widths[col_i])
                else:
                    print_str += " ".ljust(max_widths[col_i])
                    blank = True
                
                if col_i == len(max_widths) - 1:
                    print_str += "|"
                else:
                    #if (not blank) or ( (col_i in col_buffer) and (len(col_buffer[col_i]) > 0) ):
                    #if ( (col_i + 1 in col_buffer) and (len(col_buffer[col_i + 1]) > 0) ):
                    if col_i < len(max_widths) - 1:
                        if (line_mask[col_i + 1]):
                            #print "OK"
                            #print "%i: %s" % (col_i + 1, col_buffer[col_i + 1])
                            if (col_i in col_buffer) and (len(col_buffer[col_i + 1]) > 0) and (col_buffer[col_i + 1][0] == "!"):
                                print_str += "  "
                            elif sum(line_mask[:col_i]) == 0:
                                print_str += "| "
                            else:
                                print_str += "| "
                        # if nothing up to this part, print a bar!
                        # we can print a bar if it's empty before, NOT
                        # if it's empty after!
                        elif sum(line_mask[:col_i+1]) == 0:
                            print_str += "| "
                        else:
                            #print "NO"
                            print_str += "  "
                
            print print_str
        
        # Print line seps
        if print_plusline:
            cur_line = "|"
            for field_id in xrange(0, len(max_widths)):
                if line_mask[field_id] == True:
                    cur_line += "+" * (max_widths[field_id] + 1)
                    if table_debug:
                        cur_line = cur_line[:-2] + "PA"
                else:
                    if field_id > sum(line_mask) - 1:
                        cur_line += "+" * (max_widths[field_id] + 1)
                        if table_debug:
                            cur_line = cur_line[:-2] + "PB"
                    elif field_id < len(max_widths) - 1:
                        if line_mask[field_id] == True:
                            cur_line += "+" * (max_widths[field_id] + 1)
                            if table_debug:
                                cur_line = cur_line[:-2] + "PC"
                        else:
                            cur_line += " " * (max_widths[field_id] + 1)
                            if table_debug:
                                cur_line = cur_line[:-2] + "PD"
                    else:
                        cur_line += " " * (max_widths[field_id] + 1)
                        if table_debug:
                            cur_line = cur_line[:-2] + "PE"
                if (field_id > sum(line_mask) - 1) and (field_id != len(max_widths) - 1):
                    cur_line += "+"
                elif field_id < len(max_widths) - 1:
                    #if line_mask[field_id + 1] == True:
                    #    cur_line += "|"
                    #else:
                    #    cur_line += "+"
                    if sum(line_mask[:field_id]) == 0:
                        cur_line += "|"
                    else:
                        cur_line += "+"
            cur_line += "|"
            print cur_line
            print_plusline = False
        else:
            # Check if this is the last line/row
            if row_i == len(table_dict) - 1:
                cur_line = "-"
            else:
                cur_line = "|"
            
            # Iterate columns
            for field_id in xrange(0, len(max_widths)):
                if False and line_mask[field_id] == True:
                    cur_line += "-" * (max_widths[field_id] + 1)
                    if table_debug:
                        cur_line = cur_line[:-1] + "A"
                else:
                    # Check... I don't even know... but hey, it works!
                    if field_id > sum(line_mask) - 1:
                        cur_line += "-" * (max_widths[field_id] + 1)
                        if table_debug:
                            cur_line = cur_line[:-1] + "B"
                    # Check if this is the last line/row
                    elif row_i == len(table_dict) - 1:
                        cur_line += "-" * (max_widths[field_id] + 1)
                        if table_debug:
                            cur_line = cur_line[:-1] + "C"
                    # Check if we are not at the last column yet
                    elif field_id < len(max_widths) - 1:
                        #if line_mask[field_id + 1] == True:
                        #    cur_line += "-" * (max_widths[field_id] + 1)
                        #    cur_line = cur_line[:-1] + "C"
                        #else:
                        if (row_i < len(table_dict) - 1) and (field_id <= len(table_dict[row_i+1]) - 1) and (str(table_dict[row_i+1][field_id]) != ""):
                            cur_line += "-" * (max_widths[field_id] + 1)
                        else:
                            cur_line += " " * (max_widths[field_id] + 1)
                        
                        if table_debug:
                            cur_line = cur_line[:-1] + "D"
                    else:
                        cur_line += " " * (max_widths[field_id] + 1)
                        if table_debug:
                            cur_line = cur_line[:-1] + "E"
                if (field_id > len(line_mask) - 1) and (field_id != len(max_widths) - 1):
                    cur_line += "-"
                elif field_id < len(max_widths) - 1:
                    #if line_mask[field_id + 1] == True:
                    #    cur_line += "|"
                    #else:
                    #    cur_line += "-"
                    #print "FID: %i | SUM: %i" % (field_id, sum(line_mask[:field_id+1]))
                    # Check if this is the last line/row
                    if row_i == len(table_dict) - 1:
                        cur_line += "-"
                    elif (line_mask[field_id + 1]):
                        if (field_id in col_buffer) and (len(col_buffer[field_id + 1]) > 0) and (col_buffer[field_id + 1][0] == "!"):
                            cur_line += "-"
                        else:
                            if (row_i < len(table_dict) - 1) and \
                                ( (field_id <= len(table_dict[row_i+1]) - 1) and (str(table_dict[row_i+1][field_id]) != "") ) or \
                                (field_id > len(table_dict[row_i+1]) - 1):
                                cur_line += "-"
                            else:
                                cur_line += "|"
                    elif (row_i < len(table_dict) - 1) and (field_id <= len(table_dict[row_i+1]) - 1) and (str(table_dict[row_i+1][field_id]) != ""):
                        cur_line += "-"
                    elif (sum(line_mask[:field_id+1]) == 0):
                        #if (row_i < len(table_dict) - 1) and (field_id <= len(table_dict[row_i+1]) - 1) and (str(table_dict[row_i+1][field_id]) != ""):
                        #    cur_line += "-"
                        #else:
                        #    cur_line += "|"
                        cur_line += "|"
                    else:
                        cur_line += "-"
            # Check if this is the last line/row
            if row_i == len(table_dict) - 1:
                cur_line += "-"
            else:
                cur_line += "|"
            #print col_buffer
            #print row
            print cur_line
            if pause:
                get_key_press()
        #raw_input()
        
        # RULES:
        # If remaining boxes are empty, don't print any more bars.
        # Line breaks:
        # For blank boxes with filled boxes to the right, print an
        # empty line for unfilled, line for filled.
        
        #print "| " + " ".ljust(col_width_1) + "| " + val_part.ljust(col_width_2) + "|"
        row_i += 1
    #print boldline
    
def display(pyradmon_config, plot_dict, pause = True, table_debug = False):
    validate(pyradmon_config, plot_dict, False)
    # PyRadmon Configuration
    if pyradmon_config:
        pyradmon_disp = []
        
        for key in PYRADMON_CONFIG_DICT:
            left_str = PYRADMON_CONFIG_DICT[key] + ":"
            if isset(key, pyradmon_config):
                if type(pyradmon_config[key]) == str:
                    right_str = pyradmon_config[key]
                elif type(pyradmon_config[key]) == list:
                    right_str = ", ".join(map(str,pyradmon_config[key]))
                elif type(pyradmon_config[key]) == bool:
                    right_str = "Yes" if pyradmon_config[key] else "No"
                else:
                    right_str = str(pyradmon_config[key]) + " [warn: unknown type]"
            else:
                right_str += "[Undefined]"
            pyradmon_disp.append([left_str, right_str])
        col_width_1 = max(len(row[0]) for row in pyradmon_disp) + 2
        col_width_2 = max(len(row[1]) for row in pyradmon_disp) + 2
        
        if col_width_2 > 34:
            col_width_2 = 34
            
        boldline = ("=" * (col_width_1 + col_width_2 + 5))
        line = ("-" * (col_width_1 + col_width_2 + 5))
        print boldline
        print "| " + "PyRadmon Configuration".ljust(col_width_1) + "  " + " ".ljust(col_width_2) + "|"
        print boldline
        print "| " + "Configuration".ljust(col_width_1) + "| " + "Value".ljust(col_width_2) + "|"
        print line
        for row in pyradmon_disp:
            shown = False
            for val_part in textwrap.wrap(row[1], col_width_2):
                if shown:
                    print "| " + " ".ljust(col_width_1) + "| " + val_part.ljust(col_width_2) + "|"
                else:
                    print "| " + row[0].ljust(col_width_1) + "| " + val_part.ljust(col_width_2) + "|"
                    shown = True
        print line
        if pause:
            get_key_press()
    # Plot dictionary config
    # ------------------------------------------------------------------
    # | Plot                                                           |
    # | [plot1_id]                                                     |
    # |----------------------------------------------------------------|
    # | Title                                                          |
    # |----------------------------------------------------------------|
    # | %INSTRUMENT_SAT%   %START_DATE%-%END_DATE%                     |
    # | Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%     |
    # | Global  All    %EXPERIMENT_ID%                                 |
    # |----------------------------------------------------------------|
    # | Output                                                         |
    # |----------------------------------------------------------------|
    # | my_awesome_plot.png                                            |
    # |----------------------------------------------------------------|
    # | Settings      | DPI:   | 50                                    |
    # |               |------------------------------------------------|
    # |               | Target | 595x700 px                            |
    # |               | size:  |                                       |
    # |---------------|------------------------------------------------|
    # | Subplot       | Title: | None                                  |
    # | [subplot1_id] |------------------------------------------------|
    # |               | Data:  | (x,y):      | (timestamp,             |
    # |               |        |             |  ges|bc_total|mean)     |
    # |               |        |---------------------------------------|
    # |               |        | Label:      | Avg (K)                 |
    # |               |        |             | %AVERAGE%               |
    # |               |        |---------------------------------------|
    # |               |        | Line color: | red                     |
    # |               |        |+++++++++++++++++++++++++++++++++++++++|
    # |               |        | (x,y):      | (timestamp,             |
    # |               |        |             |  ges|bc_total|stddev)   |
    # |               |        |---------------------------------------|
    # |               |        | Label:      | Sdv (K)                 |
    # |               |        |             | %AVERAGE%               |
    # |               |        |---------------------------------------|
    # |               |        | Line color: | blue                    |
    # |               |------------------------------------------------|
    # |               | Axes:  | X:          | Label: None             |
    # |               |        |             |-------------------------|
    # |               |        |             | Ticks: 6                |
    # |               |        |---------------------------------------|
    # |               |        | Y:          | Label: None             |
    # |               |        |             |-------------------------|
    # |               |        |             | Ticks: 5                |
    # |               |------------------------------------------------|
    # |               | Legend | Total Bias                            |
    # |               | Title: |                                       |
    # ------------------------------------------------------------------
    # 
    
    # table_data[ROW][COL] (c,r)
    # ---------------------
    # | 00 | 01 | 02 | 03 |
    # ---------------------
    # | 10 | 11 | 12 | 13 |
    # ---------------------
    # | 20 | 21 | 22 | 23 |
    # ---------------------
    # | 30 | 31 | 32 | 33 |
    # ---------------------
    for plotID in sorted(plot_dict):
        table_data = []
        plot = plot_dict[plotID]
        table_data.append([ "Plot\n[%s]" % plotID ])
        
        table_data.append([ "Plot Title" ])
        
        # Now fill in actual data!
        if isset("title", plot):
            table_data.append([ plot["title"] ])
        else:
            table_data.append([ "None" ])
        
        table_data.append([ "Settings", "DPI:" ])
        table_data.append([ "", "Target\nsize:" ])
        if isset("settings", plot):
            if isset("dpi", plot["settings"]):
                table_data[3].append(plot["settings"]["dpi"])
            else:
                table_data[4].append("[Not specified]")
            if isset("target_size", plot["settings"]):
                table_data[4].append("%ix%i px" % (plot["settings"]["target_size"][0], plot["settings"]["target_size"][1]))
            else:
                table_data[4].append("[Not specified]")
        else:
            table_data[3].append("[Not specified]")
            table_data[4].append("[Not specified]")
        
        # Subplots...
        for subplotIndex in xrange(0, len(plot["plots"])):
            # Set our subplot!
            subplotID = plot["plots"][subplotIndex].keys()[0]
            subplot = plot["plots"][subplotIndex][subplotID]
            # Subplot header + title
            table_data_line = ["Subplot\n[%s]" % subplotID, "Title:"]
            if isset("title", subplot):
                table_data_line.append(subplot["title"])
            else:
                table_data_line.append("[Not specified]")
            table_data.append(table_data_line)
            
            # Data field: (x,y), line color, and label
            if isset("data", subplot):
                if isset("labels", subplot["data"]):
                    for i in xrange(0, len(subplot["data"]["y"])):
                        if i == 0:
                            table_data_line = ["",                          "Data:", "(x,y):"               ]
                        else:
                            table_data_line = ["",                          "",      "(x,y):"               ]
                        table_data_line.append("(%s,\n%s)" % (subplot["data"]["x"], subplot["data"]["y"][i]))
                        table_data.append(table_data_line)
                        
                        table_data_line = ["",                          "",      "Label:"               ]
                        table_data_line.append("%s" % subplot["data"]["labels"][i])
                        table_data.append(table_data_line)
                        
                        table_data_line = ["",                          "",      "Line Color:"          ]
                        if isset("colors", subplot["data"]):
                            table_data_line.append("%s" % subplot["data"]["colors"][i])
                        else:
                            table_data_line.append("[Not specified]")
                        
                        # Add a "!" to indicate a different line... but
                        # only if we have more than one Y field, and if
                        # we're not the last one...
                        if (len(subplot["data"]["y"]) > 1) and (i != len(subplot["data"]["y"]) - 1):
                            table_data_line.append("!")
                        table_data.append(table_data_line)
            
            if isset("axes", subplot):
                if isset("x", subplot["axes"]):
                    table_data_line = ["",                          "Axes:", "X:",          "Label:"]
                    if isset("label", subplot["axes"]["x"]):
                        table_data_line.append(subplot["axes"]["x"]["label"])
                    else:
                        table_data_line.append("[Not specified]")
                    
                    table_data.append(table_data_line)
                    
                    table_data_line = ["",                          "",      "",            "Ticks:"]
                    if isset("ticks", subplot["axes"]["x"]):
                        table_data_line.append(subplot["axes"]["x"]["ticks"])
                    else:
                        table_data_line.append("[Not specified]")
                    
                    table_data.append(table_data_line)
                else:
                    table_data_line = ["",                          "Axes:", "X:",          "Label:"]
                    table_data_line.append("[Not specified]")
                    table_data.append(table_data_line)
                    
                    table_data_line = ["",                          "",      "",            "Ticks:"]
                    able_data_line.append("[Not specified]")
                    table_data.append(table_data_line)
                
                if isset("y", subplot["axes"]):
                    table_data_line = ["",                          "",      "Y:",          "Label:"]
                    if isset("label", subplot["axes"]["y"]):
                        table_data_line.append(subplot["axes"]["y"]["label"])
                    else:
                        table_data_line.append("[Not specified]")
                    
                    table_data.append(table_data_line)
                    
                    table_data_line = ["",                          "",      "",            "Ticks:"]
                    if isset("ticks", subplot["axes"]["y"]):
                        table_data_line.append(subplot["axes"]["y"]["ticks"])
                    else:
                        table_data_line.append("[Not specified]")
                    
                    table_data.append(table_data_line)
                else:
                    table_data_line = ["",                          "",      "Y:",          "Label:"]
                    table_data_line.append("[Not specified]")
                    table_data.append(table_data_line)
                    
                    table_data_line = ["",                          "",      "",            "Ticks:"]
                    table_data_line.append("[Not specified]")
                    table_data.append(table_data_line)
            
            table_data_line = ["", "Legend\nTitle:" ]
            if isset("legend_title", subplot):
                table_data_line.append(subplot["legend_title"])
            else:
                table_data_line.append("[Not specified]")
            table_data.append(table_data_line)
            
        # Now we're ready to print!
        print_table(table_data, pause = pause, table_debug = table_debug)
            
        
    
