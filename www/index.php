<html>
<head>
<title>Radiance Monitoring</title>

 <?php
# This section is the initial setup for the radiance monitoring package.  Upon selecting the radio boxes, the
# page is resubmitted on itself as a posted form, hence most of the logic in the radio boxes.  You'll see 
# plenty of setting of POST variables - these set the defaults if you're visiting the page fresh.  
#
# To add a new instrument:
#
# - as of right now, add something to the platform table below
  ini_set('display_errors', 'On');

  $datadir = 'radmon_data/';
#  $datadir = '../rad_mon_data/';

  $insttable = array(
    "platform" => array(
      array("name" => "msu_tirosn",   "longname" => "MSU TIROS-N",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n06",      "longname" => "MSU NOAA-6",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n07",      "longname" => "MSU NOAA-7",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n08",      "longname" => "MSU NOAA-8",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n09",      "longname" => "MSU NOAA-9",     "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n10",      "longname" => "MSU NOAA-10",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n11",      "longname" => "MSU NOAA-11",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n12",      "longname" => "MSU NOAA-12",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "msu_n14",      "longname" => "MSU NOAA-14",    "nchan" => 4,   "startch" => 2,  "dosubset" => false),
      array("name" => "ssu_tirosn",   "longname" => "SSU TIROS-N",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n06",      "longname" => "SSU NOAA-6",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n07",      "longname" => "SSU NOAA-7",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n08",      "longname" => "SSU NOAA-8",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n09",      "longname" => "SSU NOAA-9",     "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n11",      "longname" => "SSU NOAA-11",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssu_n14",      "longname" => "SSU NOAA-14",    "nchan" => 3,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsua_n15",    "longname" => "AMSU-A NOAA-15", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n16",    "longname" => "AMSU-A NOAA-16", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n17",    "longname" => "AMSU-A NOAA-17", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n18",    "longname" => "AMSU-A NOAA-18", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_n19",    "longname" => "AMSU-A NOAA-19", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_metop-a","longname" => "AMSU-A METOP-A", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_metop-b","longname" => "AMSU-A METOP-B", "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "amsua_aqua",   "longname" => "AMSU-A Aqua",    "nchan" => 15,  "startch" => 6,  "dosubset" => false),
      array("name" => "atms_npp",     "longname" => "ATMS SNPP",      "nchan" => 22,  "startch" => 6,  "dosubset" => false),
      array("name" => "hirs2_tirosn", "longname" => "HIRS2 TIROS-N",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n06",    "longname" => "HIRS2 NOAA-6",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n07",    "longname" => "HIRS2 NOAA-7",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n08",    "longname" => "HIRS2 NOAA-8",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n09",    "longname" => "HIRS2 NOAA-9",   "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n10",    "longname" => "HIRS2 NOAA-10",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n11",    "longname" => "HIRS2 NOAA-11",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n12",    "longname" => "HIRS2 NOAA-12",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs2_n14",    "longname" => "HIRS2 NOAA-14",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n15",    "longname" => "HIRS3 NOAA-15",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n16",    "longname" => "HIRS3 NOAA-16",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs3_n17",    "longname" => "HIRS3 NOAA-17",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_n18",    "longname" => "HIRS4 NOAA-18",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_n19",    "longname" => "HIRS4 NOAA-19",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_metop-a","longname" => "HIRS4 METOP-A",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "hirs4_metop-b","longname" => "HIRS4 METOP-B",  "nchan" => 19,  "startch" => 2,  "dosubset" => false),
      array("name" => "airs_aqua",    "longname" => "AIRS AQUA",      "nchan" => 281, "startch" => 3,  "dosubset" => false),
      array("name" => "iasi_metop-a", "longname" => "IASI METOP-A",   "nchan" => 616, "startch" => 1,  "dosubset" => false),
      array("name" => "iasi_metop-b", "longname" => "IASI METOP-B",   "nchan" => 616, "startch" => 1,  "dosubset" => false),
      array("name" => "cris_npp",     "longname" => "CRIS NPP",       "nchan" => 399, "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f08",     "longname" => "SSMI F08",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f10",     "longname" => "SSMI F10",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f11",     "longname" => "SSMI F11",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f13",     "longname" => "SSMI F13",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f14",     "longname" => "SSMI F14",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmi_f15",     "longname" => "SSMI F15",       "nchan" => 7,   "startch" => 1,  "dosubset" => false),
      array("name" => "ssmis_f16",    "longname" => "SSMIS F16",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f17",    "longname" => "SSMIS F17",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f18",    "longname" => "SSMIS F18",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "ssmis_f19",    "longname" => "SSMIS F19",      "nchan" => 24,  "startch" => 3,  "dosubset" => false),
      array("name" => "amsub_n15",    "longname" => "AMSU-B NOAA-15", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsub_n16",    "longname" => "AMSU-B NOAA-16", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "amsub_n17",    "longname" => "AMSU-B NOAA-17", "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_n18",      "longname" => "MHS NOAA-18",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_n19",      "longname" => "MHS NOAA-19",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_metop-a",  "longname" => "MHS METOP-A",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      array("name" => "mhs_metop-b",  "longname" => "MHS METOP-B",    "nchan" => 5,   "startch" => 1,  "dosubset" => false),
      )
   );

   $imgtype = array(
      array("fn_abbr" => "bkg", "longname" => "Observation Summary"),
      array("fn_abbr" => "anl", "longname" => "Analysis Summary"),
      array("fn_abbr" => "bcor","longname" => "Bias Correction"),
   );

   $explist = glob("$datadir/*",GLOB_ONLYDIR);                                      # Gather experiments
   usort($explist,create_function('$a,$b', 'return filemtime($a) - filemtime($b);'));  # sort by time
   $explist = array_reverse($explist);                                                 # reverse, so newest is first

   $explist = array_map('basename',$explist);

   if (! isset($_POST['exp'])) {
      $_POST['exp'] = $explist[0];

   } else {
      if ($_POST['exp'] <> $_POST['oldexp']) {
         unset($_POST['date']);
         unset($_POST['inst']);
      }
   }
#   if (! isset($_POST['plat'])) $_POST['plat'] = $inst["platform"][0]["name"];
#   if (! isset($_POST['chan'])) $_POST['chan'] = 1;

   if (! isset($_POST['imgtype'])) $_POST['imgtype'] = $imgtype[0]["fn_abbr"];
   $curexp = $_POST['exp'];

   $datelist = glob("$datadir/$curexp/*",GLOB_ONLYDIR);
   $datelist = array_reverse($datelist);                                                 # reverse, so last date is first
   $datelist = array_map('basename',$datelist);

   if (! isset($_POST['date'])) {
      $_POST['date'] = $datelist[0];
   } #else { 
  #   unset($_POST['inst']);
  #   unset($_POST['chan']);
  # }
   $curdate = $_POST['date'];

   $instlist = glob("$datadir/$curexp/$curdate/*",GLOB_ONLYDIR);
   if (! is_array($instlist)) $instlist = array($instlist);
   $instlist = array_map('basename',$instlist);

   if (! isset($_POST['inst'])) $_POST['inst'] = $instlist[0];
   if (! in_array($_POST['inst'],$instlist)) $_POST['inst'] = $instlist[0];
   $curinst = $_POST['inst'];

   foreach ($insttable["platform"] as $curplat) {
      if ($curplat['name'] == $curinst) {
         if (! isset($_POST['chan'])) $_POST['chan'] = $curplat['startch'];
         if ($_POST['chan'] > $curplat['nchan']) $_POST['chan'] = $curplat['startch'];
      }
   }

?>
</head>
<body>

<form action="index.php" method="post">


<table width="940px" >
  <tr>
    <td width="320px" valign="top"> 

     <table cols=2 border=2 cellpadding=6 cellspacing=8>
      <tr>
        <td colspan=2>
          <b>Statistics over Time and FOV</b>
        </td>
      </tr>
      <tr>
        <td colspan=2 >
          <select name="date" style="width:100%"  onchange="this.form.submit();">
          <?php
            foreach ($datelist as $date) {
               if ($curdate == $date) {
                  echo "  <option value={$date} selected>{$date}</option>\n";
               } else {
                  echo "  <option value={$date}>{$date}</option>\n";
               }
            }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan=2>
         <?php
            echo "<input type=hidden name=oldexp value={$curexp}>\n";
         ?>
         <select name="exp" style="width:100%" onchange="this.form.submit();">
          <?php
            foreach ($explist as $exp) {
               if ($curexp == $exp) {
                  echo "  <option value={$exp} selected>{$exp}</option>\n";
               } else {
                  echo "  <option value={$exp}>{$exp}</option>\n";
               }
            }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan=2>
          <select name="inst" style="width:100%"  onchange="this.form.submit();">
          <?php
             $instsel = false;
             foreach ($instlist as $inst) {
                $instmatch = false;
                foreach ($insttable["platform"] as $curplat) {
                   if ($inst == $curplat['name']) {
                      $instmatch = true;
                      if ($curinst == $inst) {
                         echo "  <option value={$curplat['name']} selected>{$curplat['longname']}</option>\n";
                         $nchan    = $curplat['nchan'];
                         $dosubset = $curplat['dosubset'];
                         $instsel = true;
                      } else {
                         echo "  <option value={$curplat['name']}>{$curplat['longname']}</option>\n"; 
                      };
                   };
                };
                if (! $instmatch) echo "<br><br><br>WARNING: $inst not matched in table!!!<br><br><br>\n";
             };
             if (! $instsel) {
                $curinst = $instlist[0];
                foreach ($insttable["platform"] as $curplat) {
                   if ($curinst == $curplat['name']) {
                      $nchan    = $curplat['nchan'];
                      $dosubset = $curplat['dosubset'];
                      $instsel = true;
                   }
                }
             };
          ?> 
          </select> 
        </td>
      </tr>
      <tr>
        <td colspan=2>
          <select name="chan" style="width:100%" onchange="this.form.submit();">
          <?php
             foreach (range(1, $nchan) as $chan) {
                if ($_POST['chan'] == $chan) {
                   echo "  <option value=$chan selected> Ch. $chan </option>\n";
                } else {
                   echo "  <option value=$chan > Ch. $chan </option>\n";
                }
             }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan=2>
          <select name="imgtype" style="width:100%" onchange="this.form.submit();">
          <?php
             foreach ($imgtype as $ctype) {
                if ($_POST['imgtype'] == $ctype["fn_abbr"]) {
                   echo "  <option value={$ctype["fn_abbr"]} selected> {$ctype["longname"]} </option>\n";
                } else {
                   echo "  <option value={$ctype["fn_abbr"]}> {$ctype["longname"]} </option>\n";
                }
             }
          ?>
          </select>
        </td>
      </tr>
      <tr>
        <td colspan=2>
          <center>
            <?php       
              echo "<img src=\"/products/nwp/systems/radmon/wf/{$_POST['inst']}/wf_{$_POST['inst']}_chan{$_POST['chan']}.png\">\n";
            ?>
          </center>
        </td>
      </tr>
     </table>
    </td>
    <td width="20" valign="top">
    </td>
    <td width="600" valign="top">
      <table cols=1 border=2 cellpadding=6 cellspacing=8>
        <tr>
          <td valign="top">
             <center>
             <?php
                $img = "{$datadir}/{$_POST['exp']}/{$_POST['date']}/{$_POST['inst']}/{$_POST['inst']}_{$_POST['imgtype']}_ch{$_POST['chan']}.png";
                echo "<a href=\"$img\">\n";
                echo "<img src=\"$img\">\n" ;
                echo "</a>\n"
             ?>
             </center>
          </td>
        <tr>
      </table>
    </td>
  </tr>
</table>

</body></html>
