<?php
$html = scraperWiki::scrape("http://ugala.ee/index.php/mangukavakalender");
require 'scraperwiki/simple_html_dom.php';

$kava = array();
$piletimaailm = array();

$dom = new simple_html_dom();
$dom->load($html);
/*
$id = 0;
foreach(current($dom->find('table'))->find('tbody tr') as $tr){
    $td = $tr->find("td");
    if (empty($td[0])) continue;

    $rec = array('id' => $id++);
    $c = 0;
    foreach($td as $cell) $rec['col_' . $c++] = $cell->plaintext;
    scraperwiki::save_sqlite(array('id'), $rec, 'raw', 2);
}
*/

$id = 0;
foreach(current($dom->find('table'))->find('tbody tr') as $tr) {
    $td = $tr->find('td');
    if (empty($td[1])) continue; # Using colspan stuff ... :/

    $kava[] = $record = array(
        'id' => $id++,
        'aeg' => preg_replace('/.*(\d\d).(\d\d).(\d\d\d\d)\s*$/', '\3-\2-\1 ', $td[0]->plaintext) . trim($td[1]->plaintext) . ":00",
        'tiitel' => $td[2]->plaintext,
        'asukoht' => $td[3]->plaintext,
        'hind' => floatval(strtr($td[4]->plaintext, ',','.')) * 100,
        'link' => 'http://www.ugala.ee' . current($td[2]->find('a'))->href,
        'valjamuudud'   => 0, # Ugala puhul pole mõeldav :)
        'reserveeritud' => 0, # Ei leidnud ühtegi juhtumit
        'lisainfo' => '',
        'pmaailm' => current($td[5]->find('a'))->href
    );
}
scraperwiki::save_sqlite(array('id'), $kava, 'kava');

