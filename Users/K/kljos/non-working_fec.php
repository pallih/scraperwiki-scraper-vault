<?php

# Blank PHP
$html = scraperWiki::scrape("http://www.fec.gov/finance/disclosure/ftpsum.shtml");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@align='center'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
'Election Cycle' => $tds[0]->plaintext, 
'File' => intval($tds[1]->plaintext),
'Format Description' => intval($tds[2]->plaintext)
);
    scraperwiki::save(array('Election Cycle'), $record);           
}
?>
