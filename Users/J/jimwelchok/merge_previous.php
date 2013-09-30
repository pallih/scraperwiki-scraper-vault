<?php
require 'scraperwiki/simple_html_dom.php';
//TABLE of CONTENTS
// function sum_pby($pby_id)                      Propagate summary of church stats up to single presbytery
// function sum_all_pby()                         Propagate summary of church stats up to presbytery.
// function sum_all_synod()                       Propagate summary of pby stats up to synods
//
// function find_old_church($oldChurch, $cid)     Find a church in old DB
// function find_stat($stats, $cid)               Find a stat in old DB
//
// function copyChurch()                          copy churches from old data into new table and match new column names
// function copyDenom()                           copy denominationsfrom old data into new table and match new column names
// function copyStats()                           copy stats from old data into new table and match new column names
// function copySynod()                           copy old synod into new
// function copyPby()                             copy presbytery from old into new
//
// function merge_church($newChurch, $oldChurch)  merge old church into new
// function merge_stats($newStats)                merge old stats into new stats
// function merge_old_stats()                     merge very old stats into new stats
// function fix_stats()                           change null to zero stats

// *****************************************************
function sum_pby($pby_id)        // Propagate summary of church stats up to single presbytery
{
    global $debug;
    global $xyzzy;

    $mbr = array();
    $wor = array();
    $ctb = array();

    $churchdata = scraperwiki::select("church_id from churches where pby_id=". $pby_id );
   // $statdata   = scraperwiki::select("* from stats" );
    $pbydata    = scraperwiki::select("* from pbys where pby_id=". $pby_id);
    //print "Pby#" . $pby_id . "#ch=" . sizeof($churchdata) . "#pby=" . sizeof($pbydata) . "\n";
    $Cnt  = 0;
    foreach($churchdata as $church)
        {
        $cid = $church['church_id'];
        $statdata= scraperwiki::select("* from stats where church_id=" . $cid );
        //print "CH=" . $cid . "/" . sizeof($churchdata) . " Stats=" . sizeof($statdata) . "\n";
        if (sizeof($statdata) == 0)
            {
            print "CH=" . $cid . "/" . sizeof($churchdata) . " Stats=" . sizeof($statdata) . "\n";
            continue;
            }
        $stats = $statdata[0];
            if($xyzzy)
                {
                $xyzzy = 0;
                //print_r($stats);
                }
        if ($Cnt  == 0)
            {    // get headers from first church
            foreach($stats as $k => $col)
                {
                $k2 = substr($k, 0, 3);
                if ($k2 == "mbr")
                    $mbr[$k] = 0;

                if ($k2 == "wor")
                    $wor[$k] = 0;

                if ($k2 == "ctb")
                    $ctb[$k] = 0;
                }
            }
        // get stats from church
        foreach($stats as $k => $col)
            {
            $k2 = substr($k, 0, 3);
            if ($k2 == "mbr")
                $mbr[$k] += $col;

            if ($k2 == "wor")
                $wor[$k] += $col;

            if ($k2 == "ctb")
                $ctb[$k] += $col;
//if ($k == "mbr1996" && $col > 0)
//print "Mbr1999=" . $col . "\n";
            }
        $Cnt++;
        }
    //print "Sum Pby=" . $pby_id . " churches=" . $Cnt . " mbr=" . sizeof($mbr) . "\n";
    //print_r($mbr);

    // add totals to each pby
    foreach($mbr as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }
    foreach($wor as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }
    foreach($ctb as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }

    $pbydata[0]['churches'] = $Cnt;
    scraperwiki::save_sqlite(array('pby_id'), $pbydata, $table_name="pbys", $verbose=0);
    //print_r($mbr);
}

// *****************************************************
function sum_all_pby()        // Propagate summary of church stats up to presbytery.
{
    global $debug;
    $PBI = scraperwiki::get_var('IndxPby', "0");
    $pbydata = scraperwiki::select("pby_id from pbys");

    print "Start Sum All Presbyteries #" . $PBI . " of " . sizeof($pbydata) . "\n";

    for ( ; $PBI < sizeof($pbydata); $PBI++)
    {
        $pby = $pbydata[$PBI];
        $pby_id = $pby['pby_id'];
        if (($PBI % 10) == 0)
            print "Sum Pby@" . $pby_id . " " . $PBI . " of " . sizeof($pbydata) . "\n";
        sum_pby($pby_id);
    scraperwiki::save_var('IndxPby', $PBI);
    }
    print "Sum Pby " . $PBI . " of " . sizeof($pbydata) . "\n";
    scraperwiki::save_var('IndxPby', 0);  // start over
}

// *****************************************************
function sum_all_synod()        // Propagate summary of pby stats up to synods
{
    print "Summing All Synods\n";

    $Gch_cnt = 0;
    $Gpby_cnt = 0;
    $Gsyn_cnt = 0;

    $Gmbr  = array();
    $Gwor  = array();
    $Gcont = array();

    $synTop = scraperwiki::select("syn_id from synod");
    foreach($synTop as $syn)
    {
        $syn_id = $syn['syn_id'];
        print "Sum Synod:" . $syn_id . "\n";

        $ch_cnt = 0;   // num of churches in synod

        $mbr  = array();
        $wor  = array();
        $cont = array();

        $syndata = scraperwiki::select("* from synod where syn_id=" . $syn_id);
        $pbydata = scraperwiki::select("* from pbys where syn_id=". $syn_id);

        if ($Gsyn_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                $pby = $pbydata[0];
                foreach($pby as $k => $col)
                    {
                    //print "PBY=" . $pby['pby_id'] . "\n";
                    if (substr($k, 0, 3) == "mbr")
                        $Gmbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $Gwor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $Gcont[$k] = 0;
                    }
                }
        $Gsyn_cnt++;

        $pby_cnt = 0;  // num of pbys in synod
        foreach($pbydata as $pby)
            {
            //print "Pby=" . $pby['pby_id']. "\n";
            if ($pby_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $wor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] = 0;
                    }
                }
            else
                {    // total each pby into synod and denom totals
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] += $col;
                    if (substr($k, 0, 3) == "wor")
                       $wor[$k] += $col;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] += $col;
                    }
                }
            $ch_cnt    += $pby['churches'];

            $pby_cnt++;
            }
        $Gch_cnt  += $ch_cnt;
        $Gpby_cnt += $pby_cnt;

        // copy totals to each synod DB, and totalize for denom
        foreach($mbr as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gmbr[$k] += $col;
            }
        foreach($wor as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gwor[$k] += $col;
            }
        foreach($cont as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gcont[$k] += $col;
            }

        $syndata[0]['churches']     = $ch_cnt;
        $syndata[0]['pbys']         = $pby_cnt;
        $syndata[0]['denom_id']     = 1;
        scraperwiki::save_sqlite(array('syn_id'), $syndata, $table_name="synod", $verbose=0);
    }
    $denom= array();
    print "Synods:" . $Gsyn_cnt . " pbys:" . $Gpby_cnt . " churches:" . $Gch_cnt . "\n";
    $denom[0]['name']      = 'pcusa';
    $denom[0]['denom_id']  = '1';
    $denom[0]['churches']  = $Gch_cnt;
    $denom[0]['pbys']      = $Gpby_cnt;
    $denom[0]['synods']    = $Gsyn_cnt;
    print "Mbrs:" . sizeof($Gmbr) . "\n";
    // copy totals to denom
    foreach($Gmbr as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gwor as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gcont as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    //print_r($denom);
    scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
}

// *****************************************************
function find_old_church($oldChurch, $cid)        // Find a church in old DB
    {
    foreach($oldChurch as $old)
       {
        if($old['church_id'] == $cid)
       //print "ID=" . $col['church_id']. " name=" . $col['name']  . "\n";
            return $old;
        }
    }

// *****************************************************
function find_church_webid($Churches, $web_id)        // Find a church in old DB
    {
    foreach($Churches as $church)
       {
        if($church['old_id'] == $web_id)
            return $church['church_id'];
        }
    return null;
    }

// *****************************************************
function find_stat($stats, $cid)        // Find a stat in old DB
    {
    foreach($stats as $church)
       {
        if($church['church_id'] == $cid)
       //print "ID=" . $col['church_id']. " name=" . $col['name']  . "\n";
            return $church;
        }
    }

// *****************************************************
// copy old data to my DB
//http://www.kiwanis-ok.org/jdownloads/JimTest/*.json

// *****************************************************
function copyChurch()        // copy churches from old data into new table and match new column names
{
    print "Copy Churches from OLD\n";
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/church.json');
    $oldChurch= json_decode ( $data, true);
//    $chi = scraperwiki::get_var('IndxChurch', "0");
    $chi = 0;
    $new = array();
    foreach($oldChurch as $old)    // copy olny new values
        {
        foreach($old as $k => $v)
            {
            if ($k == "m2010" ||  $k == "w2010" || $k == "c2010" )    // skip data no longer used.
                continue;
            if ($k == "denom" )
                {
                $k = 'denom_id';
                if ($v = 'pcusa')
                    $new[$chi]['denom_id'] = 1;
                else
                    $new[$chi]['denom_id'] = 0;
                continue;
                }
            else
                {
                $new[$chi][$k] = $v;
                }
            }
        $chi++;
        if ( ($chi % 100) == 0)
            print "Church @" . $chi . "\n";
        //scraperwiki::save_var('IndxChurch', $chi );
        }
    scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);
    print "Church @" . $chi . "\n";
}

// *****************************************************
function copyDenom()        // copy denominationsfrom old data into new table and match new column names
{
    print "Copy Denoms from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists denom");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/denom.json');
    $oldData= json_decode ( $data, true);
    $Cnt = 0;
    $new = array();
    foreach($oldData as $old)
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);

            if ($k == "zero" ||  $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k2 == "m20" ||  $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" || $k2 == "c19" || $k2 == "w19" )
                    continue;    // old names - will regen.

            if ($k == "id" )
                    $k ='denom_id';

            if ($k == "presbyteries" )
                    $k ='pbys';

            $new[$Cnt][$k] = $v;
            }
        $Cnt++;
        }
    scraperwiki::save_sqlite(array('denom_id'), $new, $table_name="denom", $verbose=0);
}

// *****************************************************
function copyStats()        // copy stats from old data into new table and match new column names
    {
    print "Copy Stats from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists stats");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/stats.json');
    $oldData= json_decode ( $data, true);
    $Cnt = 0;
    print "Copy #Stats=" . sizeof($oldData) . "\n";
    foreach($oldData as $old)
        {
        $new = array();
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 1);

            if ( $k != "church_id" )
                {    // fix up old stats abr.
                if ($k2 == "m")
                    $k = "mbr" . substr($k, 1);

                else if ( $k2 == "c")
                    $k = "ctb" . substr($k, 1);

                else if ( $k2 == "w")
                    $k = "wor" . substr($k, 1);
                }

            $new[0][$k] = $v;
            }
        scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);
        unset ($new);
        $Cnt++;
        if ( ($cnt % 100) == 0)
            print " Stat@" . $Cnt . "/" . sizeof($oldData) . " " . intval($Cnt / sizeof($oldData)  * 100) . "%\n";
        }
    }
// *****************************************************
function copySynod()        // copy old synod into new
{
    print "Copy Synods from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists synod");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/synod.json');
    $oldData= json_decode ( $data, true);
    $Cnt= 0;
    $new = array();
    foreach($oldData as $old)    // copy only new values
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);
            if ($k == "zero" ||  $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k2 == "m20" ||  $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" || $k2 == "c19" || $k2 == "w19" )
                continue;// skip data no longer used.
            else
                {
                if($k == "syn_id")
                    $v++;// move from zero base to 1 based (0=>none)
                $new[$Cnt][$k] = $v;
                }
            }
        $new[$Cnt]['denom_id'] = 1;
        //print "Synod\n";
        //if ($Cnt == 1) print_r($new);
        //break;
        $Cnt++;
        print "Synod@" . $Cnt. "\n";
        }
    scraperwiki::save_sqlite(array('syn_id'), $new, $table_name="synod", $verbose=0);
}

// *****************************************************
function copyPby()        // copy presbytery from old into new
{
    print "Copy Pbys from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists pbys");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/pby.json');
    $oldData= json_decode ( $data, true);
    $new = array();
    $Cnt=0;
    foreach($oldData as $old)
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);
            if ($k == "zero" || $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k == "t100" || $k == "t250" || $k == "t500" || $k == "tbig"
             || $k2 == "m20" || $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" ||  $k2 == "c19" || $k2 == "w19"
                )
                continue;// skip data no longer used.
            else
                {
                if ($k == "syn_id")
                    $v++;    // syn_id now 1-x, was 0-x
                $new[$Cnt][$k] = $v;
                }
            }
        $new[$Cnt]['denom_id'] = 1;
        //print "PBY\n";
        //print_r ($new);
        //break;
        $Cnt++;
        }
    scraperwiki::save_sqlite(array('pby_id'), $new, $table_name="pbys", $verbose=0);
    print "Pby@" . $Cnt . "\n";
}

// *****************************************************
function merge_church($newChurch, $oldChurch)        // merge old church into new
{
    $Cnt      = scraperwiki::get_var('IndxChurch', "0");

    do {
        $new = $newChurch[$Cnt];
        $old = find_old_church($oldChurch, $new['church_id']);
        if (sizeof($old) == 0)
            {
            print "Not Found: ID=" . $new['church_id']. " name=" . $new['name']  . "\n";
            $new['founded'] = 2011;
            scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);// add new church
            }
        else
            {
            foreach($old as $k => $v)
                {
                if ($k = 'old_cid' || $k = 'founded' || $k = 'left')
                    $new[$k] = $v;
                else if ($new[$k] != $old[$k])
                    {
                    print $k . " Mismatch @". $new['church_id'] . " New=" . $new[$k]. " Old=" . $new[$k]  . "\n";
                    }
                }
            }
        $Cnt++;
        if (($Cnt % 100) == 0)
            {
            print "Merge Church@" . $Cnt . " ". intval($Cnt / sizeof($newChurch)* 100). "%\n";
            scraperwiki::save_var('IndxChurch', $Cnt );
            }
        } while ($Cnt < sizeof($newChurch));

    print "merge churches=" . $Cnt . "\n";

    $Cnt = 0;
    scraperwiki::save_var('IndxChurch', $Cnt );
}


// *****************************************************
function merge_old_stats()        // merge old stats into new stats
{
    scraperwiki::attach("merge_previous_1", "previous");
    $oldStats  = scraperwiki::select("church_id from previous.statold");
    $Cnt = scraperwiki::get_var('IndxStat', "0");
    $Size = sizeof($oldStats);
    print "Merge OLD Stats START@" . $Cnt . "/" . $Size . "\n";

    for( ; $Cnt < $Size; $Cnt++)
        {
        $cid = $oldStats[$Cnt]['church_id'];
        $oldstat  = scraperwiki::select("* from previous.statold where church_id=" . $cid);

        $new  = scraperwiki::select("* from stats where church_id=" . $cid);

        if ($new== null)
            {
            print "Church Not Found=" . $cid . "\n";
            continue;
            }

        for ($yr = 1996; $yr <= 2007; $yr++)
            {
            $new[0]['mbr' . $yr] = $oldstat[0]['mbr' . $yr];
            $new[0]['wor' . $yr] = $oldstat[0]['wor' . $yr];
            $new[0]['ctb' . $yr] = $oldstat[0]['ctb' . $yr];
            }

        scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);

        if ( ($Cnt % 1000) == 0)
            {
            scraperwiki::save_var('IndxStat', $Cnt );
            print "Merge OLD Stats #" . $Cnt . "/" . $Size ."\n";
            }
        }

    print "Merge Old Stats DONE #" . $Cnt . "/" . $Size ."\n";
    scraperwiki::save_var('IndxStat', 0 );
    }

// *****************************************************
function merge_stats($newStats)        // merge latest stats into new stats
{
    $Cnt = scraperwiki::get_var('IndxChurch', "0");
    $dirty = 0;
    //$Cnt = 5237;    // test
    print "Merge Stats cnt=" . $Cnt . "/" . sizeof($newStats) . "\n";
    $update = 0;
    $same = 0;
    $newval = 0;
    $notfound = 0;
    $churchCnt = 0;

    do {
        $new = $newStats[$Cnt];
        $oldData = scraperwiki::select("* from pcusa.stats where church_id='" . $new['church_id'] . "'");
        if (sizeof($oldData) == 0)
            {
            $notfound++;
            print "Not Found: ID=" . $new['church_id'] . "\n";
            }
        else
            {
            $old = $oldData[0];
            foreach($old as $k => $v)
                {    // only check stats
                $k2 = substr($k, 0 , 3);
                if ($k2 == "wor" || $k2 == "ctb" || $k2 == "mbr")
                    {
                    //print "k=\"" . $k . "\" v=\"" . $v . "\"\n";

                    if (array_key_exists ( $k , $new) )
                        {
                        if (intval($new[$k]) !== intval($old[$k]) )
                            {
                            if (isset($old[$k]) ) // && (substr($k, 3, 4) == "2011") )
                                {
                                $update++;
                                $dirty = 1;
                                //print "Mismatch #" . $Cnt . " @". $new['church_id'] . " key=" . $k . " New=\"" . $new[$k]. "\" Old=\"" . $old[$k]  . "\"\n";
                                $new[$k] = $v;
                                }
                            }
                        else      // value same
                            {
                            $same++;
                            //print $k . " Same@". $new['church_id'] . " New=" . $new[$k]. " Old=" . $old[$k]  . "\n";
                            }
                        }
                    else if (isset($v) && $v > 0)
                        {
                        $dirty = 1;

                        $newval++;
                        $new[$k] = $v;
                        //print "New Value " . $k . "=" . $v ."\n";
                        }
                    }
                }
            if($dirty)
                {
                $churchCnt++;
                scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);
                $dirty = 0;
                }
            }
        $Cnt++;
        $done = $Cnt / sizeof($newStats) * 100;
        if ( ($Cnt % 1000) == 0)
            {
            print "merge stats=" . $Cnt . " Up=" . $update . " ok=" . $same . " new=" . $newval . " notfound=" . $notfound . " " . intval($done) . "%\n";
            scraperwiki::save_var('IndxChurch', $Cnt );
            }
        } while ($Cnt < sizeof($newStats));

    print "merge stats=" . $Cnt . " Stats_Modified=" . $churchCnt . " Up=" . $update . " ok=" . $same. " new=" . $newval . " notfound=" . $notfound . "\n";

    $Cnt = 0;
    scraperwiki::save_var('IndxChurch', $Cnt );
}

// *****************************************************
function fix_stats()        // change null to zero stats
{
    $stats = scraperwiki::select("* from stats");
    $Cnt = 0;
    $Bad = 0;
    print "Fixing Stats " . sizeof($stats) . "\n";

    foreach($stats as $stat)
        {
        $dirty = 0;
        foreach($stat as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $stat[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        $dirty = 0;
        if ( ($Cnt % 1000) == 0)
            print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
function fix_denom()        // change null to zero stats
{
    $denoms = scraperwiki::select("* from denom");
    $Cnt = 0;
    $Bad = 0;
 
    print "Fixing denom " . sizeof($denoms) . "\n";

    foreach($denoms as $denom)
        {
        $dirty = 0;
        foreach($denom as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $denom[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
        $dirty = 0;
        print " denom #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print "DONE denom #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
// MAIN
    $xyzzy = 1;
    $copy = 0;
    if ($copy)
        {
        copyChurch();
        copySynod();
        copyPby();
        copyDenom();
        copyStats();
        }

    $merge= 0;
    if ($merge)
        {
         //scraperwiki::save_var('IndxChurch', 0);// start over

        scraperwiki::attach("pcusa_church_data", "pcusa");
        $newChurch = scraperwiki::select("* from pcusa.churches");
        $oldChurch = scraperwiki::select("* from churches");
        merge_church($newChurch, $oldChurch);
        }

    $doStats= 0;
    if ($doStats)
        {
        scraperwiki::save_var('IndxStat', 0);// start over
        merge_old_stats();
        }

    //scraperwiki::save_var('IndxChurch', 0 );
    //merge_stats();

    //fix_stats();
    //fix_denom();

    $sum = 1;
    if ($sum)
        {
        //scraperwiki::save_var('IndxPby', 0);  // start over
        sum_all_pby();
        sum_all_synod();
        }

//TEST CASES
        //sum_pby(150146);
        //sum_all_pby();

?>
<?php
require 'scraperwiki/simple_html_dom.php';
//TABLE of CONTENTS
// function sum_pby($pby_id)                      Propagate summary of church stats up to single presbytery
// function sum_all_pby()                         Propagate summary of church stats up to presbytery.
// function sum_all_synod()                       Propagate summary of pby stats up to synods
//
// function find_old_church($oldChurch, $cid)     Find a church in old DB
// function find_stat($stats, $cid)               Find a stat in old DB
//
// function copyChurch()                          copy churches from old data into new table and match new column names
// function copyDenom()                           copy denominationsfrom old data into new table and match new column names
// function copyStats()                           copy stats from old data into new table and match new column names
// function copySynod()                           copy old synod into new
// function copyPby()                             copy presbytery from old into new
//
// function merge_church($newChurch, $oldChurch)  merge old church into new
// function merge_stats($newStats)                merge old stats into new stats
// function merge_old_stats()                     merge very old stats into new stats
// function fix_stats()                           change null to zero stats

// *****************************************************
function sum_pby($pby_id)        // Propagate summary of church stats up to single presbytery
{
    global $debug;
    global $xyzzy;

    $mbr = array();
    $wor = array();
    $ctb = array();

    $churchdata = scraperwiki::select("church_id from churches where pby_id=". $pby_id );
   // $statdata   = scraperwiki::select("* from stats" );
    $pbydata    = scraperwiki::select("* from pbys where pby_id=". $pby_id);
    //print "Pby#" . $pby_id . "#ch=" . sizeof($churchdata) . "#pby=" . sizeof($pbydata) . "\n";
    $Cnt  = 0;
    foreach($churchdata as $church)
        {
        $cid = $church['church_id'];
        $statdata= scraperwiki::select("* from stats where church_id=" . $cid );
        //print "CH=" . $cid . "/" . sizeof($churchdata) . " Stats=" . sizeof($statdata) . "\n";
        if (sizeof($statdata) == 0)
            {
            print "CH=" . $cid . "/" . sizeof($churchdata) . " Stats=" . sizeof($statdata) . "\n";
            continue;
            }
        $stats = $statdata[0];
            if($xyzzy)
                {
                $xyzzy = 0;
                //print_r($stats);
                }
        if ($Cnt  == 0)
            {    // get headers from first church
            foreach($stats as $k => $col)
                {
                $k2 = substr($k, 0, 3);
                if ($k2 == "mbr")
                    $mbr[$k] = 0;

                if ($k2 == "wor")
                    $wor[$k] = 0;

                if ($k2 == "ctb")
                    $ctb[$k] = 0;
                }
            }
        // get stats from church
        foreach($stats as $k => $col)
            {
            $k2 = substr($k, 0, 3);
            if ($k2 == "mbr")
                $mbr[$k] += $col;

            if ($k2 == "wor")
                $wor[$k] += $col;

            if ($k2 == "ctb")
                $ctb[$k] += $col;
//if ($k == "mbr1996" && $col > 0)
//print "Mbr1999=" . $col . "\n";
            }
        $Cnt++;
        }
    //print "Sum Pby=" . $pby_id . " churches=" . $Cnt . " mbr=" . sizeof($mbr) . "\n";
    //print_r($mbr);

    // add totals to each pby
    foreach($mbr as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }
    foreach($wor as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }
    foreach($ctb as $k => $col)
        {
        $pbydata[0][$k] = $col;
        }

    $pbydata[0]['churches'] = $Cnt;
    scraperwiki::save_sqlite(array('pby_id'), $pbydata, $table_name="pbys", $verbose=0);
    //print_r($mbr);
}

// *****************************************************
function sum_all_pby()        // Propagate summary of church stats up to presbytery.
{
    global $debug;
    $PBI = scraperwiki::get_var('IndxPby', "0");
    $pbydata = scraperwiki::select("pby_id from pbys");

    print "Start Sum All Presbyteries #" . $PBI . " of " . sizeof($pbydata) . "\n";

    for ( ; $PBI < sizeof($pbydata); $PBI++)
    {
        $pby = $pbydata[$PBI];
        $pby_id = $pby['pby_id'];
        if (($PBI % 10) == 0)
            print "Sum Pby@" . $pby_id . " " . $PBI . " of " . sizeof($pbydata) . "\n";
        sum_pby($pby_id);
    scraperwiki::save_var('IndxPby', $PBI);
    }
    print "Sum Pby " . $PBI . " of " . sizeof($pbydata) . "\n";
    scraperwiki::save_var('IndxPby', 0);  // start over
}

// *****************************************************
function sum_all_synod()        // Propagate summary of pby stats up to synods
{
    print "Summing All Synods\n";

    $Gch_cnt = 0;
    $Gpby_cnt = 0;
    $Gsyn_cnt = 0;

    $Gmbr  = array();
    $Gwor  = array();
    $Gcont = array();

    $synTop = scraperwiki::select("syn_id from synod");
    foreach($synTop as $syn)
    {
        $syn_id = $syn['syn_id'];
        print "Sum Synod:" . $syn_id . "\n";

        $ch_cnt = 0;   // num of churches in synod

        $mbr  = array();
        $wor  = array();
        $cont = array();

        $syndata = scraperwiki::select("* from synod where syn_id=" . $syn_id);
        $pbydata = scraperwiki::select("* from pbys where syn_id=". $syn_id);

        if ($Gsyn_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                $pby = $pbydata[0];
                foreach($pby as $k => $col)
                    {
                    //print "PBY=" . $pby['pby_id'] . "\n";
                    if (substr($k, 0, 3) == "mbr")
                        $Gmbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $Gwor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $Gcont[$k] = 0;
                    }
                }
        $Gsyn_cnt++;

        $pby_cnt = 0;  // num of pbys in synod
        foreach($pbydata as $pby)
            {
            //print "Pby=" . $pby['pby_id']. "\n";
            if ($pby_cnt == 0)
                {    // init totals to zero, and gather names (changes once a year)
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] = 0;
                    if (substr($k, 0, 3) == "wor")
                        $wor[$k] = 0;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] = 0;
                    }
                }
            else
                {    // total each pby into synod and denom totals
                foreach($pby as $k => $col)
                    {
                    if (substr($k, 0, 3) == "mbr")
                        $mbr[$k] += $col;
                    if (substr($k, 0, 3) == "wor")
                       $wor[$k] += $col;
                    if (substr($k, 0, 3) == "ctb")
                        $cont[$k] += $col;
                    }
                }
            $ch_cnt    += $pby['churches'];

            $pby_cnt++;
            }
        $Gch_cnt  += $ch_cnt;
        $Gpby_cnt += $pby_cnt;

        // copy totals to each synod DB, and totalize for denom
        foreach($mbr as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gmbr[$k] += $col;
            }
        foreach($wor as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gwor[$k] += $col;
            }
        foreach($cont as $k => $col)
            {
            $syndata[0][$k] = $col;
            $Gcont[$k] += $col;
            }

        $syndata[0]['churches']     = $ch_cnt;
        $syndata[0]['pbys']         = $pby_cnt;
        $syndata[0]['denom_id']     = 1;
        scraperwiki::save_sqlite(array('syn_id'), $syndata, $table_name="synod", $verbose=0);
    }
    $denom= array();
    print "Synods:" . $Gsyn_cnt . " pbys:" . $Gpby_cnt . " churches:" . $Gch_cnt . "\n";
    $denom[0]['name']      = 'pcusa';
    $denom[0]['denom_id']  = '1';
    $denom[0]['churches']  = $Gch_cnt;
    $denom[0]['pbys']      = $Gpby_cnt;
    $denom[0]['synods']    = $Gsyn_cnt;
    print "Mbrs:" . sizeof($Gmbr) . "\n";
    // copy totals to denom
    foreach($Gmbr as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gwor as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    foreach($Gcont as $k => $col)
        {
        $denom[0][$k] = $col;
        }
    //print_r($denom);
    scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
}

// *****************************************************
function find_old_church($oldChurch, $cid)        // Find a church in old DB
    {
    foreach($oldChurch as $old)
       {
        if($old['church_id'] == $cid)
       //print "ID=" . $col['church_id']. " name=" . $col['name']  . "\n";
            return $old;
        }
    }

// *****************************************************
function find_church_webid($Churches, $web_id)        // Find a church in old DB
    {
    foreach($Churches as $church)
       {
        if($church['old_id'] == $web_id)
            return $church['church_id'];
        }
    return null;
    }

// *****************************************************
function find_stat($stats, $cid)        // Find a stat in old DB
    {
    foreach($stats as $church)
       {
        if($church['church_id'] == $cid)
       //print "ID=" . $col['church_id']. " name=" . $col['name']  . "\n";
            return $church;
        }
    }

// *****************************************************
// copy old data to my DB
//http://www.kiwanis-ok.org/jdownloads/JimTest/*.json

// *****************************************************
function copyChurch()        // copy churches from old data into new table and match new column names
{
    print "Copy Churches from OLD\n";
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/church.json');
    $oldChurch= json_decode ( $data, true);
//    $chi = scraperwiki::get_var('IndxChurch', "0");
    $chi = 0;
    $new = array();
    foreach($oldChurch as $old)    // copy olny new values
        {
        foreach($old as $k => $v)
            {
            if ($k == "m2010" ||  $k == "w2010" || $k == "c2010" )    // skip data no longer used.
                continue;
            if ($k == "denom" )
                {
                $k = 'denom_id';
                if ($v = 'pcusa')
                    $new[$chi]['denom_id'] = 1;
                else
                    $new[$chi]['denom_id'] = 0;
                continue;
                }
            else
                {
                $new[$chi][$k] = $v;
                }
            }
        $chi++;
        if ( ($chi % 100) == 0)
            print "Church @" . $chi . "\n";
        //scraperwiki::save_var('IndxChurch', $chi );
        }
    scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);
    print "Church @" . $chi . "\n";
}

// *****************************************************
function copyDenom()        // copy denominationsfrom old data into new table and match new column names
{
    print "Copy Denoms from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists denom");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/denom.json');
    $oldData= json_decode ( $data, true);
    $Cnt = 0;
    $new = array();
    foreach($oldData as $old)
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);

            if ($k == "zero" ||  $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k2 == "m20" ||  $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" || $k2 == "c19" || $k2 == "w19" )
                    continue;    // old names - will regen.

            if ($k == "id" )
                    $k ='denom_id';

            if ($k == "presbyteries" )
                    $k ='pbys';

            $new[$Cnt][$k] = $v;
            }
        $Cnt++;
        }
    scraperwiki::save_sqlite(array('denom_id'), $new, $table_name="denom", $verbose=0);
}

// *****************************************************
function copyStats()        // copy stats from old data into new table and match new column names
    {
    print "Copy Stats from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists stats");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/stats.json');
    $oldData= json_decode ( $data, true);
    $Cnt = 0;
    print "Copy #Stats=" . sizeof($oldData) . "\n";
    foreach($oldData as $old)
        {
        $new = array();
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 1);

            if ( $k != "church_id" )
                {    // fix up old stats abr.
                if ($k2 == "m")
                    $k = "mbr" . substr($k, 1);

                else if ( $k2 == "c")
                    $k = "ctb" . substr($k, 1);

                else if ( $k2 == "w")
                    $k = "wor" . substr($k, 1);
                }

            $new[0][$k] = $v;
            }
        scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);
        unset ($new);
        $Cnt++;
        if ( ($cnt % 100) == 0)
            print " Stat@" . $Cnt . "/" . sizeof($oldData) . " " . intval($Cnt / sizeof($oldData)  * 100) . "%\n";
        }
    }
// *****************************************************
function copySynod()        // copy old synod into new
{
    print "Copy Synods from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists synod");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/synod.json');
    $oldData= json_decode ( $data, true);
    $Cnt= 0;
    $new = array();
    foreach($oldData as $old)    // copy only new values
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);
            if ($k == "zero" ||  $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k2 == "m20" ||  $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" || $k2 == "c19" || $k2 == "w19" )
                continue;// skip data no longer used.
            else
                {
                if($k == "syn_id")
                    $v++;// move from zero base to 1 based (0=>none)
                $new[$Cnt][$k] = $v;
                }
            }
        $new[$Cnt]['denom_id'] = 1;
        //print "Synod\n";
        //if ($Cnt == 1) print_r($new);
        //break;
        $Cnt++;
        print "Synod@" . $Cnt. "\n";
        }
    scraperwiki::save_sqlite(array('syn_id'), $new, $table_name="synod", $verbose=0);
}

// *****************************************************
function copyPby()        // copy presbytery from old into new
{
    print "Copy Pbys from OLD\n";
    scraperwiki::sqliteexecute("drop table if exists pbys");
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/pby.json');
    $oldData= json_decode ( $data, true);
    $new = array();
    $Cnt=0;
    foreach($oldData as $old)
        {
        foreach($old as $k => $v)
            {
            $k2 = substr($k, 0, 3);
            if ($k == "zero" || $k == "m100" || $k == "m250" || $k == "m500" || $k == "mbig"
             || $k == "t100" || $k == "t250" || $k == "t500" || $k == "tbig"
             || $k2 == "m20" || $k2 == "c20" || $k2 == "w20"  || $k2 == "m19" ||  $k2 == "c19" || $k2 == "w19"
                )
                continue;// skip data no longer used.
            else
                {
                if ($k == "syn_id")
                    $v++;    // syn_id now 1-x, was 0-x
                $new[$Cnt][$k] = $v;
                }
            }
        $new[$Cnt]['denom_id'] = 1;
        //print "PBY\n";
        //print_r ($new);
        //break;
        $Cnt++;
        }
    scraperwiki::save_sqlite(array('pby_id'), $new, $table_name="pbys", $verbose=0);
    print "Pby@" . $Cnt . "\n";
}

// *****************************************************
function merge_church($newChurch, $oldChurch)        // merge old church into new
{
    $Cnt      = scraperwiki::get_var('IndxChurch', "0");

    do {
        $new = $newChurch[$Cnt];
        $old = find_old_church($oldChurch, $new['church_id']);
        if (sizeof($old) == 0)
            {
            print "Not Found: ID=" . $new['church_id']. " name=" . $new['name']  . "\n";
            $new['founded'] = 2011;
            scraperwiki::save_sqlite(array('church_id'), $new, $table_name="churches", $verbose=0);// add new church
            }
        else
            {
            foreach($old as $k => $v)
                {
                if ($k = 'old_cid' || $k = 'founded' || $k = 'left')
                    $new[$k] = $v;
                else if ($new[$k] != $old[$k])
                    {
                    print $k . " Mismatch @". $new['church_id'] . " New=" . $new[$k]. " Old=" . $new[$k]  . "\n";
                    }
                }
            }
        $Cnt++;
        if (($Cnt % 100) == 0)
            {
            print "Merge Church@" . $Cnt . " ". intval($Cnt / sizeof($newChurch)* 100). "%\n";
            scraperwiki::save_var('IndxChurch', $Cnt );
            }
        } while ($Cnt < sizeof($newChurch));

    print "merge churches=" . $Cnt . "\n";

    $Cnt = 0;
    scraperwiki::save_var('IndxChurch', $Cnt );
}


// *****************************************************
function merge_old_stats()        // merge old stats into new stats
{
    scraperwiki::attach("merge_previous_1", "previous");
    $oldStats  = scraperwiki::select("church_id from previous.statold");
    $Cnt = scraperwiki::get_var('IndxStat', "0");
    $Size = sizeof($oldStats);
    print "Merge OLD Stats START@" . $Cnt . "/" . $Size . "\n";

    for( ; $Cnt < $Size; $Cnt++)
        {
        $cid = $oldStats[$Cnt]['church_id'];
        $oldstat  = scraperwiki::select("* from previous.statold where church_id=" . $cid);

        $new  = scraperwiki::select("* from stats where church_id=" . $cid);

        if ($new== null)
            {
            print "Church Not Found=" . $cid . "\n";
            continue;
            }

        for ($yr = 1996; $yr <= 2007; $yr++)
            {
            $new[0]['mbr' . $yr] = $oldstat[0]['mbr' . $yr];
            $new[0]['wor' . $yr] = $oldstat[0]['wor' . $yr];
            $new[0]['ctb' . $yr] = $oldstat[0]['ctb' . $yr];
            }

        scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);

        if ( ($Cnt % 1000) == 0)
            {
            scraperwiki::save_var('IndxStat', $Cnt );
            print "Merge OLD Stats #" . $Cnt . "/" . $Size ."\n";
            }
        }

    print "Merge Old Stats DONE #" . $Cnt . "/" . $Size ."\n";
    scraperwiki::save_var('IndxStat', 0 );
    }

// *****************************************************
function merge_stats($newStats)        // merge latest stats into new stats
{
    $Cnt = scraperwiki::get_var('IndxChurch', "0");
    $dirty = 0;
    //$Cnt = 5237;    // test
    print "Merge Stats cnt=" . $Cnt . "/" . sizeof($newStats) . "\n";
    $update = 0;
    $same = 0;
    $newval = 0;
    $notfound = 0;
    $churchCnt = 0;

    do {
        $new = $newStats[$Cnt];
        $oldData = scraperwiki::select("* from pcusa.stats where church_id='" . $new['church_id'] . "'");
        if (sizeof($oldData) == 0)
            {
            $notfound++;
            print "Not Found: ID=" . $new['church_id'] . "\n";
            }
        else
            {
            $old = $oldData[0];
            foreach($old as $k => $v)
                {    // only check stats
                $k2 = substr($k, 0 , 3);
                if ($k2 == "wor" || $k2 == "ctb" || $k2 == "mbr")
                    {
                    //print "k=\"" . $k . "\" v=\"" . $v . "\"\n";

                    if (array_key_exists ( $k , $new) )
                        {
                        if (intval($new[$k]) !== intval($old[$k]) )
                            {
                            if (isset($old[$k]) ) // && (substr($k, 3, 4) == "2011") )
                                {
                                $update++;
                                $dirty = 1;
                                //print "Mismatch #" . $Cnt . " @". $new['church_id'] . " key=" . $k . " New=\"" . $new[$k]. "\" Old=\"" . $old[$k]  . "\"\n";
                                $new[$k] = $v;
                                }
                            }
                        else      // value same
                            {
                            $same++;
                            //print $k . " Same@". $new['church_id'] . " New=" . $new[$k]. " Old=" . $old[$k]  . "\n";
                            }
                        }
                    else if (isset($v) && $v > 0)
                        {
                        $dirty = 1;

                        $newval++;
                        $new[$k] = $v;
                        //print "New Value " . $k . "=" . $v ."\n";
                        }
                    }
                }
            if($dirty)
                {
                $churchCnt++;
                scraperwiki::save_sqlite(array('church_id'), $new, $table_name="stats", $verbose=0);
                $dirty = 0;
                }
            }
        $Cnt++;
        $done = $Cnt / sizeof($newStats) * 100;
        if ( ($Cnt % 1000) == 0)
            {
            print "merge stats=" . $Cnt . " Up=" . $update . " ok=" . $same . " new=" . $newval . " notfound=" . $notfound . " " . intval($done) . "%\n";
            scraperwiki::save_var('IndxChurch', $Cnt );
            }
        } while ($Cnt < sizeof($newStats));

    print "merge stats=" . $Cnt . " Stats_Modified=" . $churchCnt . " Up=" . $update . " ok=" . $same. " new=" . $newval . " notfound=" . $notfound . "\n";

    $Cnt = 0;
    scraperwiki::save_var('IndxChurch', $Cnt );
}

// *****************************************************
function fix_stats()        // change null to zero stats
{
    $stats = scraperwiki::select("* from stats");
    $Cnt = 0;
    $Bad = 0;
    print "Fixing Stats " . sizeof($stats) . "\n";

    foreach($stats as $stat)
        {
        $dirty = 0;
        foreach($stat as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $stat[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('church_id'), $stat, $table_name="stats", $verbose=0);
        $dirty = 0;
        if ( ($Cnt % 1000) == 0)
            print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print " Stats #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
function fix_denom()        // change null to zero stats
{
    $denoms = scraperwiki::select("* from denom");
    $Cnt = 0;
    $Bad = 0;
 
    print "Fixing denom " . sizeof($denoms) . "\n";

    foreach($denoms as $denom)
        {
        $dirty = 0;
        foreach($denom as $k => $v)
            {
            if (!isset($v))
                {
                $Bad++;
                $dirty = 1;
                //print "Bad k=" . $k . "\n";
                $denom[$k] = 0;
                }
            }
        if($dirty)
            scraperwiki::save_sqlite(array('denom_id'), $denom, $table_name="denom", $verbose=0);
        $dirty = 0;
        print " denom #" . $Cnt . " Bad=" . $Bad . "\n";
        $Cnt++;
        }
    print "DONE denom #" . $Cnt . " Bad=" . $Bad . "\n";
}

// *****************************************************
// MAIN
    $xyzzy = 1;
    $copy = 0;
    if ($copy)
        {
        copyChurch();
        copySynod();
        copyPby();
        copyDenom();
        copyStats();
        }

    $merge= 0;
    if ($merge)
        {
         //scraperwiki::save_var('IndxChurch', 0);// start over

        scraperwiki::attach("pcusa_church_data", "pcusa");
        $newChurch = scraperwiki::select("* from pcusa.churches");
        $oldChurch = scraperwiki::select("* from churches");
        merge_church($newChurch, $oldChurch);
        }

    $doStats= 0;
    if ($doStats)
        {
        scraperwiki::save_var('IndxStat', 0);// start over
        merge_old_stats();
        }

    //scraperwiki::save_var('IndxChurch', 0 );
    //merge_stats();

    //fix_stats();
    //fix_denom();

    $sum = 1;
    if ($sum)
        {
        //scraperwiki::save_var('IndxPby', 0);  // start over
        sum_all_pby();
        sum_all_synod();
        }

//TEST CASES
        //sum_pby(150146);
        //sum_all_pby();

?>
