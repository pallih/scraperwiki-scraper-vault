<?php
$html = scraperWiki::scrape("http://www.linnateater.ee/et/mangukava/");
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
$kava = array();
$id = 0;
foreach($dom->find('#kava tr') as $tr) {
    $td = $tr->find('td');
    if (empty($td[1])) continue; # Using colspan stuff ... :/

    $record = array(
          'id' => $id++
        , 'aeg' => preg_replace('/.*(\d\d).(\d\d).(\d\d\d\d)\s*$/', '\3-\2-\1 ', $td[1]->plaintext) . trim($td[2]->plaintext) . ":00"
        , 'tiitel' => $td[3]->plaintext
        , 'asukoht' => $td[4]->plaintext
        , 'hind' => null
        , 'link' => 'http://www.linnateater.ee' . current($td[3]->find('a'))->href
        , 'valjamuudud'   => strpos($td[5]->plaintext, 'Välja müüdud') === false ? 0 : 1
        , 'reserveeritud' => strpos($td[6]->plaintext, 'Reserveeritud') === false ? 0 : 1
        , 'lisainfo' => trim(str_replace('Reserveeritud!', '', $td[6]->plaintext))
        , 'plevi' => ''
    );
    if (!$record['valjamuudud']) {
        $a = $td[5]->find('a');
        if (!empty($a)) $record['plevi'] = $a[0]->href;
    }
    $kava[] = $record;
}
scraperwiki::save_sqlite(array('id'), $kava, 'kava');

<?php
$html = scraperWiki::scrape("http://www.linnateater.ee/et/mangukava/");
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
$kava = array();
$id = 0;
foreach($dom->find('#kava tr') as $tr) {
    $td = $tr->find('td');
    if (empty($td[1])) continue; # Using colspan stuff ... :/

    $record = array(
          'id' => $id++
        , 'aeg' => preg_replace('/.*(\d\d).(\d\d).(\d\d\d\d)\s*$/', '\3-\2-\1 ', $td[1]->plaintext) . trim($td[2]->plaintext) . ":00"
        , 'tiitel' => $td[3]->plaintext
        , 'asukoht' => $td[4]->plaintext
        , 'hind' => null
        , 'link' => 'http://www.linnateater.ee' . current($td[3]->find('a'))->href
        , 'valjamuudud'   => strpos($td[5]->plaintext, 'Välja müüdud') === false ? 0 : 1
        , 'reserveeritud' => strpos($td[6]->plaintext, 'Reserveeritud') === false ? 0 : 1
        , 'lisainfo' => trim(str_replace('Reserveeritud!', '', $td[6]->plaintext))
        , 'plevi' => ''
    );
    if (!$record['valjamuudud']) {
        $a = $td[5]->find('a');
        if (!empty($a)) $record['plevi'] = $a[0]->href;
    }
    $kava[] = $record;
}
scraperwiki::save_sqlite(array('id'), $kava, 'kava');

