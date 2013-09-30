<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/ve/pda070809-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@id=\"table1\"] tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-inquiries' => intval($tds[1]->plaintext),
        '3-disclosures' => intval($tds[2]->plaintext),
        '4-referred' => intval($tds[3]->plaintext),
        '5-acted_upon' => intval($tds[4]->plaintext),
        '6-not-acted_upon' => intval($tds[5]->plaintext),
        '7-investigations' => intval($tds[6]->plaintext),
        '8-wrongdoing' => intval($tds[7]->plaintext),
        '9-corrections' => intval($tds[8]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>
<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/ve/pda070809-eng.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@id=\"table1\"] tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-inquiries' => intval($tds[1]->plaintext),
        '3-disclosures' => intval($tds[2]->plaintext),
        '4-referred' => intval($tds[3]->plaintext),
        '5-acted_upon' => intval($tds[4]->plaintext),
        '6-not-acted_upon' => intval($tds[5]->plaintext),
        '7-investigations' => intval($tds[6]->plaintext),
        '8-wrongdoing' => intval($tds[7]->plaintext),
        '9-corrections' => intval($tds[8]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>
