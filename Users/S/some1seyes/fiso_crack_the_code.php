<?php

$html = scraperWiki::scrape("http://crackthecode.fiso.co.uk/CTC.XML");
//print $html . "\n"; 


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("PLAYER") as $data){ 
    $name = $data->find("NAME"); 
    $percent = $data->find("NTI_PERCENT");
    $ntitoday = $data->find("NTITODAY");
    $record = array( 
        'Name' => $name[0]->plaintext, 
        'NTI Today' => $ntitoday[0]->plaintext, 
        'Percent' => $percent[0]->plaintext, 
    ); 
    //print_r($record) . "\n";
    scraperwiki::save(array('Name'), $record);
}

?>
