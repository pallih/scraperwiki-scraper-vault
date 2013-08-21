<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/ve/snrs2-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("<table border=\"0\" cellspacing=\"0\" cellpadding=\"3\" width=\"100%\"> tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-details' => utf8_encode($tds[1]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>