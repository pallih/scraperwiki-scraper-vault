<?php

require 'scraperwiki/simple_html_dom.php';

//scraperwiki::attach("craigslist_cities"); //Attach the craigslist city scraper
//print_r(scraperwiki::select("* from craigslist_cities.swdata WHERE state = 'Alabama'"));

scraperwiki::attach('synthfilter_utils');
$manufacturers = scraperwiki::get_var('manufacturers');
$manufacturers = explode(',',$manufacturers); //Convert to array
//

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

$ignored_manufacturers = array();
//Build the scraper name based on the manufacturer array.
print "There are a total of ".count($manufacturers)." manufacturers in the system.\n";
for($i=0;$i<count($manufacturers);$i++){
    $manufacturer = $manufacturers[$i];
    
    if(!in_array($manufacturer,$ignored_manufacturers)){
        $manufacturer = str_replace(",","",$manufacturer);
        $manufacturer = str_replace(".","",$manufacturer);
        $manufacturer = str_replace("(","",$manufacturer);
        $manufacturer = str_replace(")","",$manufacturer);
        $tempName = "california_".strtolower(trim(str_replace(" ","_",$manufacturer)))."_craigslist_synth_scraper";
        if(strlen($tempName) >= 50){
            echo $tempName."\n";
            $dif = (strlen($tempName) - 50);
            $tempName = substr($tempName,0,-$dif);
        }
        //Special cases
        /*switch($manufacturer){
            
            default:
                $tempName = "";
                break;
        }*/
        echo "Loading found synths from: ".$tempName."\n";
        $scrapers[] = $tempName;
    }
}

$foundSynths = array();
$counter = 0;
foreach($scrapers as $scraper){
    //echo "Attaching DB: <a href='https://scraperwiki.com/scrapers/".$scraper."' target='_blank'>".$scraper."</a><br/>";
    try {
        $data = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=$scraper&query=select%20*%20from%20%60swdata%60");
        if(!empty($data)){
            $dataDecoded = json_decode($data);
            //print_r($dataDecoded);
            if(!empty($dataDecoded)){
                //print_r($dataDecoded);
                if(!isset($dataDecoded->error)){

                    //Save the data to a new record
                    $foundSynths = array_merge($dataDecoded,$foundSynths);
                }else{
                    //echo $dataDecoded->error;
                }
            }
        }
    }catch(Exception $e){
        //echo "There is no data for this manufacturer.<br/>";
    }
}

//print_r($foundSynths);
if(!empty($foundSynths)){
    echo "Total Synths Found: ".count($foundSynths)."\n";
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link','post_item_description','post_item_images'), $foundSynths);
    print strval($saveMessage);
}

?>
