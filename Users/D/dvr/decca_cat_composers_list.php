<?php

$html = scraperWiki::scrape("http://www.deccaclassics.com/cat/");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("select[@id='COMP_ID']") as $data){
    foreach($data->find("option") as $tds){
        $record = array(
            'composer' => utf8_encode($tds->plaintext)
        );
        if ($record['composer'] <> 'Composers' AND $record['composer'] <> 'All Composers') {
            scraperwiki::save(array('composer'), $record);
        }
    }
}

?><?php

$html = scraperWiki::scrape("http://www.deccaclassics.com/cat/");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("select[@id='COMP_ID']") as $data){
    foreach($data->find("option") as $tds){
        $record = array(
            'composer' => utf8_encode($tds->plaintext)
        );
        if ($record['composer'] <> 'Composers' AND $record['composer'] <> 'All Composers') {
            scraperwiki::save(array('composer'), $record);
        }
    }
}

?>