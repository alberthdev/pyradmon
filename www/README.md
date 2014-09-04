Introduction
============
Included is a php webpage to visualize the pyradmon output.  Output from pyradmon that follows the:

EXPERIMENT/TIME/INSTRUMENT/images

following the radiance_plots.yaml.tmpl output structure should be placed in a subdirectory of the directory containing the index.php file named radmon_data.

e.g. http://host.com/radmon/index.php, the data should be in:
radmon/radmon_data

The website is smart enough to populate itself from this directory structure.  If a new instrument is added, it needs to be added to the table at the beginning of index.php 
