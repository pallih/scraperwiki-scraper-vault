<?php

function htmldecode($uSTR)
{
 return str_replace(array("&auml;", "&Auml;", '&ouml;', '&Ouml;', '&uuml;','&Uuml;', '&szlig;'), array("ä", "Ä",'ö','Ö','ü','Ü','ß'), $uSTR); 
}

function trim_num($t) {
    $x=intval(str_replace('&nbsp;','',$t));
    if ($x=='') $x=0;
    return $x;
}

$html = scraperWiki::scrape("http://inters.bayern.de/luebmw/html/aktmesswerte_lueb.php");


require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom(); 
$dom->load($html); 
$datum=$dom->find('span.luebt2',0);
$datum= date_parse($datum->plaintext);
$datum= $datum['day'].'.'.$datum['month'].'.'.$datum['year'].' '.$datum['hour'].':'.$datum['minute'];
foreach($dom->find("table") as $tds){ 
    $bezirk=$tds->find("font",0);
    if (is_object($bezirk)) {
    $i=4;
    do {     
        $wert=$tds->children($i);
        if (is_object($wert)) {
           ;            
                $record = array( 
                    'id' => $datum.'-'.$wert->children(0)->plaintext,
                    'datum' => $datum,  
                    'bezirk' => $bezirk->plaintext,
                    'ort' => htmldecode($wert->children(0)->plaintext),
                    'ozon8' => trim_num(html_entity_decode($wert->children(1)->plaintext)),
                    'ozon1' => trim_num($wert->children(2)->plaintext),
                    'no2' => trim_num($wert->children(4)->plaintext),
                    'co2' => trim_num($wert->children(5)->plaintext)
                    ); 
                
            
       }
    scraperwiki::save(array('id'), $record);    
    $i++;
    } while (is_object($tds->children($i)));

}

}

?>
