<?php

$html = scraperWiki::scrape("http://www.grandtheatre.info/default.asp?Id=324&sC=page46"); 
 
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$i = 1;
foreach($dom->find("div.classeventsWRAP") as $data){
  
        //$title = $data->find("h2");
        print_r($data);

        //$tds = $data->find("td");
        //$record = array(
        //        'id' => $i,
        //        'event' => str_replace("´","'",$tds[0]->plaintext), 
        //        'date' => $tds[1]->plaintext,
        //        'venue' => $tds[2]->plaintext,
        //        'status' => $tds[3]->innertext
        //);
        //scraperwiki::save_sqlite(array('id'), $record);
    $i++;  
}        
?>