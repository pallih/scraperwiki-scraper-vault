<?php

$url = 'http://www.bundesbank.de/download/zahlungsverkehr/bankleitzahlen/20120603/blz_20120305.txt';
$data = scraperWiki::scrape($url);
$lines = explode("\n", $data);
$i=0;
// Maximum number of rows to read:
$max = 0;
$header = array();
foreach($lines as $line) {
    if($max>0 and $i>=$max)
        break;
    $row = array(
        'blz'=>substr($line,0,8),
        'merkmal'=>substr($line,8,1),
        'name'=>utf8_encode(trim(substr($line,9,58))),
        'plz'=>substr($line,67,5),
        'ort'=>utf8_encode(trim(substr($line,72,35))),
        'kurzbezeichnung'=>utf8_encode(trim(substr($line,107,27))),
        'pan'=>substr($line,134,5),
        'bic'=>substr($line,139,11),
        'pruefziffernmethode'=>substr($line,150,2),
        'datensatznummer'=>substr($line,152,6),
        'aenderungskennzeichen'=>substr($line,158,1),
        'bankleitzahlloeschung'=>substr($line,159,1)==1 ? true : false,
        'nachfolgebankleitzahl'=>substr($line,160,8)
    );
    if($i==0)
        $header = array_keys($row);
    // Save row
    scraperwiki::save($header, $row); 
    $i++;
}

?>
