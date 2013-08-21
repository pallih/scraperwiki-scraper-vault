<?php

print "Hello, new data scraper!";

// cth link // $html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");

$html = scraperWiki::scrape("http://www.e-solat.gov.my/prayer_time.php");

print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
   if(count($tds)==12){
     $record = array(
       'year' => $tds[0]->plaintext, 
     'author' => intval($tds[4]->plaintext)
);
 scraperwiki::save(array('isbn'), $record);

   }
}


?>
