<?php

// require scraperwiki's HTML parsing script
require 'scraperwiki/simple_html_dom.php';  

// define the URL you want to scrape
$html = scraperWiki::scrape("http://www.ons.gov.uk/ons/release-calendar/index.html?newquery=*&newoffset=&pageSize=100&pagetype=calendar-entry&sortBy=releaseDate&sortDirection=DESCENDING&releaseDateRangeType=next12months&applyFilters=true");                  
$dom = new simple_html_dom();
$dom->load($html);


foreach($dom->find("table[@class='results-listing non-pres'] tr") as $data){

$tds = $data->find("td");



$record = array(

          'name' => $tds[2]->plaintext

  );



    if ( $record['name'] == '' ) {
    $record['name'] = 'No name specified';
  }
 scraperwiki::save_sqlite(array('name'), $record);

}



?>