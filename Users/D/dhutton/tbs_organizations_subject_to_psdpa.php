<?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/pas-srp/report-rapport_e.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("<table border=\"1\" cellspacing=\"0\" cellpadding=\"1\"> tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-code' => intval($tds[1]->plaintext),
        '3-min-affil' => intval($tds[2]->plaintext),
        '4-corp-code' => intval($tds[3]->plaintext),
        '5-soa' => intval($tds[4]->plaintext),
        '6-hr-univ' => intval($tds[5]->plaintext),
        '7-fin-adm' => intval($tds[6]->plaintext),
        '8-' => intval($tds[7]->plaintext),
        '9-' => intval($tds[8]->plaintext),
        '10-' => intval($tds[9]->plaintext),
        '11-' => intval($tds[10]->plaintext),
        '12-PSDPA' => intval($tds[11]->plaintext),
        '13-agent' => intval($tds[12]->plaintext),
        '14-status' => intval($tds[13]->plaintext),
        '15-num-empl' => intval($tds[14]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?><?php
$html = scraperWiki::scrape("http://www.tbs-sct.gc.ca/pas-srp/report-rapport_e.asp");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("<table border=\"1\" cellspacing=\"0\" cellpadding=\"1\"> tr") as $data){
    $tds = $data->find("td");
    $record = array(
        '1-organization' => $tds[0]->plaintext."-XX", 
        '2-code' => intval($tds[1]->plaintext),
        '3-min-affil' => intval($tds[2]->plaintext),
        '4-corp-code' => intval($tds[3]->plaintext),
        '5-soa' => intval($tds[4]->plaintext),
        '6-hr-univ' => intval($tds[5]->plaintext),
        '7-fin-adm' => intval($tds[6]->plaintext),
        '8-' => intval($tds[7]->plaintext),
        '9-' => intval($tds[8]->plaintext),
        '10-' => intval($tds[9]->plaintext),
        '11-' => intval($tds[10]->plaintext),
        '12-PSDPA' => intval($tds[11]->plaintext),
        '13-agent' => intval($tds[12]->plaintext),
        '14-status' => intval($tds[13]->plaintext),
        '15-num-empl' => intval($tds[14]->plaintext)

    );
    print_r($record);
    scraperwiki::save(array('1-organization'), $record);
}

?>