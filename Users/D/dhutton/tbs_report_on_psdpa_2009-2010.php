<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/rp/09-10/psdpa-pfdar07-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class=\"fontSize70\"] tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-inquiries' => intval($tds[1]->plaintext),
        '3-disclosures' => intval($tds[2]->plaintext),
        '4-referred' => intval($tds[3]->plaintext),
        '5-carried_over' => intval($tds[4]->plaintext),
        '6-acted_upon' => intval($tds[5]->plaintext),
        '7-not_acted_upon' => intval($tds[6]->plaintext),
        '8-carried_over_next' => intval($tds[7]->plaintext),
        '9-investigations' => intval($tds[8]->plaintext),
        '10-investigations' => intval($tds[9]->plaintext),
        '11-corrections' => intval($tds[10]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?><?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/rp/09-10/psdpa-pfdar07-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class=\"fontSize70\"] tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-inquiries' => intval($tds[1]->plaintext),
        '3-disclosures' => intval($tds[2]->plaintext),
        '4-referred' => intval($tds[3]->plaintext),
        '5-carried_over' => intval($tds[4]->plaintext),
        '6-acted_upon' => intval($tds[5]->plaintext),
        '7-not_acted_upon' => intval($tds[6]->plaintext),
        '8-carried_over_next' => intval($tds[7]->plaintext),
        '9-investigations' => intval($tds[8]->plaintext),
        '10-investigations' => intval($tds[9]->plaintext),
        '11-corrections' => intval($tds[10]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>