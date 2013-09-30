<?php
//require 'scraperwiki/simple_html_dom.php';

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}


//Synth Museum           
$synthList1 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList1)) $synthList1 = json_decode($synthList1);

//VintageSynth
$synthList2 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synthmuseum&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList2)) $synthList2 = json_decode($synthList2);

//Current Synths
$synthList3 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=current_synths&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList3)) $synthList3 = json_decode($synthList3);

$synths = array();
$synths = traverseList($synthList1);
$synths = array_merge(traverseList($synthList2),$synths);
$synths = array_merge(traverseList($synthList3),$synths);

$synths = array_map('unserialize', array_unique(array_map('serialize', $synths)));

echo "Total synths: ".count($synths)."\n";

//var_dump($synths);

if(!empty($synths)){
    //$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url'), $synths);
    //print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($synths));           
    print scraperWiki::get_var('total_results');
}

function traverseList($list){
    $dataList = array();
    foreach($list as $item){
        //Clean up the data
        foreach($item as $key => $value){
            $item->$key = preg_replace("/<*.>/","",$value);
            //echo $item->$key."\n";
        }
        $dataList[] = $item;
    }
    return $dataList;
}

?>
<?php
//require 'scraperwiki/simple_html_dom.php';

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}


//Synth Museum           
$synthList1 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList1)) $synthList1 = json_decode($synthList1);

//VintageSynth
$synthList2 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synthmuseum&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList2)) $synthList2 = json_decode($synthList2);

//Current Synths
$synthList3 = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=current_synths&query=select%20DISTINCT%20manufacturer%2C%20url%2C%20name%20from%20%60swdata%60");
if(!empty($synthList3)) $synthList3 = json_decode($synthList3);

$synths = array();
$synths = traverseList($synthList1);
$synths = array_merge(traverseList($synthList2),$synths);
$synths = array_merge(traverseList($synthList3),$synths);

$synths = array_map('unserialize', array_unique(array_map('serialize', $synths)));

echo "Total synths: ".count($synths)."\n";

//var_dump($synths);

if(!empty($synths)){
    //$dbName = "vintagesynth-scrape-".$today = date("m-d-Y");
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','url'), $synths);
    //print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($synths));           
    print scraperWiki::get_var('total_results');
}

function traverseList($list){
    $dataList = array();
    foreach($list as $item){
        //Clean up the data
        foreach($item as $key => $value){
            $item->$key = preg_replace("/<*.>/","",$value);
            //echo $item->$key."\n";
        }
        $dataList[] = $item;
    }
    return $dataList;
}

?>
