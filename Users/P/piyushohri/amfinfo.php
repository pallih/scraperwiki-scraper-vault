<?php

# Blank PHP
$html = scraperWiki::scrape("http://amfiindia.com/nfo.aspx?intId=6216");

#print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table#ctl00_amfiHomeContent_dtvNFO tr") as $data){
    $tds = $data->find("td");
    $record = array(
        'field' => $tds[0]->plaintext, 
        'value' => $tds[1]->plaintext
    );
    #print_r($record);
    scraperwiki::save(array('field'), $record);

}


?>
