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
# Test Data -
#   data for testing out the library!
# 

TEST_DATA_VARS = [
                "timestamp",
                "frequency",
                "iuse",
                "ges|bc_total|mean",
                "ges|bc_total|stddev",
                "ges|bc_fixang|mean",
                "ges|bc_fixang|stddev",
                "ges|bc_const|mean",
                "ges|bc_const|stddev",
                "ges|bc_satang|mean",
                "ges|bc_satang|stddev",
                "ges|bc_tlap|mean",
                "ges|bc_tlap|stddev",
                "ges|bc_tlap2|mean",
                "ges|bc_tlap2|stddev",
                "ges|bc_clw|mean",
                "ges|bc_clw|stddev",
                "ges|bc_coslat|mean",
                "ges|bc_coslat|stddev",
                "ges|bc_sinlat|mean",
                "ges|bc_sinlat|stddev",
                "ges|Obs Error|mean",
                "anl|Obs Error|mean",
                "ges|Cost (Jo)|mean",
                "anl|Cost (Jo)|mean",
                "ges|O-F BC|mean",
                "anl|O-F BC|mean",
                "ges|O-F BC|stddev",
                "anl|O-F BC|stddev",
                "ges|#total obs",
                "anl|#total obs",
                "ges|#assim obs",
                "anl|#assim obs",
                "ges|Tb-Total|mean",
                "ges|Tb-Assim|mean",
                "ges|O-F noBC|mean",
                "ges|O-F noBC|stddev",
            ]

BAD_TEST_DATA_VARS = [
                "timestamp",
                "frequency",
                "iuse",
                "iuse",
                "ges|bc_total|mean",
                "ges|bc_total|stddev",
                "ges|bc_fixang|mean",
                "ges|bc_fixang|stddev",
                "ges|bc_const|mean",
                "ges|bc_const|stddev",
                "ges|bc_satang|mean",
                "ges|bc_satang|stddev",
                "ges|bc_tlap|mean",
                "ges|bc_tlap|stddev",
                "ges|bc_tlap2|mean",
                "ges|bc_tlap2|stddev",
                "ges|bc_clw|mean",
                "ges|bc_clw|stddev",
                "ges|bc_coslat|mean",
                "ges|bc_coslat|stddev",
                "ges|bc_sinlat|mean",
                "ges|bc_sinlat|stddev",
                "ges|Obs Error|mean",
                "anl|Obs Error|mean",
                "ges|Cost (Jo)|mean",
                "anl|Cost (Jo)|mean",
                "ges|O-F BC|mean",
                "anl|O-F BC|mean",
                "ges|O-F BC|stddev",
                "anl|O-F BC|stddev",
                "ges|#total obs",
                "anl|#total obs",
                "ges|#assim obs",
                "anl|#assim obs",
                "ges|Tb-Total|mean",
                "ges|Tb-Assim|mean",
                "ges|O-F noBC|mean",
                "ges|O-F noBC|stddev",
            ]

plot_dict = {
   'plot1': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Total Bias",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_total|mean", "ges|bc_total|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ],
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Scan Angle",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_fixang|mean", "ges|bc_fixang|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_const|mean", "ges|bc_const|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "Sat Zen Ang",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_satang|mean", "ges|bc_satang|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "Lapse Rate",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_tlap|mean", "ges|bc_tlap|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot6_id':
            {
                 'title': "Lapse Rate**2",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_tlap2|mean", "ges|bc_tlap2|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot7_id':
            {
                 'title': "CLW",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_clw|mean", "ges|bc_clw|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot8_id':
            {
                 'title': "Cosine Lat",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_coslat|mean", "ges|bc_coslat|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot9_id':
            {
                 'title': "Sine lat",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_sinlat|mean", "ges|bc_sinlat|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot.png",
     },
   'plot2': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Number of Radiance",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|#total obs", "ges|#assim obs" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Observation Error",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Obs Error|mean", "anl|Obs Error|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Err Bkg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Err Anl (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Penalty Contribution",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Cost (Jo)|mean", "anl|Cost (Jo)|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Jo Bkg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Jo Anl (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "O-F & O-A Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|mean", "anl|O-F BC|mean" ],
                     'colors' : [ 'red', 'green' ],
                     'labels' : [
                                   (
                                      "O-F (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "O-A (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "O-F & O-A Standard Deviation",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|stddev", "anl|O-F BC|stddev" ],
                     'colors' : [ 'red', 'green' ],
                     'labels' : [
                                   (
                                      "O-F (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "O-A (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot_2.png",
     },
   'plot3': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Number of Radiance",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|#total obs", "ges|#assim obs" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Brightness Temperature",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Tb-Total|mean", "ges|Tb-Assim|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Total Bias Correction",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_total|mean", "ges|bc_total|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "O-F Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|mean", "ges|O-F noBC|mean" ],
                     'colors' : [ 'green', 'red' ],
                     'labels' : [
                                   (
                                      "BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "no BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "O-F Standard Deviation",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|stddev", "ges|O-F noBC|stddev" ],
                     'colors' : [ 'green', 'red' ],
                     'labels' : [
                                   (
                                      "BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "no BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot_3.png",
     }
}
plot_dict_with_pp = {
   'plot1': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Total Bias",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_total|mean", "ges|bc_total|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ],
                     'post_processing': {
                                           'x': '[n + datetime.timedelta(days=365) for n in x]',
                                           'y': '[1.234 for _ in y]',
                                        },
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Scan Angle",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_fixang|mean", "ges|bc_fixang|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_const|mean", "ges|bc_const|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "Sat Zen Ang",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_satang|mean", "ges|bc_satang|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "Lapse Rate",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_tlap|mean", "ges|bc_tlap|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot6_id':
            {
                 'title': "Lapse Rate**2",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_tlap2|mean", "ges|bc_tlap2|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot7_id':
            {
                 'title': "CLW",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_clw|mean", "ges|bc_clw|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot8_id':
            {
                 'title': "Cosine Lat",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_coslat|mean", "ges|bc_coslat|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
        {
          'subplot9_id':
            {
                 'title': "Sine lat",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_sinlat|mean", "ges|bc_sinlat|stddev" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'line'        : True,
                     'border'      : False,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot.png",
     },
   'plot2': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Number of Radiance",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|#total obs", "ges|#assim obs" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Observation Error",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Obs Error|mean", "anl|Obs Error|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Err Bkg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Err Anl (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Penalty Contribution",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Cost (Jo)|mean", "anl|Cost (Jo)|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Jo Bkg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Jo Anl (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "O-F & O-A Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|mean", "anl|O-F BC|mean" ],
                     'colors' : [ 'red', 'green' ],
                     'labels' : [
                                   (
                                      "O-F (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "O-A (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "O-F & O-A Standard Deviation",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|stddev", "anl|O-F BC|stddev" ],
                     'colors' : [ 'red', 'green' ],
                     'labels' : [
                                   (
                                      "O-F (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "O-A (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot_2.png",
     },
   'plot3': {
      'title': (
                  '%INSTRUMENT_SAT%   %START_DATE%-%END_DATE%\n'
                  'Channel %CHANNEL%  %FREQUENCY%       %ASSIMILATION_STATUS%\n'
                  'Global  All    %EXPERIMENT_ID%'
               ),
      'plots': 
       [ 
        {
          'subplot1_id':
            {
                 'title': "Number of Radiance",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|#total obs", "ges|#assim obs" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot2_id':
            {
                 'title': "Brightness Temperature",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|Tb-Total|mean", "ges|Tb-Assim|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "All Obs (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Used Obs (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot3_id':
            {
                 'title': "Total Bias Correction",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|bc_total|mean", "ges|bc_total|mean" ],
                     'colors' : [ 'blue', 'red' ],
                     'labels' : [
                                   (
                                      "Avg (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "Sdv (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot4_id':
            {
                 'title': "O-F Mean",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|mean", "ges|O-F noBC|mean" ],
                     'colors' : [ 'green', 'red' ],
                     'labels' : [
                                   (
                                      "BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "no BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
        {
          'subplot5_id':
            {
                 'title': "O-F Standard Deviation",
                 'data': {
                     'x'      : [ "timestamp" ],
                     'y'      : [ "ges|O-F BC|stddev", "ges|O-F noBC|stddev" ],
                     'colors' : [ 'green', 'red' ],
                     'labels' : [
                                   (
                                      "BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                   (
                                      "no BC (K)\n"
                                      "%AVERAGE%"
                                   ),
                                ]
                   },
                 'axes': 
                   {
                     'x': {
                            'ticks'  : 6,
                            'label'  : None,
                          },
                     'y': {
                            'ticks'  : 5,
                            'label'  : None,
                          },
                   },
               'legend':
                   {
                     'title'       : None,
                     'border'      : False,
                     'line'        : True,
                   },
            },
        },
       ],
      'settings': {
                     'dpi'        : 50,
                     'target_size': [595, 770],
                  },
      'output'  : "test_plot_3.png",
     }
}
metadata_dict = {
    'base_directory'    : "MERRA2/",
    'experiment_id'     : "d5124_m2_jan91",
    'start_year'        : "1991",
    'start_month'       : "01",
    'start_day'         : "01",
    'start_hour'        : "00",
    'end_year'          : "1991",
    'end_month'         : "02",
    'end_day'           : "28",
    'end_hour'          : "18",
    'instrument_sat'    : "ssmi_f08",
    'channel'           : 4,
}
