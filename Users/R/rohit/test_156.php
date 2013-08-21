<?php
print "Hello, coding in the cloud!";
$html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm"); 
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("div[@align='left'] tr.tcont")as $data)
{ $tds = $data->find("td"); $record = array( 'country' => $tds[0]->plaintext, 'years_in_school' => intval($tds[4]->plaintext) );
 print_r($record);
 }
scraperwiki::save(array('country'), $record); 


?>
