#!/bin/csh -f

set ESMADIR=/gpfsm/dnb02/wrmccart/progress_cvs/GEOSadas-5_13_0
source $ESMADIR/src/g5_modules loadmodules

if ( $#argv > 3 || $#argv < 3 ) then
    echo "usage: determine_inst.csh <experiment base directory with diags> <start YYYYMMDD> <end YYYYMMDD>"
    exit 99
endif

set dir=$argv[1]
set startdate=$argv[2]
set enddate=$argv[3]

set curdate=$startdate

set dirs=""

while ( $curdate <= $enddate )
    set year     = `echo $curdate |cut -b1-4`
    set mon      = `echo $curdate |cut -b5-6`
    set day      = `echo $curdate |cut -b7-8`
    if (-d $dir/obs/Y$year/M$mon/D$day) set dirs="$dirs $dir/obs/Y$year/M$mon/D$day"
    set curdate  = `$ESMADIR/Linux/bin/tick $curdate 000000 000000 240000 |cut -b1-8`
end

set init=1
set cinst=""

foreach file (`find $dirs |grep ges`)
    if ($init == 1) then
        set cfile=`basename $file`
        set dat = `echo $cfile | perl -wlne 'print "$1 $2 $3 $4" if  /^(\w+)\.diag_([\w\-]+)_ges\.(\d{8})_(\d{2})z.\w{3}/'`
        set exp        = ${dat[1]}
        set inst       = ${dat[2]}
        set yyyymmdd   = ${dat[3]}
        set hh         = ${dat[4]}
        set yyyymmddhh = $yyyymmdd$hh
        set cinst      = $inst
        set init       = 0
    else
        set cfile=`basename $file`
        set dat = `echo $cfile | perl -wlne 'print "$1 $2 $3 $4" if  /^(\w+)\.diag_([\w\-]+)_ges\.(\d{8})_(\d{2})z.\w{3}/'`
        set exp        = ${dat[1]}
        set cinst       = ${dat[2]}
        set yyyymmdd   = ${dat[3]}
        set hh         = ${dat[4]}
        set yyyymmddhh = $yyyymmdd$hh
        set listcheck = 0
        foreach iinst ( $inst )
            if ($cinst == $iinst) then
                set listcheck = 1 
            endif
        end
        if ($listcheck == 0) then
           set inst = ($cinst $inst)
        endif
   endif
end


echo $inst | sed 's/ /\n/g'



