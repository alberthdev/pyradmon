Getting Started - User
***********************************************************************

As a user of **PyRadmon**, you probably want to use **PyRadmon** for
creating radiance monitoring plots. This guide will help you achieve
that!

This guide is for running and using **PyRadmon** to search, extract, 
and plot data.

Getting PyRadmon
================
If you haven't already done so, get PyRadmon now!

:doc:`getting-pyradmon`

Speedy Start
============
The first thing you probably want to do is make a plot, right? It's 
really simple!

#. **Creating Your Configuration File, Part 1**\
   
   First, create a new file called myconfig.yaml. Copy the following text into
   this new file:
   
   .. code-block:: yaml
   
    config:
      data_path_format: PATH_TO_PROCESSED_TXT_FILES
      data_step: anl|ges
      data_start_date: YYYY-MM-DD HHz
      data_end_date: YYYY-MM-DD HHz
      experiment_id: EXPERIMENT_ID
      data_instrument_sat: INSTRUMENT_SAT
      data_channels: DATA_CHANNEL_RANGE
      
   Replace ``YYYY-MM-DD HHz`` in ``data_start_date`` with your desired 
   data start date, with the format given above. (``YYYY-MM-DD HHz``)
   
   **Note that all digits must be filled!** (For instance, if month is 
   ``5``, it should be written as ``05``.)
   
   Replace ``YYYY-MM-DD HHz`` in ``data_end_date`` with your desired 
   data end date, with the format given above. (``YYYY-MM-DD HHz``) 
   Again, the above rules apply!
   
   Now replace ``INSTRUMENT_SAT`` in ``data_instrument_sat`` with the 
   instrument/satellite ID, and ``EXPERIMENT_ID`` in ``experiment_id`` 
   with the experiment ID.
   
   Now replace ``DATA_CHANNEL_RANGE`` in ``data_channels`` with a 
   numeric channel range and/or comma-seperated channel/channel range. 
   Examples::
   
    1,2-5,10
    1-10
    1,3,5
    1
   
   Finally, replace ``PATH_TO_PROCESSED_TXT_FILES`` in 
   ``data_path_format`` with the correct path to the processed text 
   files. This path is templated with %VAR% variables. Here's an 
   example::
   
    MERRA2/%EXPERIMENT_ID%/obs/Y%YEAR4%/M%MONTH2%/D%DAY2%/H%HOUR2%/%EXPERIMENT_ID%.diag_%INSTRUMENT_SAT%_%DATA_TYPE%.%YEAR4%%MONTH2%%DAY2%_%HOUR2%z.txt
    
   So many variables! Here's a breakdown of available variables:
   
   +--------------------+-------------------------------------------+
   | Variable           | Description                               |
   +====================+===========================================+
   | %EXPERIMENT_ID%    | The current experiment ID for the data.   |
   +--------------------+-------------------------------------------+
   | %INSTRUMENT_SAT%   | The current instrument/satellite ID for   |
   |                    | the data.                                 |
   +--------------------+-------------------------------------------+
   | %DATA_TYPE%        | The current data type for the data.       |
   |                    | Typically 'anl' or 'ges' - can be         |
   |                    | different depending on your data.         |
   +--------------------+-------------------------------------------+
   | %YEAR4%            | The current full 4-digit year for the     |
   +--------------------+ data.                                     |
   | %YEAR%             |                                           |
   +--------------------+-------------------------------------------+
   | %YEAR2%            | The current 2-digit abbreviated year for  |
   |                    | the data.                                 |
   +--------------------+-------------------------------------------+
   | %MONTH2%           | The current full 2-digit month for the    |
   +--------------------+ data.                                     |
   | %MONTH%            |                                           |
   +--------------------+-------------------------------------------+
   | %DAY2%             | The current full 2-digit day for the      |
   +--------------------+ data.                                     |
   | %DAY%              |                                           |
   +--------------------+-------------------------------------------+
   | %HOUR2%            | The current full 2-digit hour for the     |
   +--------------------+ data.                                     |
   | %HOUR%             |                                           |
   +--------------------+-------------------------------------------+
   
   Once done, your config file should look similar (but not necessary 
   exactly) this::
   
    config:
      data_path_format: MERRA2/%EXPERIMENT_ID%/obs/Y%YEAR4%/M%MONTH2%/D%DAY2%/H%HOUR2%/%EXPERIMENT_ID%.diag_%INSTRUMENT_SAT%_%DATA_TYPE%.%YEAR4%%MONTH2%%DAY2%_%HOUR2%z.txt
      data_step: anl|ges
      data_start_date: 1991-01-01 00z
      data_end_date: 1991-02-28 18z
      experiment_id: d5124_m2_jan91
      data_instrument_sat: ssmi_f08
      data_channels: 1-7
   
#. **Creating Your Configuration File, Part 2**
   
   So now you have your data source parameters. What now? Well, data 
   isn't interesting without graphing it! 
