<?php
require 'scraperwiki/simple_html_dom.php';
//TABLE of CONTENTS
//
// function find_stat($stats, $cid)               Find a stat in old DB
//
// function copyChurch()                          copy churches from old data into new table and match new column names
// function copyDenom()                           copy denominationsfrom old data into new table and match new column names
// function copyStats()                           copy stats from old data into new table and match new column names
// function copySynod()                           copy old synod into new
// function copyPby()                             copy presbytery from old into new
// function copy_old_stats($newStats)             copy old stats into new stats

// *****************************************************
function find_church_webid($Churches, $web_id)        // Find a church in old DB
    {
    foreach($Churches as $church)
       {
        if($church['old_cid'] == $web_id)
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
        if ( ($Cnt % 100) == 0)
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
function copy_old_stats()        // merge old stats into new stats
{
    $Cnt = scraperwiki::get_var('IndxStat', "0");
    print "Merge CSV Stats START@" . $Cnt . "\n";
    if ($Cnt == 0)
        scraperwiki::sqliteexecute("drop table if exists statold");
    $Churches = scraperwiki::select("church_id, old_cid from churches" );
    $data = scraperWiki::scrape('http://www.kiwanis-ok.org/jdownloads/JimTest/churches_2008.csv');
    $lines = explode("\n", $data);
    print "Merge CSV Stats - data downloaded\n";

    if ($Cnt == 0)
            $Cnt++;// first line is header

    do {
        $new = array();
        $row = $lines[$Cnt];
        $row = str_getcsv($row);        // convert csv row to json row
        $size =  sizeof($row);
        //print_r($row);
        if ($size <= 1)
            {
            print "Empty line #" . $Cnt . "\n";
            $Cnt++;
            continue;
            }
        $old_cid = $row[0];
        //print "Stat:" . $old_cid . "columns:" . $size . "\n";
        $new['old_cid'] = $old_cid;
        $cid = find_church_webid($Churches, $old_cid);
        if ($cid == null)
            {
            print "**Cannot find id for " . $old_cid . "\n";
            $cid = $old_cid;        // workaround so we can look in table
            }

        $new['church_id'] = $cid;

        //print "Merge CSV Stats #" . $Cnt . "/" . $cid ."\n";
        $col = 1;
        for ($yr = 1996; $yr <= 2007; $yr++)
            {
            //print "Yr:" . $yr . " col:" . $col . "\n";
            $new['mbr'.$yr] = $row[$col];
            $col++;
            $new['wor'.$yr] = $row[$col];
            $col++;
            $new['ctb'.$yr] = $row[$col];
            $col++;
            }
        //print_r($new);

        scraperwiki::save_sqlite(array('church_id'), $new, $table_name="statold", $verbose=0);
        $Cnt++;
        if ( ($Cnt % 1000) == 0)
            {
            scraperwiki::save_var('IndxStat', $Cnt );
            print "Merge CSV Stats #" . $Cnt . "/" . sizeof($lines) ."\n";
            }
        } while ($Cnt < sizeof($lines));     // next line (church)
    print "Copy Old CSV Stats DONE #" . $Cnt . "/" . sizeof($lines) ."\n";
    scraperwiki::save_var('IndxStat', 0 );
    }

// *****************************************************
// MAIN
    //copyChurch();
    //copySynod();
    //copyPby();
    //copyDenom();
    //copyStats();

    //scraperwiki::save_var('IndxStat', 0 );    // will erase table
    copy_old_stats();

?>
