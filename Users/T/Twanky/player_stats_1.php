<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.basketball-reference.com/leagues/NBA_2013_totals.html");

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@id='div_totals'] tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==25){
        $record = array(
            'name' => $tds[1]->plaintext,
            'team' => $tds[3]->plaintext,
            'g' => $tds[4]->plaintext,
            'fg' => $tds[7]->plaintext,
            'fga' => $tds[8]->plaintext,
            'three' => $tds[10]->plaintext,
            'ft' => $tds[13]->plaintext,
            'fta' => $tds[14]->plaintext,
            'reb' => $tds[18]->plaintext,
            'ast' => $tds[19]->plaintext,
            'stl' => $tds[20]->plaintext,
            'blk' => $tds[21]->plaintext,
            'to' => $tds[22]->plaintext,
            'pts' => $tds[24]->plaintext
        );
        scraperwiki::save(array('name'), $record); 
    }
}

?>
