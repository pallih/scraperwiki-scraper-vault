<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/rp/08-09/psdpa-pfdar07-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@class=\"fontSize70\"] tr") as $data){
    $ths = $data->find("th");
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $ths[0]->plaintext."-XX", 
        '2-inquiries' => intval($tds[0]->plaintext),
        '3-disclosures' => intval($tds[1]->plaintext),
        '4-referred' => intval($tds[2]->plaintext),
        '5-carried_over' => intval($tds[3]->plaintext),
        '6-acted_upon' => intval($tds[4]->plaintext),
        '7-not_acted_upon' => intval($tds[5]->plaintext),
        '8-investigations' => intval($tds[6]->plaintext),
        '9-wrongdoing' => intval($tds[7]->plaintext),
        '10-corrections' => intval($tds[8]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>
