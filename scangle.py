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
# Scan Angle Plot Generator -
#   program for plotting the scan angles!
# 

import matplotlib
matplotlib.use('Agg', warn=False)
import matplotlib.pyplot as plt
import numpy as np

import pyradmon.enumerate as en
from pyradmon import dummymp
from pyradmon.core import *
from pyradmon.config import gen_channel_list

import sys
import copy
import datetime

from decimal import Decimal

from scangle_config import *

#######################################################################
# Functions
#######################################################################
def substVars(in_str, channel = 0, range_date = None):
    in_str = in_str.replace("%YEAR4%" , reference_year    .zfill(4))
    in_str = in_str.replace("%YEAR2%" , reference_year[2:].zfill(2))
    in_str = in_str.replace("%MONTH2%", reference_month   .zfill(2))
    in_str = in_str.replace("%DAY2%"  , reference_day     .zfill(2))
    in_str = in_str.replace("%HOUR2%" , reference_hour    .zfill(2))
    
    if range_date:
        in_str = in_str.replace("%RYEAR4%" , str(range_date.year)    .zfill(4))
        in_str = in_str.replace("%RYEAR2%" , str(range_date.year)[2:].zfill(2))
        in_str = in_str.replace("%RMONTH2%", str(range_date.month)   .zfill(2))
        in_str = in_str.replace("%RDAY2%"  , str(range_date.day)     .zfill(2))
        in_str = in_str.replace("%RHOUR2%" , str(range_date.hour)    .zfill(2))
    
    in_str = in_str.replace("%INSTRUMENT_SAT%", instrument_sat)
    in_str = in_str.replace("%EXPERIMENT_ID%", experiment_id)
    in_str = in_str.replace("%CHANNEL%", str(channel))
    
    return in_str

def postProcessDates(all_dates):
    max_arr_len = max([ len(arr) for arr in all_dates ])
    
    #print "Max array length: ",max_arr_len
    
    all_dates_tmp = all_dates
    all_dates_tmp2 = []
    
    for arr in all_dates_tmp:
        if len(arr) < max_arr_len:
            #print "Adjusting len %i to %i (adding %i)..." % (len(arr), max_arr_len, max_arr_len - len(arr))
            for n in xrange(0, max_arr_len - len(arr)):
                arr.append(0)
            #print "Adjusted: len %i == %i..." % (len(arr), max_arr_len)
        all_dates_tmp2.append(arr)
    
    all_dates = []
    
    for arr in all_dates_tmp2:
        all_dates.append(np.array(arr))
    
    return all_dates

#######################################################################
# Configuration Handling
#######################################################################
final_config = do_config()

data_path_format   = final_config["data_path_format"]
experiment_id      = final_config["experiment_id"]
instrument_sat     = final_config["instrument_sat"]
all_channels       = final_config["all_channels"]
channels           = final_config["channels"]

start_year         = final_config["start_year"]
start_month        = final_config["start_month"]
start_day          = final_config["start_day"]
start_hour         = final_config["start_hour"]

reference_year     = final_config["reference_year"]
reference_month    = final_config["reference_month"]
reference_day      = final_config["reference_day"]
reference_hour     = final_config["reference_hour"]

output_file        = final_config["output_file"]

mp_disable         = final_config["mp_disable"]
mp_priority_mode   = final_config["mp_priority_mode"]
mp_cpu_limit       = final_config["mp_cpu_limit"]

#DATA_PATH_FORMAT  = "/gpfsm/dnb51/projects/p14/scratch/%EXPERIMENT_ID%/ana/Y%YEAR4%/M%MONTH2%/%EXPERIMENT_ID%.ana.satbang.%YEAR4%%MONTH2%%DAY2%_%HOUR2%z.txt"
#EXPERIMENT_ID     = "e5110_fp"
#instrument_sat    = "amsua_n18"
#CHANNELS          = "1-15"

#START_YEAR        = "2014"
#START_MONTH       = "01"
#START_DAY         = "01"
#START_HOUR        = "00"

#REFERENCE_YEAR    = "2014"
#REFERENCE_MONTH   = "02"
#REFERENCE_DAY     = "28"
#REFERENCE_HOUR    = "00"

#OUTPUT_FILE       = "scan_angle_%EXPERIMENT_ID%_%instrument_sat%_ch%CHANNEL%.png"

#######################################################################
# Program
#######################################################################
reference_date = datetime.datetime(int(reference_year), int(reference_month), int(reference_day), int(reference_hour))
start_date = datetime.datetime(int(start_year), int(start_month), int(start_day), int(start_hour))
end_date = reference_date

#log.init(logging.INFO, sys.stdout)

if start_date > end_date:
    die("ERROR: Start date is more recent than end date (reference date)!")

if end_date - start_date < datetime.timedelta(days=30):
    info("Gathering data for the minimum 30 days - original range will still be in effect.")
    start_date_final = end_date - datetime.timedelta(days=30)
else:
    start_date_final = start_date

start_year        = start_date_final.year
start_month       = start_date_final.month
start_day         = start_date_final.day
start_hour        = start_date_final.hour
end_year          = end_date.year
end_month         = end_date.month
end_day           = end_date.day
end_hour          = end_date.hour

# all_channels

info("Enumerating...")
(files_to_read, stats_dict) = \
    en.enumerate(data_path_format=data_path_format, experiment_id = experiment_id, instrument_sat = instrument_sat, \
        start_year = start_year, start_month = start_month, start_day = start_day, start_hour = start_hour, \
        end_year = end_year, end_month = end_month, end_day = end_day, end_hour = end_hour, \
        data_type = None)

# Revert
start_year        = start_date.year
start_month       = start_date.month
start_day         = start_date.day
start_hour        = start_date.hour

#print stats_dict
#print files_to_read

chans = channels
if type(chans) == str:
    chans = [ x.strip() for x in chans.split(",") ]
else:
    chans = str(chans)

info("Reading data...")

if all_channels or len(list(gen_channel_list(chans))) > 1:
    if not all_channels:
        total_chans = len(list(gen_channel_list(chans)))
    file_data = {}
    multiple_chans = True
else:
    total_chans = 1
    file_data = []
    multiple_chans = False

final_data = {}

chan_list = []

for file_to_read in files_to_read:
    if file_to_read["instrument_sat"] != instrument_sat:
        warn("WARNING: Instrument/sat field does not match! Skipping invalid data. (Correct: %s | Invalid: %s)" % (instrument_sat, file_to_read['instrument_sat']))
        continue
    #print file_to_read
    with open(file_to_read["filename"], "r") as data_file:
        header_found = False
        data_chunk_done = False
        data_chunk = []
        
        for data_line in data_file:
            data_line = (' '.join(data_line.split())).split()
            #print data_line
            if not header_found:
                # Try to examine the header
                if len(data_line) == 4:
                    # Instrument/sat check
                    if data_line[1] != instrument_sat:
                        continue
                    current_chan = int(data_line[2])
                    if all_channels or any(chan == current_chan for chan in gen_channel_list(chans)):
                        # Channel found!
                        header_found = True
                        
                        if not current_chan in chan_list:
                            chan_list.append(current_chan)
                        #print "I/S: %s | Found channel %i!" % (data_line[1], current_chan)
            else:
                # Try to read in data!
                if len(data_line) == 10:
                    #val_array = [ Decimal(x) for x in data_line ]
                    val_array = [ float(x) for x in data_line ]
                    data_chunk += val_array
                elif len(data_line) == 0:
                    data_chunk_done = True
            
            if data_chunk_done:
                #print "Got data chunk! (len=%i)" % len(data_chunk)
                header_found = False
                data_chunk_done = False
                
                #print "dc", data_chunk
                #print len(data_chunk)
                
                if len(data_chunk) == 0:
                    print "ERROR: Could not get any data!"
                    sys.exit(1)
                
                # Data culling...
                while data_chunk[-1] == 0:
                    data_chunk.pop(-1)
                    
                    if len(data_chunk) == 0:
                        break
                
                if multiple_chans:
                    if current_chan in final_data:
                        print "WARNING: current_chan %i already found..." % current_chan
                    file_data[current_chan] = data_chunk
                else:
                    file_data = data_chunk
                
                data_chunk = []
            #raw_input()
    final_data[file_to_read["date"]] = copy.deepcopy(file_data)
    
#from pprint import pprint
#pprint(final_data)

info("Plotting data...")

if all_channels:
    chans = [ str(chan) for chan in chan_list ]

def plot_scangle(channel):
    fig = plt.figure(figsize=(595 / 50, 700 / 50), dpi = 50)
    
    #plt.subplots_adjust(hspace = 1.2, left=0.15, top=0.88)
    plt.subplots_adjust(hspace = 0.3, left=0.15, top=0.88)

    # 4 plots                   # SUBPLOT ID
    axe = fig.add_subplot(4, 1, 0 + 1)

    #axe.xaxis.set_label_text("X LABEL")
    # CUSTOM
    #axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))

    #axe.yaxis.set_label_text("Y LABEL")
    #print final_data[reference_date][1]
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), np.array(final_data[reference_date][channel]), color = "black")

    #legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0)
    #plt.setp(legend.get_title(),fontsize='large')
    
    subplot_title = "Fixed Angle Correction - %YEAR4%%MONTH2%%DAY2% (Single Day)"
    subplot_title = substVars(subplot_title, channel)
    
    axe.set_title(subplot_title, fontsize='large')
    
    #################################################################
    # 4 plots                   # SUBPLOT ID
    axe = fig.add_subplot(4, 1, 1 + 1)

    #axe.xaxis.set_label_text("X LABEL")
    # CUSTOM
    #axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))

    #axe.yaxis.set_label_text("Y LABEL")
    #print final_data[reference_date][1]
    idate = reference_date - datetime.timedelta(days=7)
    all_dates = []
    
    while idate < reference_date:
        if idate in final_data:
            plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray")
            all_dates.append(final_data[idate][channel])
        idate = idate + datetime.timedelta(hours=1)
    
    all_dates = postProcessDates(all_dates)
    
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), np.array(all_dates).mean(axis=0), color = "red")

    #legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0)
    #plt.setp(legend.get_title(),fontsize='large')
    
    subplot_title = "Fixed Angle Correction - %RYEAR4%%RMONTH2%%RDAY2% - %YEAR4%%MONTH2%%DAY2% (Last 7 Days)"
    subplot_title = substVars(subplot_title, channel, (reference_date - datetime.timedelta(days=7)))
    
    axe.set_title(subplot_title, fontsize='large')
    week_all_dates = np.array(all_dates)
    #################################################################
    # 4 plots                   # SUBPLOT ID
    axe = fig.add_subplot(4, 1, 2 + 1)

    #axe.xaxis.set_label_text("X LABEL")
    # CUSTOM
    #axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))

    #axe.yaxis.set_label_text("Y LABEL")
    #print final_data[reference_date][1]
    idate = reference_date - datetime.timedelta(days=30)
    all_dates = []
    
    while idate < reference_date:
        if idate in final_data:
            plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray")
            all_dates.append(final_data[idate][channel])
        idate = idate + datetime.timedelta(hours=1)
    
    all_dates = postProcessDates(all_dates)
    
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), np.array(all_dates).mean(axis=0), color = "lightgreen")

    #legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0)
    #plt.setp(legend.get_title(),fontsize='large')
    
    subplot_title = "Fixed Angle Correction - %RYEAR4%%RMONTH2%%RDAY2% - %YEAR4%%MONTH2%%DAY2% (Last 30 Days)"
    subplot_title = substVars(subplot_title, channel, (reference_date - datetime.timedelta(days=30)))
    
    axe.set_title(subplot_title, fontsize='large')
    
    month_all_dates = np.array(all_dates)
    #################################################################
    # 4 plots                   # SUBPLOT ID
    axe = fig.add_subplot(4, 1, 3 + 1)

    #axe.xaxis.set_label_text("X LABEL")
    # CUSTOM
    #axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))

    #axe.yaxis.set_label_text("Y LABEL")
    #print final_data[reference_date][1]
    all_dates = []
    
    last_ele = len(final_data) - 1
    
    """for i, idate in enumerate(final_data):
        if i != last_ele:
            plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray")
        else:
            plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray", label = "Individual")
        all_dates.append(final_data[idate][channel])"""
    
    idate = start_date
    i = 0
    while idate < reference_date:
        if idate in final_data:
            plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray")
            all_dates.append(final_data[idate][channel])
        idate = idate + datetime.timedelta(hours=1)
    
    idate = idate - datetime.timedelta(days=1)
    plt.plot(np.array(range(1, len(final_data[idate][channel]) + 1)), np.array(final_data[idate][channel]), color = "gray", label = "Individual")
    
    earliest_date = start_date
    
    all_dates = postProcessDates(all_dates)
    
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), np.array(final_data[reference_date][channel]), color = "black", label="Most Recent")
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), month_all_dates.mean(axis=0), color = "lightgreen", label = "Last 30 Days (Mean)")
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), week_all_dates.mean(axis=0), color = "red", label = "Last 7 Days (Mean)")
    plt.plot(np.array(range(1, len(final_data[reference_date][channel]) + 1)), np.array(all_dates).mean(axis=0), color = "blue", label = "All Days (Mean)")

    #legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0)
    #plt.setp(legend.get_title(),fontsize='large')
    
    subplot_title = "Fixed Angle Correction - %RYEAR4%%RMONTH2%%RDAY2% - %YEAR4%%MONTH2%%DAY2% (All Days)"
    subplot_title = substVars(subplot_title, channel, earliest_date)
    
    axe.set_title(subplot_title, fontsize='large')
    
    # Shrink current axis's height by 10% on the bottom
    box = axe.get_position()
    axe.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    # Put a legend below current axis
    legend = axe.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          ncol=2)
    legend.draw_frame(False)
    
    ###############################################################################################################################################
    fig.patch.set_facecolor('white')
    output_file_final = substVars(output_file, channel)
    if not ((os.path.dirname(output_file_final) == "") or (os.path.exists(os.path.dirname(output_file_final)))):
        info("Output path %s not found, creating directory." % os.path.dirname(output_file_final))
        mkdir_p(os.path.dirname(output_file_final))
    
    ##########################################################################
    fig.suptitle(substVars("AMSUA_N18   %RYEAR4%%RMONTH2%%RDAY2% - %YEAR4%%MONTH2%%DAY2%\nChannel %CHANNEL%    Global All    Exp_fp", channel, earliest_date), fontsize=18) #old: 20
    
    plt.savefig(output_file_final, facecolor=fig.get_facecolor(), edgecolor='none', figsize=(595 / 50, 700 / 50), dpi = 50)

    plt.close()

def report_status(total_completed, total_running, total_procs):
    info("[%.2f%%] %i/%i completed (%i running)" % ((total_completed / (total_procs + 0.0)) * 100, total_completed, total_procs, total_running))

if mp_disable:
    info("Multiprocessing (mp) is disabled, processing in order...")
else:
    if mp_priority_mode == "GENEROUS":
        info("Multiprocessing (mp) priority mode set to GENEROUS.")
        dummymp.set_priority_mode(dummymp.DUMMYMP_GENEROUS)
    elif mp_priority_mode == "NORMAL":
        info("Multiprocessing (mp) priority mode set to NORMAL.")
        dummymp.set_priority_mode(dummymp.DUMMYMP_NORMAL)
    elif mp_priority_mode == "AGGRESSIVE":
        info("Multiprocessing (mp) priority mode set to AGGRESSIVE.")
        dummymp.set_priority_mode(dummymp.DUMMYMP_AGGRESSIVE)
    elif mp_priority_mode == "EXTREME":
        info("Multiprocessing (mp) priority mode set to EXTREME.")
        dummymp.set_priority_mode(dummymp.DUMMYMP_EXTREME)
    elif mp_priority_mode == "NUCLEAR":
        info("Multiprocessing (mp) priority mode set to NUCLEAR.")
        dummymp.set_priority_mode(dummymp.DUMMYMP_NUCLEAR)
    else:
        die("ERROR: Invalid multiprocesing (mp) priority mode detected - this may be a bug!")
    
    if mp_cpu_limit != 0:
        info("Multiprocessing (mp) maximum CPU limit set to %i CPUs." % mp_cpu_limit)
        if mp_cpu_limit == 1:
            info("(We noticed that you limited it to 1 CPU... we recommend")
            info("using --mp-disable or 'mp_disable: true' instead.)")
        dummymp.set_max_processes(mp_cpu_limit)

for channel in gen_channel_list(chans):
    info("Plotting data for channel %i..." % channel)
    if mp_disable:
        plot_scangle(channel)
    else:
        dummymp.run(plot_scangle, channel)
        dummymp.process_process()

if not mp_disable:
    dummymp.set_end_callback(report_status)
    ncpus = dummymp.getCPUAvail()
    
    if ncpus == 0:
        info(" ** Detected that the system is overloaded. Plot generation may be slow.")
        info(" ** To run tasks without waiting for CPU availability, increase priority.")
    
    info(" ** Detected %i or more CPUs available..." % ncpus)
    dummymp.process_until_done()

info("Done!")
