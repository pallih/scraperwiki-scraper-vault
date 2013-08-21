<?php

// require scraperwiki's HTML parsing script
require 'scraperwiki/simple_html_dom.php';  

// define the URL you want to scrape
$html = scraperWiki::scrape("www.bbc.co.uk/news/uk-10629358");                  
$dom = new simple_html_dom();
$dom->load($html);

// select the table and data from that table
foreach($dom->find("table[@class='ba sortable'] tr") as $data){
    $tds = $data->find("td");

// separate the military force from their regiment
    $force = explode("<br />", $tds[4]);

// remove the text "Full story" from the incident entry
    $incidenttext = str_replace("Full story", "", $tds[5]);
    $incident = explode("</span>", $incidenttext);

// separate the location of the incident from the region
    $location = explode("</span>", $tds[6]);

// separate the hometown from the home region
    $birthplace = explode("<br />", $tds[3]);
    
// create the array
    $record = array(
       
        'birthregion' => strip_tags($birthplace[0]),
        'birthcity' => strip_tags($birthplace[1]),

        'force' => strip_tags($force[0]),
        'servedwith' => strip_tags($force[1]),

        'incidenttype' => strip_tags($incident[0]),
        'incidentdetails' => html_entity_decode(strip_tags($incident[1])),

        'location' => strip_tags($location[0]),
        'locationdetail' => strip_tags($location[1]),
        
        'name' => $tds[0]->plaintext,
        'rank' => $tds[1]->plaintext,
        'age' => $tds[2]->plaintext,
        'date' => $tds[7]->plaintext
        
    );

  if ( $record['name'] == '' ) {
    $record['name'] = 'No name specified';
  }

// save array to scraperwiki, based on the 'Name' array, which will be checked every time scraperwiki updates
 scraperwiki::save_sqlite(array('name'), $record);


}

// spare loop
/*
for ($i = 1; $i <= sizeof($record); $i++)
*/

?>