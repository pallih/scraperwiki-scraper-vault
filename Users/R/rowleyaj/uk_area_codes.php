<?php

$html = scraperWiki::scrape("http://consumers.ofcom.org.uk/2009/09/telephone-area-codes-tool/");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table#allCodes tr") as $data){
    $ths = $data->find("th");
    $tds = $data->find("td");
    $record = array(
        'code' => $ths[0]->plaintext, 
        'area' => $tds[0]->plaintext);

    scraperwiki::save(array('code'), $record);
}

?>
