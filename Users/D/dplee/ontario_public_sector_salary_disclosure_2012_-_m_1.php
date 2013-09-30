<?php

require 'scraperwiki/simple_html_dom.php';       

$html = scraperWiki::scrape("http://www.fin.gov.on.ca/en/publications/salarydisclosure/pssd/orgs.php?pageNum_pssd=4&organization=ministries");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@summary='Salary Disclosure'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==6){
        $record = array(
            'id' => $tds[1]->plaintext . $tds[2]->plaintext . $tds[4]->plaintext,
            'employer' => $tds[0]->plaintext, 
            'surname' => $tds[1]->plaintext, 
            'givenname' => $tds[2]->plaintext, 
            'position' => $tds[3]->plaintext, 
            'salarypaid' => $tds[4]->plaintext, 
            'taxablebenefits' => $tds[5]->plaintext
        );
        scraperwiki::save(array('id'), $record);
        $html='';
    }
}

?><?php

require 'scraperwiki/simple_html_dom.php';       

$html = scraperWiki::scrape("http://www.fin.gov.on.ca/en/publications/salarydisclosure/pssd/orgs.php?pageNum_pssd=4&organization=ministries");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table[@summary='Salary Disclosure'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==6){
        $record = array(
            'id' => $tds[1]->plaintext . $tds[2]->plaintext . $tds[4]->plaintext,
            'employer' => $tds[0]->plaintext, 
            'surname' => $tds[1]->plaintext, 
            'givenname' => $tds[2]->plaintext, 
            'position' => $tds[3]->plaintext, 
            'salarypaid' => $tds[4]->plaintext, 
            'taxablebenefits' => $tds[5]->plaintext
        );
        scraperwiki::save(array('id'), $record);
        $html='';
    }
}

?>