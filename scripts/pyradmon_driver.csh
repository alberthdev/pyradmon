#!/bin/csh

#setenv ESMADIR /gpfsm/dnb02/wrmccart/progress_cvs/GEOSadas-5_13_0
#source $ESMADIR//src/g5_modules loadmodules
#module load comp/intel-13.1.2.183 other/mpi/mvapich2-1.8.1/intel-13.1.2.183   
#module load other/comp/gcc-4.6.3-sp1 lib/mkl-13.0.1.117
#module load other/SIVO-PyD/spd_1.15.0_gcc-4.6.3-sp1_mkl-13.0.1.117

setenv ESMADIR /gpfsm/dnb02/wrmccart/progress_cvs/GEOSadas-5_13_0
source /gpfsm/dnb02/wrmccart/progress_cvs/GEOSadas-5_13_0/src/g5_modules loadmodules
module list
module unload other/comp/gcc-4.5
module load other/comp/gcc-4.6.3-sp1
module load lib/mkl-13.0.1.117
module load other/SIVO-PyD/spd_1.15.0_gcc-4.6.3-sp1_mkl-13.0.1.117


if ( $#argv > 3 || $#argv < 3 ) then
    echo "usage: pyradmon_driver.csh <experiment rc file> <start YYYYMMDD> <end YYYYMMDD>"
    echo "   example: ./pyradmon_driver.csh pyradmon_driver.example.rc 20140601 20140814"
    exit 99
endif

set rcfile=$argv[1]
set startdate=$argv[2]
set enddate=$argv[3]

set data_dirbase=`$ESMADIR/Linux/bin/echorc.x -rc $rcfile data_dirbase`
set expid=`$ESMADIR/Linux/bin/echorc.x -rc $rcfile expid`
set scratch_dir=`$ESMADIR/Linux/bin/echorc.x -rc $rcfile scratch_dir`
set output_dir=`$ESMADIR/Linux/bin/echorc.x -rc $rcfile output_dir`
set pyradmon_path=`$ESMADIR/Linux/bin/echorc.x -rc $rcfile pyradmon_path`

echo "Determining instruments for $expid from $startdate to $enddate.  This "
echo "  may take a while..."
set insts=`$pyradmon_path/scripts/determine_inst.csh $data_dirbase/$expid $startdate $enddate`
echo $pyradmon_path/scripts/determine_inst.csh $data_dirbase/$expid $startdate $enddate

set syyyy = `echo $startdate |cut -b1-4`
set smm   = `echo $startdate |cut -b5-6`
set sdd   = `echo $startdate |cut -b7-8`
set shh   = "00z"

set eyyyy = `echo $enddate |cut -b1-4`
set emm   = `echo $enddate |cut -b5-6`
set edd   = `echo $enddate |cut -b7-8`
set ehh   = "18z"

set pyr_startdate="$syyyy-$smm-$sdd $shh"
set pyr_enddate="$eyyyy-$emm-$edd $ehh"



foreach inst ($insts) 
  if (-e $pyradmon_path/config/radiance_plots.$inst.yaml.tmpl) then
    set configtmpl="$pyradmon_path/config/radiance_plots.$inst.yaml.tmpl"
  else
    set configtmpl="$pyradmon_path/config/radiance_plots.yaml.tmpl"
  endif

  set configfile="$scratch_dir/$inst.$expid.$startdate.$enddate.plot.yaml"

  cp $configtmpl $configfile

  sed -i "s@>>>DATA_DIRBASE<<<@$data_dirbase@g" $configfile
  sed -i "s/>>>STARTDATE<<</$pyr_startdate/g" $configfile 
  sed -i "s/>>>ENDDATE<<</$pyr_enddate/g" $configfile 
  sed -i "s/>>>EXPID<<</$expid/g" $configfile 
  sed -i "s@>>>OUTPUT_DIR<<<@$output_dir@g" $configfile 

  echo "Running PyRadMon for $inst from $pyr_startdate to $pyr_enddate"
  $pyradmon_path/pyradmon.py --config-file $configfile plot --data-instrument-sat $inst
end



