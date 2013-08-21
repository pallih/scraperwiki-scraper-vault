<?php

require 'scraperwiki/simple_html_dom.php';           

function scrapeTEDDataPage($url, $sector){
  $record = array();
  // print ("a \n");
  if (strcmp($url, "http://ted.europa.eu/")===0) return $record;
  //print ("b \n");
  $time = microtime(true);
  // $html = scraperWiki::scrape($url); 
  $curl = curl_init($url);
  //print ("d \n");
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  //print ("e \n");
  curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
  //print ("f \n");
  curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
  //print ("g \n");
  curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($curl, CURLOPT_TIMEOUT, 10); // 10 second before aborting
  // try CURLOPT_CONNECTTIMEOUT (in seconds)
  // try CURLOPT_LOW_SPEED_LIMIT (to define what slow is, with):
  // curl_setopt($curl, CURLOPT_LOW_SPEED_TIME, 10); (10 second at low speed before aborting
  //print ("h \n");
  $html = curl_exec($curl);
  //print ("i ".curl_error($curl)."\n");
  curl_close($curl);
  //print ("j \n");
  $dom = new simple_html_dom();
  //print ("k \n");
  $dom->load($html);
  print("......done in ".(microtime(true)-$time)."s ".(memory_get_usage()/1000000)."MB\n");

  $tabletrs = $dom->find("table[class=data] tr");

  $record= array('ID' => $url, 'sector' => $sector);
  foreach ($tabletrs as $tabletr){
     $th = $tabletr->find("th");
     $tds = $tabletr->find("td");
     $record[$th[0]->plaintext] = $tds[1]->plaintext;   
     unset ($th); unset($tds); 
  }

  unset($tabletrs); 
  $dom->__destruct();
  unset ($dom); unset ($html);
  scraperwiki::save(array('ID', 'sector'), $record);
  sleep(2);
  return $record;
}

$sourcescraper = 'tedscrapper';

$lasttime =  scraperwiki::get_metadata('lasttime', -1); 

scraperwiki::attach($sourcescraper); 
print("Querying for data\n");
$data = scraperwiki::sqliteexecute(           
    "select distinct time, sector, url from tedscrapper.swdata where time >= '".$lasttime."' order by time"
);

print (count($data->data)." items to process\n");
$count = 0;
foreach($data->data as $ind=>$item){
   $time = $item[0];
   $sector = $item[1];
   $url = $item [2];
   $record = scrapeTEDDataPage($url, $sector);
   print ($count++." ".$record['TI']." ".((memory_get_usage()/1024)/1024)."MB\n"); 
   scraperwiki::save_metadata('lasttime', $time); 
   unset($item); unset($record); unset($time); unset($sector); unset($url);
   unset($data->data[$ind]); unset($ind);
}

?>
