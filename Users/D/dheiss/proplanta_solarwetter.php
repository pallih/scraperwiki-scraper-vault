<?php

require 'scraperwiki/simple_html_dom.php'; 
$html_content = scraperwiki::scrape("http://www.proplanta.de/Solarwetter/profi-wetter.php?SITEID=60123&PLZ=83355"); 
$html = str_get_html($html_content);
$data = $html->find("span.SCHRIFT_FORMULAR_WERTE_MITTE[alt='Aktuelle-Wetter-Werte']");

foreach ($data as $i => $el) { 
    $data[$i] = preg_replace("/,/",".",html_entity_decode( $el->plaintext ));
}

#print_r( $data );

for( $i = 0; $i < 4; $i++ ) {
    $record[$i] = array(
        'datum' => substr( $data[0+$i], 0, 10 ),
        'rel_sonnendauer' => floatval( $data[4+$i] ),
        'globalstrahlung' => floatval( $data[8+$i] ),
        'bedeckung_0' => floatval( $data[16+$i] ),
        'bedeckung_3' => floatval( $data[20+$i] ),
        'bedeckung_6' => floatval( $data[24+$i] ),
        'bedeckung_9' => floatval( $data[28+$i] ),
        'bedeckung_12' => floatval( $data[32+$i] ),
        'bedeckung_15' => floatval( $data[36+$i] ),
        'bedeckung_18' => floatval( $data[40+$i] ),
        'bedeckung_21' => floatval( $data[44+$i] ),
        'sonnenaufgang' => substr( $data[52+$i], 0, 5 ),
        'sonnenuntergang' => substr( $data[56+$i], 0, 5 ),
        'daemmerunganfang' => substr( $data[60+$i], 0, 5 ),
        'daemmerungende' => substr( $data[64+$i], 0, 5 ));
}

#print_r( $record );

scraperwiki::save(array('datum'), $record);
?>
