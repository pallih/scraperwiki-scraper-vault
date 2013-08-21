<?php

$html = scraperWiki::scrape("http://www.hud.gov/local/ny/homeless/familiesshelters.cfm"); 
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("td#content-area p") as $data){
    $rows = explode("<br>",$data);
#    print_r($rows);
#    print count($rows);
    $record = array(
        'shelter' => $rows[0],
        'address' => $rows[1],
        'city' => $rows[2],
        'phone' => $rows[3]

    ); 
    print_r($record); 
    scraperwiki::save(array('shelter'), $record); 
}

?>
