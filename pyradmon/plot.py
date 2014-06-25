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
# Plot Generation Library -
#   library for making plots from data
# 

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from core import *

import datetime

from fractions import Fraction

import copy

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def subst_data(plot_dict, data_dict):
    #print "subst_data called"
    plot_dict_new = copy.deepcopy(plot_dict)
    for plot_id in plot_dict_new:
        plot = plot_dict_new[plot_id]
        for subplotID in xrange(0, len(plot["plots"])):
            subplotkey = "".join(plot["plots"][subplotID].keys())
            
            subplot = plot["plots"][subplotID][subplotkey]
            if isset("data", subplot):
                if isset("x", subplot["data"]):
                    # If str, turn into a list of single str
                    if type(subplot["data"]["x"]) == str:
                        subplot["data"]["x"] = [ subplot["data"]["x"] ]
                    for eleID in xrange(0, len(subplot["data"]["x"])):
                        if (type(subplot["data"]["x"][eleID]) == list):
                            warn("Conversion from ID to list attempted, but data is already a list! (x)")
                        else:
                            subplot["data"]["x"][eleID] = data_dict[subplot["data"]["x"][eleID]]
                if isset("y", subplot["data"]):
                    # If str, turn into a list of single str
                    if type(subplot["data"]["y"]) == str:
                        subplot["data"]["y"] = [ subplot["data"]["y"] ]
                    for eleID in xrange(0, len(subplot["data"]["y"])):
                        if (type(subplot["data"]["y"][eleID]) == list):
                            warn("Conversion from ID to list attempted, but data is already a list! (y)")
                        else:
                            subplot["data"]["y"][eleID] = data_dict[subplot["data"]["y"][eleID]]
            else:
                warn("No data found to convert!")
    #print "subst_data complete"
    return plot_dict_new

def plot(plot_dict, data_dict, metadata_dict):
    # Make a working copy for our use.
    plot_dict_copy = copy.deepcopy(plot_dict)
    plot_dict = plot_dict_copy
    
    for plot_id in plot_dict:
        total_plots = len(plot_dict[plot_id]["plots"])
        
        plot = plot_dict[plot_id]
        plot_dpi = plot["settings"]["dpi"]
        plot_target_size = plot["settings"]["target_size"]
        
        size_frac = Fraction(plot_target_size[0], plot_target_size[1])
        size_frac_parts = [size_frac.numerator, size_frac.denominator]
        factor = plot_target_size[0] / size_frac_parts[0]
        
        #print "DEBUG: total_plots = %i, plot_target_size = %s, len(plot['plots'])=%i" % (total_plots, str(plot_target_size), len(plot["plots"]))
        
        fig = plt.figure(figsize=(plot_target_size[0] / plot_dpi, plot_target_size[1] / plot_dpi), dpi = plot_dpi)
        #fig = plt.figure(figsize=(size_frac_parts[0], size_frac_parts[1]), dpi = factor)
        # 595x770
        #fig = plt.figure(figsize=(plot_target_size[0] / 100, plot_target_size[1] / 100), dpi = 100)
        
        if isset("title", plot):
            #print "Replacing title..."
            plot_title = plot["title"]
            plot_title = plot_title.replace("%EXPERIMENT_ID%", metadata_dict["experiment_id"])
            plot_title = plot_title.replace("%INSTRUMENT_SAT%", metadata_dict["instrument_sat"].upper())
            plot_title = plot_title.replace("%CHANNEL%", str(metadata_dict["channel"]))
            plot_title = plot_title.replace("%FREQUENCY%", str(data_dict["frequency"]))
            plot_title = plot_title.replace("%ASSIMILATION_STATUS%", "    .......................")
            plot_title = plot_title.replace("%START_DATE%", str(metadata_dict['start_year']) + str(metadata_dict['start_month']) + str(metadata_dict['start_day']))
            plot_title = plot_title.replace("%END_DATE%", str(metadata_dict['end_year']) + str(metadata_dict['end_month']) + str(metadata_dict['end_day']))
            
            if isset("iuse", data_dict):
                if data_dict["iuse"] == -1:
                    #print "Detected iuse: Not Assimilated (iuse = %i)" % data_dict["iuse"]
                    fig.text(0.67, 0.948, "Not Assimilated", ha="center", va="bottom", size="x-large",color="red")
                else:
                    #print "Detected iuse: Assimilated (iuse = %i)" % data_dict["iuse"]
                    fig.text(0.67, 0.948, "Assimilated", ha="center", va="bottom", size="x-large",color="green")
            else:
                warn("Unable to determine assimilation!")
                fig.text(0.67, 0.948, "Unknown (??)", ha="center", va="bottom", size="x-large",color="orange")
        fig.suptitle(plot_title, fontsize=18) #old: 20
        plt.subplots_adjust(hspace = 1.2, left=0.15, top=0.88)
        
        # Fix dates
        #fig.autofmt_xdate()
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        #plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        
        for subplotID in xrange(0, len(plot["plots"])):
            #print "Plot"
            axe = fig.add_subplot(total_plots, 1, subplotID + 1)
            
            # TODO: check for multiple keys, that won't work
            subplotkey = "".join(plot["plots"][subplotID].keys())
            
            subplot = plot["plots"][subplotID][subplotkey]
            #print subplot
            if isset("axes", subplot):
                if isset("x", subplot["axes"]):
                    if isset("ticks", subplot["axes"]["x"]):
                        #if (subplot["axes"]["x"]["ticks"]):
                        #####axe.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["x"]["ticks"]))
                        pass
                        #else:
                        #    print "WARNING: Non-integer ticks for X-axis on subplot %i." % subplotID
                    if isset("label", subplot["axes"]["x"]):
                        axe.xaxis.set_label_text(subplot["axes"]["x"]["label"])
                if isset("y", subplot["axes"]):
                    if isset("ticks", subplot["axes"]["y"]):
                        #if isdigit(subplot["axes"]["y"]["ticks"]):
                        axe.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(subplot["axes"]["y"]["ticks"]))
                        #else:
                        #    print "WARNING: Non-integer ticks for Y-axis on subplot %i." % subplotID
                    if isset("label", subplot["axes"]["y"]):
                        axe.yaxis.set_label_text(subplot["axes"]["y"]["label"])
            
            if isset("data", subplot):
                if isset("x", subplot["data"]):
                    # Check to make sure the data is substituted!
                    verify_x_data = True
                    for eleID in xrange(0, len(subplot["data"]["x"])):
                        if (type(subplot["data"]["x"][eleID]) != list):
                            verify_x_data = False
                            break
                    if not verify_x_data:
                        #print "x trigger verify"
                        plot_dict = subst_data(plot_dict, data_dict)
                        plot = plot_dict[plot_id]
                        subplot = plot["plots"][subplotID][subplotkey]
                    
                    if isset("y", subplot["data"]):
                        # Check to make sure data has been substituted!
                        verify_y_data = True
                        for eleID in xrange(0, len(subplot["data"]["y"])):
                            if (type(subplot["data"]["y"][eleID]) != list):
                                verify_y_data = False
                                break
                        if not verify_y_data:
                            #print "y trigger verify"
                            plot_dict = subst_data(plot_dict, data_dict)
                            plot = plot_dict[plot_id]
                            subplot = plot["plots"][subplotID][subplotkey]
                        
                        if isset("post_processing", subplot["data"]):
                            if isset("x", subplot["data"]["post_processing"]):
                                exec "post_processing_func_x = lambda data,x,y: %s" % subplot["data"]["post_processing"]["x"]
                                
                                for eleID_x in xrange(0, len(subplot["data"]["x"])):
                                    for eleID_y in xrange(0, len(subplot["data"]["y"])):
                                        subplot["data"]["x"][eleID_x] = post_processing_func_x(data_dict, subplot["data"]["x"][eleID_x], subplot["data"]["y"][eleID_y])
                            if isset("y", subplot["data"]["post_processing"]):
                                exec "post_processing_func_y = lambda data,x,y: %s" % subplot["data"]["post_processing"]["y"]
                                
                                for eleID_x in xrange(0, len(subplot["data"]["x"])):
                                    for eleID_y in xrange(0, len(subplot["data"]["y"])):
                                        subplot["data"]["y"][eleID_x] = post_processing_func_y(data_dict, subplot["data"]["x"][eleID_x], subplot["data"]["y"][eleID_y])
                        
                        plot_kwargs = {}
                        y_id = 0
                        #print subplot["data"]["y"]
                        for y_dat in subplot["data"]["y"]:
                            # todo: implement warnings
                            if isset("colors", subplot["data"]):
                                if type(subplot["data"]["colors"]) == str:
                                    subplot["data"]["colors"] = [ subplot["data"]["colors"] ]
                                if y_id < len(subplot["data"]["colors"]):
                                    l_color = subplot["data"]["colors"][y_id]
                                    plot_kwargs["color"] = l_color
                            if isset("labels", subplot["data"]):
                                if type(subplot["data"]["labels"]) == str:
                                    subplot["data"]["labels"] = [ subplot["data"]["labels"] ]
                                if y_id < len(subplot["data"]["labels"]):
                                    l_label = subplot["data"]["labels"][y_id]
                                    l_label = l_label.replace("%COLOR%", "")
                                    l_label = l_label.replace("%ENDCOLOR%", "")
                                    
                                    # Zero division detect
                                    if len(y_dat) == 0:
                                        AVG = 0
                                    else:
                                        AVG = round(sum(y_dat) / len(y_dat), 3)
                                    
                                    l_label = l_label.replace("%AVERAGE%", str(AVG))
                                    plot_kwargs["label"] = l_label
                                    # todo: implemenet %stddev%
                            else:
                                l_label = ""
                            #print "Hello"
                            
                            #plot_kwargs["marker"] = '.'
                            
                            plt.plot(np.array(subplot["data"]["x"][0]), np.array(y_dat), **plot_kwargs)
                            y_id += 1
            
            if isset("legend", subplot):
                #print "Legend area detected..."
                legend_kwargs = {}
                box = axe.get_position()
                axe.set_position([box.x0 + box.width * 0.1, box.y0, box.width * 0.9, box.height])
                '''if isset("title", subplot["legend"]):
                    legend_kwargs["title"] = subplot["legend"]["title"]'''
                
                if "title" in subplot["legend"]:
                    legend_kwargs["title"] = subplot["legend"]["title"]
                legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0, **legend_kwargs)
                
                #print "Adding legend..."
                '''if isset("line", subplot["legend"]):
                    if subplot["legend"]["line"] == True:
                        legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0, **legend_kwargs)
                    else:
                        # We have to do this in a rather hacky way...
                        legend = axe.legend(loc='center left', bbox_to_anchor=(-0.3, 0.5), borderaxespad=0., handlelength=0, **legend_kwargs)
                        import ipdb
                        ipdb.set_trace()'''
                
                
                
                plt.setp(legend.get_title(),fontsize='large')
                
                #lt = l.get_texts()
                #for llt in lt:
                #    plt.setp(llt,fontsize=10)
                
                '''if isset("border", subplot["legend"]):
                    if not subplot["legend"]["border"]:
                        legend.draw_frame(False)'''
            
            if isset("title", subplot):
                axe.set_title(subplot["title"], fontsize='large')
            
            # Set date format
            #ticks = axe.get_xticks()
            #n = len(ticks)//6
            #axe.set_xticks(ticks[::n])
            axe.xaxis.set_major_formatter(mdates.DateFormatter('%d%b\n%Y'))
        
        # Fix dates
        #plt.gcf().autofmt_xdate()
        
        
        fig.patch.set_facecolor('white')
        
        if isset("output", plot):
            plot_output = plot["output"]
            plot_output = plot_output.replace("%CHANNEL%", str(metadata_dict["channel"]))
        else:
            warn("Output path not specified, will save to 'magical_plot_please_specify_output_path_next_time.png'")
            plot_output = "magical_plot_please_specify_output_path_next_time.png"
        
        #print "Saving to: %s (size: %ix%i at %s res, dpi %i)" % (plot_output, plot_target_size[0], plot_target_size[1], str(((plot_target_size[0] + 0.0) / plot_dpi, (plot_target_size[1] + 0.0) / plot_dpi)), plot_dpi)
        
        plt.savefig(plot_output, facecolor=fig.get_facecolor(), edgecolor='none', figsize=((plot_target_size[0] + 0.0) / plot_dpi, (plot_target_size[1] + 0.0) / plot_dpi), dpi = plot_dpi)
        
        #plt.savefig(plot_output, facecolor=fig.get_facecolor(), edgecolor='none', figsize=(size_frac_parts[0], size_frac_parts[1]), dpi = factor)
        #plt.savefig(plot_output, facecolor=fig.get_facecolor(), edgecolor='none')
        
        # Free it all!
        plt.clf()
        plt.close()

if __name__ == "__main__":
    # Use test data
    from enumerate import enumerate
    from data import *
    from test import *
    
    en = enumerate()
    dat = get_data(en, TEST_DATA_VARS, 4)

    import pprint, yaml
    #pprint.pprint(plot_dict)
    #print yaml.dump(plot_dict)
    plot(plot_dict, dat, metadata_dict)
