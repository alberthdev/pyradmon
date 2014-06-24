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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# 
# Main Wrapper Library -
#   library for combining everything together!
# 

import sys

from core import *
import args
import config
import config_printer
from config import *

from enumerate import enumerate
from data import get_data
from plot import plot, subst_data

def main():
    parser = args.make_argparser()
    parse = parser.parse_args()
    (pyradmon_config, plot_dict, parse_data) = args.parse_to_config(parse)
    
    if not pyradmon_config:
        sys.exit(1)
    
    ###################################################################
    ## VERB ACTION CODE
    ###################################################################
    
    ## Config verb + Config args, part 2
    if parse.verb == "config":
        if isset_obj("config_display", parse) and parse.config_display:
            # Print configuration
            config_printer.display(pyradmon_config, plot_dict)
        if isset_obj("config_save", parse):
            # Print configuration
            config.save(parse.config_save, pyradmon_config, plot_dict)
    elif parse.verb == "plot":
        #print "HOHOHOOHOH"
        if "data_all" in pyradmon_config and pyradmon_config["data_all"]:
            (enum_opts_dict, data_var_list) = config.postprocess(pyradmon_config, plot_dict)
            
            info(" ** Enumerating data files...")
            en = enumerate(**enum_opts_dict)
            
            chans = enum_opts_dict["data_channels"]
            
            info(" ** Fetching data for channel %s..." % (chans[0] if len(chans) == 1 else \
                        " and ".join(chans) if len(chans) == 2 else \
                        (", ".join(chans[:-1]) + ", and " + chans[-1])))
            dat = get_data(en, data_var_list, gen_channel_list(chans))
            
            #pprinter(dat[1])
            
            for channel in gen_channel_list(chans):
                info(" ** Plotting data for channel %i..." % channel)
                
                enum_opts_dict["channel"] = channel
                
                try:
                    plot_dict_subs = subst_data(plot_dict, dat[channel])
                    plot(plot_dict_subs, dat[channel], enum_opts_dict)
                    del plot_dict_subs
                except:
                    critical("An error occurred! Error follows:")
                    critical(traceback.format_exc())
                    #print "Dumping data_dict:"
                    #pprint.pprint(dat)
                    critical("Exiting.")
                    sys.exit(1)

if __name__ == "__main__":
    main()
