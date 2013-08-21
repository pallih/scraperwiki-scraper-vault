<?php
require 'scraperwiki/simple_html_dom.php';
$page_counter = 0;
$next_page = FALSE;

do { 
$kovetkezo = "";
$page_counter++;
$pageurl = "http://www.hasznaltauto.hu/talalatilista/auto/QLCSFISWC1TOULJ0Y075QACTHA1LOJ4EAJS6A2MTHYURMD2R7982M3YR6M86L549M8QP1FM6C2D5RUWEK0ZSZSTYCAODPF11Z1MR3IWM8LRLP0HMGPR0K0ZGOWHTLFJOZ4Y4R2173E5JG14AMH25L2GTIPAEHK5YIQUZLA85JHUCH5QS0LM6C5WA5HDI1R9D74PEOA6MM95IAJOQ9PZC5R3HRH93KQY0JJOFZ1CKA5CRGPW46Q0YO1AHYPWQ0HZCZ9U8DGWC0D592R12SKP5ZA0H8HGM23FW7K88AZTKG9LC6JJ51ZA4JECLL0HP3TIZZOCPW24FQLUUSLUERK8265817Q8PZD09Q1RUU/page{$page_counter}";

 
$html_content = scraperWiki::scrape($pageurl);
 

$html = str_get_html($html_content);
foreach ($html->find("div.talalati_lista") as $talalat) {  
    foreach ($talalat->find("h2 a") as $el) {
    $tipus = $el->innertext;
    $url = $el->href;
    $kod = substr($url, -7); 
    }
    foreach ($talalat->find("div.talalati_lista_vetelar strong") as $ar) {
    $ar = str_replace("&nbsp;", " ", $ar->innertext);
    }
    foreach ($talalat->find("p.talalati_lista_infosor") as $info) {

    $info = str_replace("&ndash;", ",", $info->innertext);
    $info = str_replace("&nbsp;", " ", $info);
    $info = str_replace("&sup3;", "3", $info);
    $info = explode(",",$info);
    }

    scraperwiki::save(   
            array('id'),
            array(
                'id' => $kod,
                'type' => $el->innertext,
                'price' => $ar,
                'year' => $info[0],
                'benzin' => $info[1],
                'hub' => $info[2],
                'power' => $info[3],
                'url' => $url,

            )
        );
}
    foreach ($html->find("div.oldalszamozas a[title=Következő]") as $kovetkezo) {
    print $page_counter . "\n";
    }

} while ($kovetkezo != "");
?>
