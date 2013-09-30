<?php
function trim_value(&$value)
{
 $value = trim($value);
}
$html = scraperWiki::scrape("http://www.hnd.bayern.de/tabellen/tabelle_pegel.php?zp=1");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$find = array("td","td align='Right'");
foreach($dom->find("tbody tr, tr") as $data){
    $tds = $data->find("td, td align='Right'");
    if(count($tds)==9){
        $record = array(
            'Ort' => $tds[0]->plaintext, 
            'Wasser' => $tds[1]->plaintext,
            'Pegel' => $tds[3]->plaintext);
    $replace = "";
    $search = array("&nbsp;","---");
    $filter = str_replace ( $search , $replace , $record);
    array_walk($filter, 'trim_value');

scraperwiki::save(array('Ort'), $filter);     }
}

?><?php
function trim_value(&$value)
{
 $value = trim($value);
}
$html = scraperWiki::scrape("http://www.hnd.bayern.de/tabellen/tabelle_pegel.php?zp=1");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$find = array("td","td align='Right'");
foreach($dom->find("tbody tr, tr") as $data){
    $tds = $data->find("td, td align='Right'");
    if(count($tds)==9){
        $record = array(
            'Ort' => $tds[0]->plaintext, 
            'Wasser' => $tds[1]->plaintext,
            'Pegel' => $tds[3]->plaintext);
    $replace = "";
    $search = array("&nbsp;","---");
    $filter = str_replace ( $search , $replace , $record);
    array_walk($filter, 'trim_value');

scraperwiki::save(array('Ort'), $filter);     }
}

?>