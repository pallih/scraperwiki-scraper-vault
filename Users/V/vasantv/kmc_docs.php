<?php

# Database of Doctors registered with the Karnataka Medical Council

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

$letters = array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');
//$letters = array ('A');

foreach ($letters as $letter)
{

    $dom = new simple_html_dom();
    $html = scraperWiki::scrape("http://karnatakamedicalcouncil.com/atozlist/KMC_Doctors_list_".$letter.".html");

    $dom->load($html);
    
    foreach($dom->find("table border :1px",0) as $data)
    {
        $tds = $data->find("td");
        $record = array('S.No'=>$tds[0]->plaintext, 'Name' => $tds[1]->find("b")->plaintext,'Address' => $tds[1]->find("br")->innertext);
         print_r($record);
        scraperwiki::save_sqlite(array("S.No","Name","Address"),$record,"KarnatakaDocs");
    }
    
    $dom->__destruct();
}
?>