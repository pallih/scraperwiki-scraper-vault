<?php
$html = scraperWiki::scrape("http://www.draamateater.ee/playlist");
require 'scraperwiki/simple_html_dom.php';

$enMonth = array(
      'jaanuar' => 'January', 'veebruar' => 'February' , 'märts' => 'March' , 'aprill' => 'April' , 'mai' => 'May' , 'mai' => 'May'
    , 'juuni' => 'June', 'juuli' => 'July', 'august' => 'August', 'september' => 'September', 'oktoober' => 'October', 'november' => 'November', 'detsember' => 'December');

$kava = array();
$piletimaailm = array();

$dom = new simple_html_dom();
$dom->load($html);
$id = 0;
foreach($dom->find("#tablesorter tbody tr") as $tr){
    $td = $tr->find("td");
    if (empty($td[0])) continue;
    $desc = $tr->find('.kirjeldus');
    $desc = empty($desc) ? null : $desc[0]->plaintext;

    $record = array(
          'id' => $id++
        , 'aeg' =>  date("Y-m-d", strtotime(str_replace('.', '', str_replace(array_keys($enMonth), array_values($enMonth), substr($td[0]->plaintext, 1))))) . " " . $td[3]->plaintext . ":00"
        , 'tiitel' => $td[2]->plaintext
        , 'asukoht' => $td[4]->plaintext
        , 'hind' => null
        , 'link' => 'http://www.draamateater.ee' . current($td[2]->find('a'))->href
        , 'valjamuudud' => strpos($td[5]->plaintext, 'Välja müüdud') === false ? 0 : 1
        , 'reserveeritud' => strpos($desc, 'Reserveeritud') === false ? 0 : 1
        , 'lisainfo' => strpos($desc, 'Reserveeritud') === false ? $desc : null
        , 'pmaailm' => ''
    );
    if (!$record['valjamuudud']) {
        $a = $td[5]->find('a');
        if (count($a)) $record['pmaailm'] = $a[0]->href;
    }
    $kava[] = $record;
}

scraperwiki::save_sqlite(array('id'), $kava, 'kava');