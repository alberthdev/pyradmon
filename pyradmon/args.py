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
# Argument Parsing Library -
#   library for parsing command line arguments
# 

import argparse
import textwrap
import os
import sys

from _version import __version__

from core import *
import config
import config_printer
from config import SPECIAL_FIELDS
import log

import logging

try:
    from collections import OrderedDict
except:
    try:
        from ordereddict import OrderedDict
    except:
        print "ERROR: OrderedDict not found! It is required to run this script."
        sys.exit(1)

def add_args(parser, inherit, opts):
    for opt in opts:
        if inherit:
            opts[opt]['help'] = argparse.SUPPRESS
            opts[opt]['default'] = argparse.SUPPRESS
        opt_opt = dict(opts[opt])
        parser.add_argument(opt, **opt_opt)

def add_list_args(parser, inherit = False):
    opts = OrderedDict()
    opts['--data-all'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'data_all',
            'help'      : 'Use all data. Negates the options below specifying dates.',
        }
    opts['--data-single-date'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DATE',
            'dest'      : 'data_single_date',
            'help'      : 'Use single date. Format should be "YYYY-MM-DD HHz". Negates the options below specifying dates and times.',
        }
    opts['--data-base-directory'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DIR',
            'dest'      : 'data_base_directory',
            'help'      : 'Specify the base directory for data.',
        }
    opts['--data-experiment-id'] = \
        {
            'action'    : 'store',
            'metavar'   : 'EXPERIMENT_ID',
            'dest'      : 'data_experiment_id',
            'help'      : 'Specify the experiment ID for data.',
        }
    opts['--data-start-date'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DATE',
            'dest'      : 'data_start_date',
            'help'      : 'Specify the start date for data. Format should be "YYYY-MM-DD HHz".',
        }
    opts['--data-end-date'] = \
        {
            'action'    : 'store',
            'metavar'   : 'DATE',
            'dest'      : 'data_end_date',
            'help'      : 'Specify the end date for data. Format should be "YYYY-MM-DD HHz".',
        }
    opts['--data-instrument-sat'] = \
        {
            'action'    : 'store',
            'metavar'   : 'INSTRUMENT_SAT',
            'dest'      : 'data_instrument_sat',
            'help'      : 'Specify the instrument and satellite ID for data.',
        }
    opts['--data-step'] = \
        {
            'action'    : 'store',
            'metavar'   : 'STEP_TYPE',
            'dest'      : 'data_step',
            'help'      : 'Specify the step/type for the data. "anl" and "ges" are allowed. If you wish to specify more than one, use a pipe to seperate them, e.g. "anl|ges".',
        }
    opts['--data-time-delta'] = \
        {
            'action'    : 'store',
            'metavar'   : 'TIME_DELTA',
            'dest'      : 'data_time_delta',
            'help'      : """Specify the time interval for data. The time format is
                             expressed using the sleep command's format, "#U", where # is
                             a number and U is a letter representing a unit of time.""",
        }
    
    add_args(parser, inherit, opts)

def add_dump_args(parser, inherit = False):
    opts = OrderedDict()
    opts['--dump-columns'] = \
        {
            'action'    : 'store',
            'metavar'   : 'COLUMNS',
            'dest'      : 'dump_columns',
            'help'      : 'Specify the columns to dump/use, separated by commas.',
        }
    opts['--dump-all-channels'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'dump_all_channels',
            'help'      : 'Specify to dump all channels. Negates the option below specifying channels to use.',
        }
    opts['--dump-channels'] = \
        {
            'action'    : 'store',
            'metavar'   : 'CHANNELS',
            'dest'      : 'dump_channels',
            'help'      : 'Specify the channels to dump/use, separated by commas. Ranges are also acceptable.',
        }
    opts['--dump-assim-only'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'dump_assim_only',
            'help'      : 'Specify to use only assimilated data (iuse = 1).',
        }
    
    add_args(parser, inherit, opts)

def add_plot_args(parser, inherit = False):
    opts = OrderedDict()
    opts['--plot-define-plots'] = \
        {
            'action'    : 'append',
            'metavar'   : 'PLOTS',
            'dest'      : 'plot_define_plots',
            'help'      : 'Define plots. Uses the value list system, specified by "plot1,plot2,plot3,...".',
        }
    opts['--plot-define-subplots'] = \
        {
            'action'    : 'append',
            'metavar'   : 'SUBPLOTS',
            'dest'      : 'plot_define_subplots',
            'help'      : 'Define subplots. Uses the key-value pair system, specified by "plot1:subplot1,subplotid2,...;".',
        }
    opts['--plot-define-axes'] = \
        {
            'action'    : 'append',
            'metavar'   : 'AXES',
            'dest'      : 'plot_define_axes',
            'help'      : 'Define axes for the subplot. Uses the key-value pair system, specified by "plot1|subplot1|y:ticks=5,label="test";...".',
        }
    opts['--plot-define-data'] = \
        {
            'action'    : 'append',
            'metavar'   : 'DATA',
            'dest'      : 'plot_define_data',
            'help'      : 'Define data to be plotted in the subplot. Uses the key-value pair system, specified by "plot1|subplot1|x:data_field_1;plot1|subplot1|y:...".',
        }
    opts['--plot-define-title'] = \
        {
            'action'    : 'append',
            'metavar'   : 'TITLE',
            'dest'      : 'plot_define_title',
            'help'      : 'Define the title for the plot, and optionally, subplot and legend. Uses the key-value pair system, specified by "plot1:title;plot1|subplot1:title;plot1|subplot1|legend:title;...".',
        }
    opts['--plot-define-output'] = \
        {
            'action'    : 'append',
            'metavar'   : 'OUTPUT_FILE',
            'dest'      : 'plot_define_output',
            'help'      : 'Define the output file for the plot. Uses the key-value pair system, specified by "plot1:output_file.png;...".',
        }
    opts['--plot-define-settings'] = \
        {
            'action'    : 'append',
            'metavar'   : 'SETTINGS',
            'dest'      : 'plot_define_settings',
            'help'      : 'Define the settings for the plot. Uses the key-value pair system, specified by "plot1:target_size=595x700,dpi=50;...".',
        }
    opts['--plot-define-custom-vars'] = \
        {
            'action'    : 'append',
            'metavar'   : 'CUSTOM_VARS',
            'dest'      : 'plot_define_custom_vars',
            'help'      : 'Define the custom variables for use in the output file and title. Uses the key-value pair system, specified by "myvar:123,myvar2:abc,...".',
        }
    opts['--plot-make-dirs'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'plot_make_dirs',
            'help'      : 'Make directories if the specified output path does not exist.',
        }
    
    add_args(parser, inherit, opts)

def add_config_args(parser, inherit = False):
    opts = OrderedDict()
    opts['--config-display'] = \
        {
            'action'    : 'store_true',
            'dest'      : 'config_display',
            'help'      : 'Displays the configuration.',
        }
    opts['--config-load'] = \
        {
            'action'    : 'store',
            'metavar'   : 'FILE',
            'dest'      : 'config_load',
            'help'      : 'Load an existing configuration file. Note that this will override the main --config-file argument.',
        }
    opts['--config-save'] = \
        {
            'action'    : 'store',
            'metavar'   : 'FILE',
            'dest'      : 'config_save',
            'help'      : 'Save the currently loaded configuration to a file. Note that saved configuration may not be placed in order.',
        }
    
    add_args(parser, inherit, opts)

def make_argparser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, \
                epilog = textwrap.dedent("""\
                  Logging levels, from least to most importance:
                    DEBUG, INFO, WARNING, ERROR, CRITICAL
                  Setting a logging level will show messages that meet and
                  exceed that level. For instance, setting INFO will show
                  INFO, WARNING, ERROR, and CRITICAL messages.
                  
                  Quick Start Examples:
                    List data available:
                      %(prog)s --config-file=config.yaml list
                    Dump data:
                      %(prog)s --config-file=config.yaml dump
                    Make plots:
                      %(prog)s --config-file=config.yaml plot
                    Print configuration:
                      %(prog)s --config-file=config.yaml config
                    Make plots and log output:
                      %(prog)s --config-file=config.yaml --logging-output="stdout,file" \\
                               --logging-file="mylog.txt" plot
                  """),
                version = 'PyRadmon v' + __version__) # Old: %(prog)s evals to pyradmon.py

    subparsers = parser.add_subparsers(metavar="verb", dest = "verb", help='Description')

    main_opts = OrderedDict()
    main_opts['--config-file'] = \
        {
            'action'    : 'store',
            'dest'      : 'config_file',
            'metavar'   : 'FILE',
            'help'      : 'Load a configuration file for PyRadmon to use. Synonymous to --config-load, but for all verbs and options.',
        }
    main_opts['--config-unset'] = \
        {
            'action'    : 'append',
            'dest'      : 'config_unset',
            'metavar'   : 'VARS',
            'help'      : 'Unset (or remove) variables after all configuration settings (config file and command line) have been loaded. Format for VARS is "VARIABLE1;VARIABLE2;...". For core PyRadmon configuration, the variable syntax is "config.key". For plot configuration, the variable syntax follows the plot argument hierarchy format at any level, e.g. "plot|subplot|attr|subattr", "plot|subplot", or even "plot". (See plot help for more details regarding the plot hierarchy format.) ',
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
            'help'      : 'Set the logging level for PyRadmon.',
        }

    add_args(parser, False, main_opts)

    # A list command
    list_parser = subparsers.add_parser('list', help='Lists the data set available for use.', \
        description = 'Lists the data set available for use.',
        epilog = textwrap.dedent("""\
                 For --data-time-delta:
                   Available time units (case-sensitive):
                     s: seconds    m: minutes    h: hours    d: days
                     w: weeks      M: months     y: years
                   For instance, to specify 5 months, 3 minutes, 2 seconds:
                     "5M 3m 2s"
                   
                   Multiple elements with same time units will be summed up,
                   regardless of position or order. "3m 2s 5m" == "8m 2s"
                   
                   Years is not a native time delta, so this uses the
                   conversion "1 year = 365 days".
                   
                   Note that specifying years may have some caveats, see:
                     http://stackoverflow.com/a/765990
                 """), \
                 formatter_class=argparse.RawDescriptionHelpFormatter)
    add_list_args(list_parser, False)

    # [dump]
    dump_parser = subparsers.add_parser('dump', help='Dumps data from the data set.', \
        description = textwrap.dedent("""\
        Dumps data from the data set.
        
        Inherits arguments from [list]. [list] arguments may be required to use
        [dump]. For information on [list] arguments, see the [list] help.
        """), \
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_list_args(dump_parser, True)
    add_dump_args(dump_parser, False)

    # [plot]
    plot_parser = subparsers.add_parser('plot', help='Creates a plot given plot parameters.', \
        description = textwrap.dedent("""\
        Creates a plot given plot parameters.
        
        Inherits arguments from [list] and [dump]. [list] and [dump] arguments
        may be required to use [plot]. For information on [list] and [dump]
        arguments, see their respective help.
        
        NOTE: These options are advanced - although you could (potentially)
              plot using these options, it would probably be very painful!
              All of these options can be defined via config file, which is
              much easier and less verbose! These options are meant to be
              used in conjunction with a config file for overriding certain
              configuration options and testing them.
              
        """), \
        epilog = textwrap.dedent("""\
        Definitions follow either a simple value list system or a simple
        key-value pair system.
        
        Value List System:
          The value list system looks like:
          "value1,value2,value3,..."
        
          For the value list system, values are separated with commas.
        
        Key-Value Pair System:
          The key-value pair system looks like:
          "key1:value1,value2;key2:value3,value4,..."
        
          For the key-value pair system, a key is followed by a colon,
          values are separated with commas, and key-value pairs are
          separated by semicolons.
          
          If settings are being set, values can look like subkey=value.
          It is a pair with a sub-key and a sub-value, separated by an
          equal sign.
          These are called sub-key-value pairs, and are in place of values
          in a key-value system.
          
          They can look like this:
          "key1:skey1=sval1,skey2=sval2;..."
          
        Key/Value Naming:
          Plots and subplots are indicated above with plot# and subplot#,
          respectively. They are simply IDs for the plots and subplots.
          You define them with --plot-define-plots and --plot-define-subplots.
          
          They can take on any name - for instance:
            --plot-define-plots="a,b" --plot-define-subplots="a:1,2;b:3,4"
          
          Hierarchy is done by starting with the highest hierarchy, and then
          adding additional lower levels to the right, sepearated by pipes.
          For instance:
            high|medium|low
          
          In the case of plots and subplots, the hierarchy is as follows:
            plot|subplot|attribute
          
          This is the naming scheme for keys in key/value pairs.
        
        Argument Definitions:
          Note that arguments can be specified multiple times to reduce
          the length of one argument. For instance:
          
            --plot-define-plots="plot1" --plot-define-plots="plot2"
          is the same as
            --plot-define-plots="plot1,plot2"
            
          This works regardless of argument order. This is encouraged, since
          this helps with argument organization. (In particular, arguments
          deals with a specific plot or subplot can be grouped together.)
          
          --plot-define-plots
            Value list of plot IDs.
            
            This argument is REQUIRED to produce a plot.
            
            Example:
              "plot1,abc2,superplot3"
              
          --plot-define-subplots
            Key-value pairs of plot IDs and subplot IDs.
            
            This argument is REQUIRED to produce a plot.
            
            Example (using above plot IDs):
              "plot1:sub1,sub2;abc2:abc,def;superplot3:s1,s2"
              
          --plot-define-axes
            Key-value pairs of plot/subplot IDs, and axes properties
            defined as sub-key-value pairs. This is the first argument to
            use key hierarchy naming.
            
            Available hierarchy attributes:
              plot|subplot|x
                X axis settings.
              plot|subplot|y
                Y axis settings.
            
            Available attributes (sub-key-value pairs):
              ticks=#
                Define number of ticks.
              label=LABEL
                Define the axis label.
            
            Example (using above info):
              "plot1|sub1|x:ticks=5,label=Hello world"
            
          --plot-define-data
            Key-value pairs of plot/subplot IDs, with data fields as
            values. This also uses key hierarchy naming.
            
            This argument is REQUIRED to produce a plot.
            
            Available hierarchy attributes:
              plot|subplot|x
                X plotting settings.
              plot|subplot|y
                Y plotting settings.
            
            Values:
              Data field elements. Specified using a different hierarchy
              system:
                STEP/TYPE|FIELD
              
              STEP/TYPE is either "ges" or "anl", but not both.
              
              For instance: ges|bc_total|mean
            
            Example (using above info):
              "abc2|abc|x:timestamp;abc2|abc|y:ges|bc_total|mean,ges|bc_total|stddev"
            
          --plot-define-title
            Key-value pairs of plot/subplot IDs, with titles as values. This
            also uses key hierarchy naming, but in a slightly different way.
            
            Available hierarchy attributes:
              plot|title
                Title for the whole plot.
              plot|subplot|title
                Title for the subplot.
              plot|subplot|legend
                Title for the subplot's legend.
            
            Values:
              The title for the specified title attribute.
            
            Example (using above info):
              "abc2|title:Title;abc2|abc|title:SubTitle;abc2|abc|legend:LegendTitle"
          --plot-define-output
            Key-value pairs of plot and output paths.
            
            Example (using above info):
              "plot1:myplot1.png;abc2:abcplot.png;superplot3:super.png"
          --plot-define-settings
            Key-value pairs of plot IDs, and settings defined as
            sub-key-value pairs.
            
            This argument is REQUIRED to produce a plot.
            
            Available attributes (sub-key-value pairs):
              target_size=#x#
                Define the output plot target size.
              dpi=#
                Define the output plot DPI.
            
            Example (using above info):
              "plot1:target_size=595x700,dpi=50"
          --plot-define-custom-vars
            Key-value pairs of custom variables to be used in the plot
            title and output file name. Variables are case insensitive.
            
            The suggested variable definition and usage standard is
            using lowercase for variable definition, and uppercase for
            variable usage in the title and/or output file name.
            
            Example:
              "expid:exp_2;author:theauthor"
              
              Applying custom variables to plot title and output file name:
                --plot-define-title  "plot1:Experiment %EXPID% - By %AUTHOR%"
                  Result:
                    Experiment exp_2 - By theauthor
                --plot-define-output "plot1:plot_%EXPID%-%AUTHOR%.png"
                  Result:
                    plot_exp_2-theauthor.png
          --plot-make-dirs
            If specified, automatically make non-existent directories,
            as needed. No additional arguments or options needed.
            
        NOTE: These options are advanced - although you could (potentially)
              plot using these options, it would probably be very painful!
              All of these options can be defined via config file, which is
              much easier and less verbose! These options are meant to be
              used in conjunction with a config file for overriding certain
              configuration options and testing them.
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    add_list_args(plot_parser, True)
    add_dump_args(plot_parser, True)
    add_plot_args(plot_parser, False)

    # [config]
    config_parser = subparsers.add_parser('config', help='Displays, loads, and saves the configuration.', \
        description = textwrap.dedent("""\
        Displays, loads, and saves the configuration.
        
        Inherits arguments from [list], [dump], and [plot]. [list], [dump],
        and [plot] arguments may be required to use [config]. For information
        on [list], [dump], or [plot] arguments, see their respective help.
        """), \
        formatter_class=argparse.RawDescriptionHelpFormatter)
    add_list_args(config_parser, True)
    add_dump_args(config_parser, True)
    add_plot_args(config_parser, True)
    add_config_args(config_parser, False)
    
    return parser

def parse_to_config(parse):
    # Init a few variables:
    pyradmon_config = {}
    plot_dict = {}
    
    ## Core args
    # First, examine the core arguments.
    if isset_obj("config_file", parse):
        # OK, check if the file exists.
        if os.path.isfile(parse.config_file):
            # Attempt to load
            res = config.load(parse.config_file)
            
            if res == None:
                print "ERROR: Could not open configuration file!"
                return (None, None, None)
            
            pyradmon_config = res[0]
            plot_dict = res[1]
        else:
            print "ERROR: Configuration file path does not exist!"
            return (None, None, None)
        
        # Validate configuration
        config.validate(pyradmon_config, plot_dict)
    
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
                    return (None, None, None)
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
            return (None, None, None)
    else:
        logging_level = logging.INFO
    
    # We're ready - let's set up logging!
    logger = log.init(logging_level, logging_output, logging_file)
    
    # From now on, we'll stick to using the log module to print stuff
    # out.
    
    ## Config args, part 1
    if parse.verb == "config":
        # We will only read --config-load here. All others will be
        # checked at the end.
        if isset_obj("config_load", parse):
            if isset_obj("config_file", parse):
                warn("Detected --config-load when --config-file is already specified! --config-load will override the configuration file specified in --config-file. You should only specify one argument, preferrably --config-file.")
            
            # OK, check if the file exists.
            if os.path.isfile(parse.config_load):
                # Attempt to load
                res = config.load(parse.config_load)
                
                if res == None:
                    critical("ERROR: Could not open configuration file!")
                    return (None, None, None)
                
                pyradmon_config = res[0]
                plot_dict = res[1]
            else:
                critical("ERROR: Configuration file path does not exist!")
                return (None, None, None)
            
            # Validate configuration
            config.validate(pyradmon_config, plot_dict)
    
    ## Plot args
    # FUN TIME
    
    if parse.verb == "plot" or parse.verb == "config":
        if isset_obj("plot_define_plots", parse):
            plots = ",".join(parse.plot_define_plots).split(",")
            # Cleanup
            plots = [x.strip() for x in plots]
            
            for plot in plots:
                if not plot in plot_dict:
                    if plot == "":
                        warn("Invalid plot ID detected - plot ID can't be blank!")
                        warn("This plot definition will be skipped.")
                        continue
                    plot_dict[plot] = {}
            
        if isset_obj("plot_define_subplots", parse):
            # "plot1:sub1,sub2;abc2:abc,def;superplot3:s1,s2"
            subplots_def = ";".join(parse.plot_define_subplots).split(";")
            # Cleanup
            subplots_def = [x.strip() for x in subplots_def]
            for subplot_def in subplots_def:
                # Chunk: plot1:sub1,sub2
                subplot_def_split = subplot_def.split(":")
                subplot_def_split = [x.strip() for x in subplot_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(subplot_def_split) != 2:
                    warn("Invalid subplot definition detected - invalid key-value pair '%s'!" % subplot_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This subplot definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                subplot_def_plot = subplot_def_split[0]
                subplot_def_subplots = subplot_def_split[1]
                
                # Sanity check 2: does the plot named exist?!?
                if not subplot_def_plot in plot_dict:
                    warn("Invalid subplot definition detected - the plot specified, '%s', does not exist!" % subplot_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This subplot definition will be skipped.")
                    continue
                
                # OK, let's process subplots.
                subplot_def_subplots = subplot_def_subplots.split(",")
                subplot_def_subplots = [x.strip() for x in subplot_def_subplots]
                
                # Prep plot_dict
                if not "plots" in plot_dict[subplot_def_plot]:
                    plot_dict[subplot_def_plot]["plots"] = []
                
                # Add away!
                for subplot_def_subplot in subplot_def_subplots:
                    plot_dict[subplot_def_plot]["plots"].append({ subplot_def_subplot : {} })
                
                # Done!
            
        if isset_obj("plot_define_axes", parse):
            # "plot1|sub1|x:ticks=5,label=Hello world"
            axes_def = ";".join(parse.plot_define_axes).split(";")
            # Cleanup
            axes_def = [x.strip() for x in axes_def]
            for axis_def in axes_def:
                # Chunk: plot1|sub1|x:ticks=5,label=Hello world
                axis_def_split = axis_def.split(":")
                axis_def_split = [x.strip() for x in axis_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(axis_def_split) != 2:
                    warn("Invalid axis definition detected - invalid key-value pair '%s'!" % axis_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This axis definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: plot1|sub1|x --> [plot1, sub1, x]
                axis_def_plot_subplot_axis = axis_def_split[0].split("|")
                # Chunk: ticks=5,label=Hello world
                axis_def_attrs = axis_def_split[1]
                
                # Sanity check 2: does the plot/subplot/axe key have 3 elements?
                if len(axis_def_plot_subplot_axis) != 3:
                    warn("Invalid axis definition detected - the key is invalid! It should only have")
                    warn("3 elements - plot|subplot|x/y!")
                    warn("This axis definition will be skipped.")
                    continue
                
                # OK, let's seperate that out!
                axis_def_plot = axis_def_plot_subplot_axis[0]
                axis_def_subplot = axis_def_plot_subplot_axis[1]
                axis_def_axis = axis_def_plot_subplot_axis[2].lower()
                
                # Sanity check 3: does the plot/subplot named exist?!?
                if not axis_def_plot in plot_dict:
                    warn("Invalid axis definition detected - the plot specified, '%s', does not exist!" % axis_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This axis definition will be skipped.")
                    continue
                    
                # OK, plot exists. How about subplot?
                # We have to do some strange magic here...
                axis_def_subplot_found = False
                axis_def_subplot_dat = None
                for axis_def_subplot_dict in plot_dict[axis_def_plot]['plots']:
                    if axis_def_subplot in axis_def_subplot_dict:
                        axis_def_subplot_dat = axis_def_subplot_dict[axis_def_subplot]
                        axis_def_subplot_found = True
                        break
                
                if not axis_def_subplot_found:
                    warn("Invalid axis definition detected - the subplot specified, '%s', does not exist!" % axis_def_subplot)
                    warn("Ensure spelling is correct. If it is a new subplot, make sure it is defined and")
                    warn("in the right subplot. This axis definition will be skipped.")
                    continue
                
                # Sanity check 4: Is the axis valid?
                if axis_def_axis != "x" and axis_def_axis != "y":
                    warn("Invalid axis definition detected - the axis specified, '%s', is invalid!" % axis_def_axis)
                    warn("'x' and 'y' are the only axes allowed. This axis definition will be skipped.")
                    continue
                
                # OK, let's setup shop.
                if not "axes" in axis_def_subplot_dat:
                    axis_def_subplot_dat["axes"] = {}
                
                if not axis_def_axis in axis_def_subplot_dat["axes"]:
                    axis_def_subplot_dat["axes"][axis_def_axis] = {}
                
                # OK, let's process attributes.
                axis_def_attrs = axis_def_attrs.split(",")
                axis_def_attrs = [x.strip().split("=") for x in axis_def_attrs]
                
                # Sanity check 5: Are these valid key-value pairs?
                kvpair_bad = False
                for kvpair in axis_def_attrs:
                    if len(kvpair) != 2:
                        warn("Invalid axis definition detected - the key/value subpair, '%s', is invalid!" % '='.join(kvpair))
                        kvpair_bad = True
                    if type(kvpair[0]) != str:
                        warn("Invalid axis definition detected - the key '%s' in the subpair, '%s', is a non-string!" % (str(kvpair[0]), '='.join(kvpair)))
                
                if kvpair_bad:
                    warn("(Key-value subpair should be key=value - make sure there are no extra =s!)")
                    warn("This axis definition will be skipped.")
                    continue
                
                # Whew, so much sanity lost from sanity checking!
                
                # Install attributes!
                for kvpair in axis_def_attrs:
                    if kvpair[0] == 'ticks':
                        axis_def_subplot_dat["axes"][axis_def_axis][kvpair[0]] = int(kvpair[1])
                    else:
                        axis_def_subplot_dat["axes"][axis_def_axis][kvpair[0]] = kvpair[1]
                
                # Done!!!!!1111
        
        if isset_obj("plot_define_data", parse):
            # "abc2|abc|x:timestamp;abc2|abc|y:ges|bc_total|mean,ges|bc_total|stddev"
            data_defs = ";".join(parse.plot_define_data).split(";")
            # Cleanup
            data_defs = [x.strip() for x in data_defs]
            for data_def in data_defs:
                # Chunk: abc2|abc|x:timestamp
                # Chunk: abc2|abc|y:ges|bc_total|mean,ges|bc_total|stddev
                data_def_split = data_def.split(":")
                data_def_split = [x.strip() for x in data_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(data_def_split) != 2:
                    warn("Invalid data definition detected - invalid key-value pair '%s'!" % data_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This data definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: abc2|abc|x --> [abc2, abc, x]
                data_def_plot_subplot_attr = data_def_split[0].split("|")
                # Chunk: timestamp
                data_def_attrs = data_def_split[1]
                
                # Sanity check 2: does the plot/subplot/axe key have 3 elements?
                if len(data_def_plot_subplot_attr) != 3:
                    warn("Invalid data definition detected - the key is invalid! It should only have")
                    warn("3 elements - plot|subplot|x/y!")
                    warn("This data definition will be skipped.")
                    continue
                
                # OK, let's seperate that out!
                data_def_plot = data_def_plot_subplot_attr[0]
                data_def_subplot = data_def_plot_subplot_attr[1]
                data_def_attr_name = data_def_plot_subplot_attr[2].lower()
                
                # Sanity check 3: does the plot/subplot named exist?!?
                if not data_def_plot in plot_dict:
                    warn("Invalid data definition detected - the plot specified, '%s', does not exist!" % data_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This data definition will be skipped.")
                    continue
                    
                # OK, plot exists. How about subplot?
                # We have to do some strange magic here...
                data_def_subplot_found = False
                data_def_subplot_dat = None
                for data_def_subplot_dict in plot_dict[data_def_plot]['plots']:
                    if data_def_subplot in data_def_subplot_dict:
                        data_def_subplot_dat = data_def_subplot_dict[data_def_subplot]
                        data_def_subplot_found = True
                        break
                
                if not data_def_subplot_found:
                    warn("Invalid data definition detected - the subplot specified, '%s', does not exist!" % data_def_subplot)
                    warn("Ensure spelling is correct. If it is a new subplot, make sure it is defined and")
                    warn("in the right subplot. This data definition will be skipped.")
                    continue
                
                # Sanity check 4: Is the attr field valid?
                valid_attrs = [ "x", "y", "colors", "labels" ]
                if not data_def_attr_name in valid_attrs:
                    warn("Invalid data definition detected - the attribute specified, '%s', is invalid!" % data_def_data)
                    warn("%s are the only attributes allowed. This data definition will be skipped." % (",".join(valid_attrs[:-1]) + ", and " + valid_attrs[-1]))
                    continue
                
                # OK, let's setup shop.
                if not "data" in data_def_subplot_dat:
                    data_def_subplot_dat["data"] = {}
                
                # OK, let's process attributes.
                data_def_attrs = data_def_attrs.split(",")
                
                # Whew, so much sanity lost from sanity checking!
                # (But not as bad as the axes part...)
                
                # Install attributes!
                if len(data_def_attrs) == 1:
                    data_def_subplot_dat["data"][data_def_attr_name] = data_def_attrs[0]
                else:
                    if not data_def_attr_name in data_def_subplot_dat["data"]:
                        data_def_subplot_dat["data"][data_def_attr_name] = []
                    for attr_val in data_def_attrs:
                        data_def_subplot_dat["data"][data_def_attr_name].append(attr_val)
                
                # Done!
        
        if isset_obj("plot_define_title", parse):
            # "abc2|title:Title;abc2|abc|title:SubTitle;abc2|abc|legend:LegendTitle"
            title_defs = ";".join(parse.plot_define_title).split(";")
            # Cleanup
            title_defs = [x.strip() for x in title_defs]
            for title_def in title_defs:
                # Chunk: abc2|title:Title
                # Chunk: abc2|abc|title:SubTitle
                # Chunk: abc2|abc|legend:LegendTitle
                title_def_split = title_def.split(":")
                title_def_split = [x.strip() for x in title_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(title_def_split) != 2:
                    warn("Invalid title definition detected - invalid key-value pair '%s'!" % title_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This title definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: abc2|title      --> [abc2, title]
                # Chunk: abc2|abc|title  --> [abc2, abc, title]
                # Chunk: abc2|abc|legend --> [abc2, abc, legend]
                title_def_plot_subplot_attr = title_def_split[0].split("|")
                # Chunk: Title
                # Chunk: SubTitle
                # Chunk: LegendTitle
                title_def_title = title_def_split[1]
                
                # Sanity check 2: does the plot(/subplot)/attr key have 2 or 3 elements?
                if (len(title_def_plot_subplot_attr) != 3) and (len(title_def_plot_subplot_attr) != 2):
                    warn("Invalid title definition detected - the key is invalid! It should only have")
                    warn("2-3 elements - plot|title or plot|subplot|title/legend!")
                    warn("This title definition will be skipped.")
                    continue
                
                # OK, let's seperate that out!
                # ...except this varies, so let's take it a bit slow.
                
                title_def_plot_subplot = [ title_def_plot_subplot_attr[0] ]
                
                if len(title_def_plot_subplot_attr) == 3:
                    title_def_plot_subplot.append(title_def_plot_subplot_attr[1])
                
                title_def_attr_name = title_def_plot_subplot_attr[-1].lower()
                
                # Sanity check 3: does the plot/subplot named exist?!?
                if not title_def_plot_subplot[0] in plot_dict:
                    warn("Invalid title definition detected - the plot specified, '%s', does not exist!" % title_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This title definition will be skipped.")
                    continue
                
                # OK, plot exists. How about subplot?
                # We have to do some strange magic here...
                # ...but only if we need to.
                
                if len(title_def_plot_subplot) == 2:
                    title_def_subplot_found = False
                    title_def_subplot_dat = None
                    for title_def_subplot_dict in plot_dict[title_def_plot_subplot[0]]['plots']:
                        if title_def_plot_subplot[1] in title_def_subplot_dict:
                            title_def_subplot_dat = title_def_subplot_dict[title_def_plot_subplot[1]]
                            title_def_subplot_found = True
                            break
                    
                    if not title_def_subplot_found:
                        warn("Invalid title definition detected - the subplot specified, '%s', does not exist!" % title_def_subplot)
                        warn("Ensure spelling is correct. If it is a new subplot, make sure it is defined and")
                        warn("in the right subplot. This title definition will be skipped.")
                        continue
                
                # Sanity check 4: Is the attr field valid?
                # Title is valid for both, but legend is only valid for
                # plot|subplot.
                if title_def_attr_name != "title" and not ( (len(title_def_plot_subplot) == 2) and (title_def_attr_name == "legend") ):
                    warn("Invalid title definition detected - the attribute specified, '%s', is invalid!" % title_def_title)
                    warn("legend (for plot|subplot) and title are the only attributes allowed.")
                    warn("This title definition will be skipped.")
                    continue
                
                # OK, let's go!
                if len(title_def_plot_subplot) == 1:
                    plot_dict[title_def_plot_subplot[0]]["title"] = title_def_title
                else:
                    if title_def_attr_name == "legend":
                        if not isset_obj("legend", title_def_subplot_dat):
                            title_def_subplot_dat["legend"] = {}
                        title_def_subplot_dat["legend"]["title"] = title_def_title
                    else:
                        title_def_subplot_dat["title"] = title_def_title
                
                # Done!
        
        if isset_obj("plot_define_output", parse):
            # "plot1:myplot1.png;abc2:abcplot.png;superplot3:super.png"
            output_defs = ";".join(parse.plot_define_output).split(";")
            # Cleanup
            output_defs = [x.strip() for x in output_defs]
            for output_def in output_defs:
                # Chunk: plot1:myplot1.png
                output_def_split = output_def.split(":")
                output_def_split = [x.strip() for x in output_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(output_def_split) != 2:
                    warn("Invalid output definition detected - invalid key-value pair '%s'!" % output_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This output definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: plot1
                output_def_plot = output_def_split[0]
                # Chunk: myplot1.png
                output_def_output = output_def_split[1]
                
                # Sanity check 2: does the plot named exist?!?
                if not output_def_plot in plot_dict:
                    warn("Invalid output definition detected - the plot specified, '%s', does not exist!" % output_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This output definition will be skipped.")
                    continue
                
                # OK, plot exists. This is super easy, so we're free to
                # fly from here!
                plot_dict[output_def_plot]["output"] = output_def_output
                
                # Done!
        
        if isset_obj("plot_define_settings", parse):
            # "plot1:target_size=595x700,dpi=50"
            settings_def = ";".join(parse.plot_define_settings).split(";")
            # Cleanup
            settings_def = [x.strip() for x in settings_def]
            for settings_def in settings_def:
                # Chunk: plot1:target_size=595x700,dpi=50
                settings_def_split = settings_def.split(":")
                settings_def_split = [x.strip() for x in settings_def_split]
                
                # SAAAAAAAANITY CHECK!!!!!!!1111
                
                # Sanity check 1: do we have 2 elements?
                if len(settings_def_split) != 2:
                    warn("Invalid settings definition detected - invalid key-value pair '%s'!" % settings_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This settings definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: plot1
                settings_def_plot = settings_def_split[0]
                # Chunk: ticks=5,label=Hello world
                settings_def_attrs = settings_def_split[1]
                
                # Sanity check 2: does the plot/subplot named exist?!?
                if not settings_def_plot in plot_dict:
                    warn("Invalid settings definition detected - the plot specified, '%s', does not exist!" % settings_def_plot)
                    warn("Ensure spelling is correct. If it is a new plot, make sure it is defined.")
                    warn("This settings definition will be skipped.")
                    continue
                
                # OK, let's setup shop.
                if not "settings" in plot_dict[settings_def_plot]:
                    plot_dict[settings_def_plot]["settings"] = {}
                
                # OK, let's process attributes.
                settings_def_attrs = settings_def_attrs.split(",")
                settings_def_attrs = [x.strip().split("=") for x in settings_def_attrs]
                
                # Sanity check 5: Are these valid key-value pairs?
                kvpair_bad = False
                for kvpair in settings_def_attrs:
                    if len(kvpair) != 2:
                        warn("Invalid settings definition detected - the key/value subpair, '%s', is invalid!" % '='.join(kvpair))
                        kvpair_bad = True
                    if type(kvpair[0]) != str:
                        warn("Invalid settings definition detected - the key '%s' in the subpair, '%s', is a non-string!" % (str(kvpair[0]), '='.join(kvpair)))
                
                if kvpair_bad:
                    warn("(Key-value subpair should be key=value - make sure there are no extra =s!)")
                    warn("This settings definition will be skipped.")
                    continue
                
                # Whew, so much sanity lost from sanity checking!
                
                # Install attributes!
                for kvpair in settings_def_attrs:
                    if kvpair[0] == 'target_size':
                        size_arr = [ int(x) for x in kvpair[1].lower().split("x") ]
                        if len(size_arr) != 2:
                            warn("Key-value pair for target_size is invalid - should be INTxINT!")
                            warn("Skipping key-value pair.")
                            continue
                        plot_dict[settings_def_plot]["settings"]["target_size"] = size_arr
                    elif kvpair[0] == 'dpi':
                        if not kvpair[1].isdigit():
                            warn("Key-value pair for dpi is invalid - value is not an int!")
                            warn("Skipping key-value pair.")
                            continue
                        plot_dict[settings_def_plot]["settings"][kvpair[0]] = int(kvpair[1])
                    else:
                        # Strange stuff
                        warn("Key '%s' in not defined - setting anyway." % str(kvpair[0]))
                        plot_dict[settings_def_plot]["settings"][kvpair[0]] = kvpair[1]
                
                # Done!!!!!1111
        if isset_obj("plot_define_custom_vars", parse):
            # "customvar1:value1;customvar2:value2"
            custom_var_defs = ";".join(parse.plot_define_custom_vars).split(";")
            # Cleanup
            custom_var_defs = [x.strip() for x in custom_var_defs]
            for output_def in output_defs:
                # Chunk: customvar1:value1
                custom_var_def_split = custom_var_def.split(":")
                custom_var_def_split = [x.strip() for x in custom_var_def_split]
                
                # Sanity check!
                
                # Sanity check 1: do we have 2 elements?
                if len(custom_var_def_split) != 2:
                    warn("Invalid custom variable definition detected - invalid key-value pair '%s'!" % output_def)
                    warn("(Key-value pair should be key:value - make sure there are no extra colons!)")
                    warn("This custom variable definition will be skipped.")
                    continue
                
                # OK, now seperate it out!
                # Chunk: customvar1
                custom_var_def_var = custom_var_def_split[0]
                # Chunk: value1
                custom_var_def_val = custom_var_def_split[1]
                
                # OK, we got everything. This is super easy, so we're free to
                # leap from here!
                if "custom_vars" not in pyradmon_config:
                    pyradmon_config["custom_vars"] = {}
                pyradmon_config["custom_vars"][custom_var_def_var] = custom_var_def_val
                
                # Done!
        if isset_obj("plot_make_dirs", parse) and parse.plot_make_dirs:
            pyradmon_config["make_dirs"] = parse.plot_make_dirs
            
            # Done!
    
    ## Dump args
    if parse.verb == "dump" or parse.verb == "plot" or parse.verb == "config":        
        # --dump-columns
        if isset_obj("dump_columns", parse):
            for data_column in (parse.dump_columns).split(","):
                data_column = data_column.strip()
                if not data_column in SPECIAL_FIELDS:
                    if not ((data_column.startswith("ges|") or data_column.startswith("anl|"))):
                        die("ERROR: Invalid data column '%s' specified in --dump-columns! Must have ges| or anl| as a prefix." % data_column)
            
            pyradmon_config["data_columns"] = parse.dump_columns
        
        # --dump-all-channels
        if isset_obj("dump_all_channels", parse) and parse.dump_all_channels:
            pyradmon_config["data_all_channels"] = parse.dump_all_channels
        
        # --dump-channels
        if isset_obj("dump_channels", parse):
            if isset_obj("dump_all_channels", parse) and parse.dump_all_channels:
                die("ERROR: You can not specify --dump-all-channels and --dump-channels at the same time!")
            for data_channel in (parse.dump_channels).split(","):
                data_channel = data_channel.strip()
                
                if not ( (data_channel.isdigit()) or \
                    ( (len(data_channel.split("-")) == 2) and data_channel.split("-")[0].isdigit() and data_channel.split("-")[1].isdigit() ) ):
                    die("ERROR: Invalid data channel '%s' specified in --dump-channels! Must be a number or a numeric range (#-#)." % data_channel)
            
            pyradmon_config["data_channels"] = parse.dump_channels
        
        # --dump-assim-only
        if isset_obj("dump_assim_only", parse):
            pyradmon_config["data_assim_only"] = parse.dump_assim_only
    
    ## List args
    if parse.verb == "list" or parse.verb == "dump" or parse.verb == "plot" or parse.verb == "config":
        # --data-all (action flag) 
        if isset_obj("data_all", parse):
            pyradmon_config["data_all"] = parse.data_all
        
        # --data-single-date (action flag)
        if isset_obj("data_single_date", parse):
            if isset_obj("data_all", parse):
                die("ERROR: You can not specify --data-all and --data-single-date at the same time!")
            pyradmon_config["data_start_date"] = parse.data_single_date
            pyradmon_config["data_end_date"] = parse.data_single_date
        
        # --data-base-directory 
        if isset_obj("data_base_directory", parse):
            pyradmon_config["data_base_directory"] = parse.data_base_directory
        
        # --data-experiment-id
        if isset_obj("data_experiment_id", parse):
            pyradmon_config["data_experiment_id"] = parse.data_experiment_id
        
        # --data-start-date
        if isset_obj("data_start_date", parse):
            if isset_obj("data_all", parse):
                die("ERROR: You can not specify --data-all and --data-start-date at the same time!")
            if isset_obj("data_single_date", parse):
                die("ERROR: You can not specify --data-single-date and --data-start-date at the same time!")
            
            # FORMAT: YYYY-MM-DD HHz
            pyradmon_config["data_start_date"] = parse.data_start_date
            
            if not (pyradmon_config["data_start_date"][:4].isdigit() and \
                pyradmon_config["data_start_date"][5:7].isdigit() and \
                pyradmon_config["data_start_date"][8:10].isdigit() and \
                pyradmon_config["data_start_date"][11:13].isdigit()):
                die("ERROR: Start date '%s' specified in --data-start-date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_config["data_start_date"])
        
        # --data-end-date
        if isset_obj("data_end_date", parse):
            if isset_obj("data_all", parse):
                die("ERROR: You can not specify --data-all and --data-end-date at the same time!")
            if isset_obj("data_single_date", parse):
                die("ERROR: You can not specify --data-single-date and --data-end-date at the same time!")
            
            # FORMAT: YYYY-MM-DD HHz
            pyradmon_config["data_end_date"] = parse.data_end_date
            
            if not (pyradmon_config["data_end_date"][:4].isdigit() and \
                pyradmon_config["data_end_date"][5:7].isdigit() and \
                pyradmon_config["data_end_date"][8:10].isdigit() and \
                pyradmon_config["data_end_date"][11:13].isdigit()):
                die("ERROR: End date '%s' specified in --data-end-date is not valid! It must be in 'YYYY-MM-DD HHz' format!" % pyradmon_config["data_end_date"])
        
        # --data-instrument-sat
        if isset_obj("data_instrument_sat", parse):
            pyradmon_config["data_instrument_sat"] = parse.data_instrument_sat
        
        # --data-step
        if isset_obj("data_step", parse):
            pyradmon_config["data_step"] = parse.data_step
            if not ((pyradmon_config['data_step'] == "anl") or \
                (pyradmon_config['data_step'] == "ges") or \
                (pyradmon_config['data_step'] == "anl|ges") or \
                (pyradmon_config['data_step'] == "ges|anl")):
                die("ERROR: Data step '%s' specified in --date-step is not valid! Must either be 'anl', 'ges', or the two combined with a pipe ('anl|ges')." % pyradmon_config["data_step"])
        
        # --data-time-delta
        if isset_obj("data_time_delta", parse):
            pyradmon_config["data_time_delta"] = parse.data_time_delta
            
            dtd_split = pyradmon_config['data_time_delta'].split(" ")
            unit_valid = [ "s", "w", "m", "M", "h", "y", "d" ]
            
            for dtd in dtd_split:
                #  s: seconds    m: minutes    h: hours    d: days
                #  w: weeks      M: months     y: years
                if not ( (dtd[-1] in unit_valid) and (dtd[:-1].isdigit()) ):
                    die("ERROR: Invalid delta time '%s' specified in --data-delta-time! Must be a # followed by a valid unit letter. ([s]ecs, [m]inutes, [h]ours, [d]ays, [w]eeks, [M]onths, [y]ears)" % pyradmon_config["data_delta_time"])
    
    if isset_obj("config_unset", parse):
        # "config.var1;plot1|subplot1"
        config_unset_def = ";".join(parse.plot_define_subplots).split(";")
        
    
    #import pprint
    #pprint.pprint(plot_dict)
        
    #print plot_dict
    
    return (pyradmon_config, plot_dict, parse)

if __name__ == "__main__":
    parser = make_argparser()
    parse = parser.parse_args()
    print parse_to_config(parse)
