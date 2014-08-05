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
# Scan Angle Plot Generator | Configuration Helper -
#   Configuration helper library for PyRadmon SA plotter.
#   (Part of program for plotting the scan angles.)
# 

import argparse
import textwrap

import logging

from pyradmon.core import *
from pyradmon._version import __version__
from pyradmon import log

import yaml
try:
    from yaml import CLoader as Loader, CDumper as dumper
except ImportError:
    from yaml import Loader, Dumper

def load_config(config_file):
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
    pyradmon_sa_config = config_dict.pop("config", None)
    return pyradmon_sa_config

#######################################################################
# Argument Handling
#######################################################################
def make_parser():
    main_opts = OrderedDict()
    main_opts['--config-file'] = \
        {
            'action'    : 'store',
            'dest'      : 'config_file',
            'metavar'   : 'FILE',
            'help'      : 'Load a configuration file for PyRadmon SA to use.',
        }
    main_opts['--logging-output'] = \
        {
            'action'    : 'store',
            'metavar'   : 'OUTPUT',
            'dest'      : 'logging_output',
            'help'      : 'Specify where to output to. Options include file, stdout, and stderr. Multiple outputs can be specified, seperated with a comma.',
        }
    main_opts['--logging-file'] = \
        {
            'action'    : 'store',
            'metavar'   : 'FILE',
            'dest'      : 'logging_file',
            'help'      : 'If outputting to a file, specify the file path to save to.',
        }
    main_opts['--logging-level'] = \
        {
            'action'    : 'store',
            'metavar'   : 'LOG_LEVEL',
            'dest'      : 'logging_level',
            'help'      : 'Set the logging level for PyRadmon SA.',
        }

    # Settings related args
    main_opts['--data-path-format'] = \
        {
            'action'    : 'store',
            'metavar'   : 'FORMAT',
            'dest'      : 'data_path_format',
            'help'      : 'Set the path format for the data.',
        }

    main_opts['--data-experiment-id'] = \
        {
            'action'    : 'store',
            'metavar'   : 'EXPERIMENT_ID',
            'dest'      : 'data_experiment_id',
            'help'      : 'Set the data experiment ID for the data.',
        }

    main_opts['--data-instrument-sat'] = \
        {
            'action'    : 'store',
            'metavar'   : 'INSTRUMENT_SAT',
            'dest'      : 'data_instrument_sat',
            'help'      : 'Set the instrument and satellite ID for data.',
        }
    
    main_opts['--data-all-channels'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'data_all_channels',
            'help'      : 'Specify to use all of the channels from the data. Negates --data-channels option.',
        }
    
    main_opts['--data-channels'] = \
        {
            'action'    : 'store',
            'metavar'   : 'CHANNELS',
            'dest'      : 'data_channels',
            'help'      : 'Specify the channels to use from the data, separated by commas. Ranges are also acceptable.',
        }

    main_opts['--data-start-date'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DATE',
            'dest'      : 'data_start_date',
            'help'      : 'Specify the start date for the data. Format should be "YYYY-MM-DD HHz".',
        }

    main_opts['--data-reference-date'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DATE',
            'dest'      : 'data_reference_date',
            'help'      : 'Specify the reference (or end) date for the data. Format should be "YYYY-MM-DD HHz".',
        }

    main_opts['--output-file'] = \
        {
            'action'    : 'store',
            'metavar'   : 'OUTPUT_FILE',
            'dest'      : 'output_file',
            'help'      : 'Specify the output file for the generated plot.',
        }
    main_opts['--mp-disable'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'mp_disable',
            'help'      : 'Disable multiprocessing (mp) optimizations in PyRadmon.',
        }
    main_opts['--mp-priority-mode'] = \
        {
            'action'    : 'store',
            'metavar'   : 'PRIORITY_MODE',
            'dest'      : 'mp_priority_mode',
            'help'      : 'Set the priority mode for the multiprocessing (mp) optimizations in PyRadmon. Options are GENEROUS, NORMAL, AGGRESSIVE, EXTREME, and NUCLEAR. GENEROUS yields to other CPU hungry processes, while NUCLEAR spawns as many processes as it can regardless of CPU usage.',
        }
    main_opts['--mp-cpu-limit'] = \
        {
            'action'    : 'store',
            'metavar'   : 'NUM_CPUS',
            'dest'      : 'mp_cpu_limit',
            'help'      : 'Limit the number of CPUs that the multiprocessing (mp) optimizations in PyRadmon can use.',
        }

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                    epilog = textwrap.dedent("""\
                      Logging levels, from least to most importance:
                        DEBUG, INFO, WARNING, ERROR, CRITICAL
                      Setting a logging level will show messages that meet and
                      exceed that level. For instance, setting INFO will show
                      INFO, WARNING, ERROR, and CRITICAL messages.
                      
                      Quick Start Examples:
                        Make plots:
                          %(prog)s --config-file=config.yaml
                        Change start date, then make plots:
                          %(prog)s --config-file=config.yaml --data-start-date "2014-05-31 00z"
                        Make plots and log output:
                          %(prog)s --config-file=config.yaml --logging-output="stdout,file" \\
                                   --logging-file="mylog.txt"
                      """),
                    version = 'PyRadmon SA v' + __version__) # Old: %(prog)s evals to pyradmon.py

    for opt in main_opts:
        opt_opt = dict(main_opts[opt])
        parser.add_argument(opt, **opt_opt)
    
    return parser

def parse_to_config(parse):
    # Init a few variables:
    pyradmon_sa_config = {}
    
    ## Core args
    # First, examine the core arguments.
    if isset_obj("config_file", parse):
        # OK, check if the file exists.
        if os.path.isfile(parse.config_file):
            # Attempt to load
            res = load_config(parse.config_file)
            
            if res == None:
                print "ERROR: Could not open configuration file! (Alternatively, your configuration may be invalid!)"
                return None
            
            pyradmon_sa_config = res
        else:
            print "ERROR: Configuration file path does not exist!"
            return None
    
    # Now check for logging args!
    file_enabled = False
    
    if isset_obj("logging_output", parse):
        logging_output = parse.logging_output
        
        if logging_output != "":
            logging_output = logging_output.split(",")
            logging_output = [x.strip() for x in logging_output]
            
            final_logging_output = []
            
            for log_o in logging_output:
                if log_o == 'file':
                    file_enabled = True
                elif log_o == 'stdout':
                    final_logging_output.append(sys.stdout)
                elif log_o == 'stderr':
                    final_logging_output.append(sys.stderr)
                else:
                    print "ERROR: Invalid logging output! Valid output: stdout, stderr, file"
                    return None
            logging_output = final_logging_output
    else:
        logging_output = [ sys.stdout ]
    
    if logging_output and file_enabled and isset_obj("logging_file", parse):
        logging_file = parse.logging_file
    else:
        logging_file = None
    
    if isset_obj("logging_level", parse):
        logging_level = parse.logging_level
        logging_level = logging_level.strip()
        if logging_level == "INFO":
            logging_level = logging.INFO
        elif logging_level == "WARNING":
            logging_level = logging.WARNING
        elif logging_level == "ERROR":
            logging_level = logging.ERROR
        elif logging_level == "CRITICAL":
            logging_level = logging.CRITICAL
        elif logging_level == "DEBUG":
            logging_level = logging.DEBUG
        else:
            print "ERROR: Invalid logging level specified!"
            print "Valid levels: INFO, WARNING, ERROR, CRITICAL, DEBUG"
            return None
    else:
        logging_level = logging.INFO
    
    # We're ready - let's set up logging!
    logger = log.init(logging_level, logging_output, logging_file)
    
    # From now on, we'll stick to using the log module to print stuff
    # out.
    
    if isset_obj("mp_disable", parse):
        pyradmon_sa_config['mp_disable'] = parse.mp_disable
    
    if isset_obj("mp_priority_mode", parse):
        mp_priority_mode = parse.mp_priority_mode
        mp_priority_mode = mp_priority_mode.strip()
        if mp_priority_mode == "GENEROUS":
            pyradmon_sa_config['mp_priority_mode'] = "GENEROUS"
        elif mp_priority_mode == "NORMAL":
            pyradmon_sa_config['mp_priority_mode'] = "NORMAL"
        elif mp_priority_mode == "AGGRESSIVE":
            pyradmon_sa_config['mp_priority_mode'] = "AGGRESSIVE"
        elif mp_priority_mode == "EXTREME":
            pyradmon_sa_config['mp_priority_mode'] = "EXTREME"
        elif mp_priority_mode == "NUCLEAR":
            pyradmon_sa_config['mp_priority_mode'] = "NUCLEAR"
        else:
            die("ERROR: Invalid multiprocessing (mp) priority mode specified! Valid levels: GENEROUS, NORMAL, AGGRESSIVE, EXTREME, NUCLEAR")
    else:
        pyradmon_sa_config['mp_priority_mode'] = "NORMAL"
    
    if isset_obj("mp_cpu_limit", parse):
        if (parse.mp_cpu_limit).isdigit():
            pyradmon_sa_config['mp_cpu_limit'] = int(parse.mp_cpu_limit)
        else:
            die("ERROR: Invalid multiprocessing (mp) CPU limit! The CPU limit must specify an integer number of CPUs to limit use to.")
    
    # --output-file
    if isset_obj("output_file", parse):
        output_file = (parse.output_file).strip()
    
    # --data-all-channels
    if isset_obj("data_all_channels", parse) and parse.data_all_channels:
        pyradmon_sa_config["data_all_channels"] = parse.data_all_channels
    
    # --data-channels
    if isset_obj("data_channels", parse):
        if isset_obj("data_all_channels", parse) and parse.data_all_channels:
            die("ERROR: You can not specify --data-all-channels and --data-channels at the same time!")
        for data_channel in (parse.data_channels).split(","):
            data_channel = data_channel.strip()
            
            if not ( (data_channel.isdigit()) or \
                ( (len(data_channel.split("-")) == 2) and data_channel.split("-")[0].isdigit() and data_channel.split("-")[1].isdigit() ) ):
                die("ERROR: Invalid data channel '%s' specified in --data-channels! Must be a number or a numeric range (#-#)." % data_channel)
        
        pyradmon_sa_config["data_channels"] = parse.data_channels

    # --data-path-format
    if isset_obj("data_path_format", parse):
        pyradmon_sa_config["data_path_format"] = parse.data_path_format
    
    # --data-experiment-id
    if isset_obj("data_experiment_id", parse):
        pyradmon_sa_config["data_experiment_id"] = parse.data_experiment_id
    
    # --data-start-date
    if isset_obj("data_start_date", parse):
        if isset_obj("data_all", parse):
            die("ERROR: You can not specify --data-all and --data-start-date at the same time!")
        if isset_obj("data_single_date", parse):
            die("ERROR: You can not specify --data-single-date and --data-start-date at the same time!")
        
        # FORMAT: YYYY-MM-DD HHz
        pyradmon_sa_config["data_start_date"] = parse.data_start_date
        
        if not (pyradmon_sa_config["data_start_date"][:4].isdigit() and \
            pyradmon_sa_config["data_start_date"][5:7].isdigit() and \
            pyradmon_sa_config["data_start_date"][8:10].isdigit() and \
            pyradmon_sa_config["data_start_date"][11:13].isdigit()):
            die("ERROR: Start date '%s' specified in --data-start-date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_sa_config["data_start_date"])
    
    # --data-reference-date
    if isset_obj("data_reference_date", parse):
        # FORMAT: YYYY-MM-DD HHz
        pyradmon_sa_config["data_reference_date"] = parse.data_reference_date
        
        if not (pyradmon_sa_config["data_reference_date"][:4].isdigit() and \
            pyradmon_sa_config["data_reference_date"][5:7].isdigit() and \
            pyradmon_sa_config["data_reference_date"][8:10].isdigit() and \
            pyradmon_sa_config["data_reference_date"][11:13].isdigit()):
            die("ERROR: Reference/end date '%s' specified in --data-reference-date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_sa_config["data_reference_date"])
    
    # --data-instrument-sat
    if isset_obj("data_instrument_sat", parse):
        pyradmon_sa_config["data_instrument_sat"] = parse.data_instrument_sat
    
    return pyradmon_sa_config

def process_config(config):
    #### SANITY CHECK ####
    if not "data_path_format" in config:
        die("ERROR: Data path format not specified! This is required to read scan angle data!")
    
    if not "data_experiment_id" in config:
        die("ERROR: Experiment ID not specified! This is required to read and idenfiy scan angle data!")
    
    if not "data_instrument_sat" in config:
        die("ERROR: Instrument and satellite ID not specified! This is required to read and idenfiy scan angle data!")
    
    if (not "data_all_channels" in config) and (not "data_channels" in config):
        die("ERROR: No data channels specified! Must either have data_all_channels or specific data_channels specified!")
    
    if not "data_start_date" in config:
        die("ERROR: Start date not specified! This is required to read and idenfiy scan angle data!")
    
    if not "data_reference_date" in config:
        die("ERROR: Reference (end) date not specified! This is required to read and idenfiy scan angle data!")
    
    if not "output_file" in config:
        die("ERROR: Output file not specified! This is required to product scan angle plots!")
    
    #### PROCESS ####
    final_config = {}
    
    final_config["data_path_format"] = config["data_path_format"]
    final_config["experiment_id"]    = config["data_experiment_id"]
    final_config["instrument_sat"]   = config["data_instrument_sat"]
    final_config["all_channels"]     = config["data_all_channels"] if ("data_all_channels" in config) else False
    final_config["channels"]         = config["data_channels"] if ("data_channels" in config) else None
    
    final_config["start_year"]       = config["data_start_date"][:4]
    final_config["start_month"]      = config["data_start_date"][5:7]
    final_config["start_day"]        = config["data_start_date"][8:10]
    final_config["start_hour"]       = config["data_start_date"][11:13]
    
    final_config["reference_year"]   = config["data_reference_date"][:4]
    final_config["reference_month"]  = config["data_reference_date"][5:7]
    final_config["reference_day"]    = config["data_reference_date"][8:10]
    final_config["reference_hour"]   = config["data_reference_date"][11:13]
    
    final_config["output_file"]      = config["output_file"]
    
    if "mp_disable" in config:
        final_config["mp_disable"]   = config["mp_disable"]
    else:
        final_config["mp_disable"]   = False
    
    if "mp_priority_mode" in config:
        final_config["mp_priority_mode"]   = config["mp_priority_mode"]
    else:
        # May be redundant due to preprocessing
        final_config["mp_priority_mode"]   = "NORMAL"
    
    if "mp_cpu_limit" in config:
        final_config["mp_cpu_limit"]   = config["mp_cpu_limit"]
    else:
        final_config["mp_cpu_limit"]   = 0
    
    return final_config

def do_config():
    parser = make_parser()
    parse = parser.parse_args()
    pyradmon_sa_config = parse_to_config(parse)
    final_config = process_config(pyradmon_sa_config)
    return final_config
