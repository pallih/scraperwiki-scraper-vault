<?php

$html = scraperWiki::scrape("http://www.trmc.aec.gov.tw/utf8/big5/main.php");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

$timeZone = new DateTimeZone("Asia/Taipei");
foreach($dom->find('td.w_in_t') as $data) {
  $place = trim($data->plaintext);
  $dateStr = substr($data->find('a', 0)->title, 15, -4);
  $timestamp = DateTime::createFromFormat('Y\/m\/d H:i', $dateStr, $timeZone)->getTimestamp();
  $usv = floatval($data->next_sibling()->plaintext);

  $record = array(
    'place' => $place,
    'time' => $timestamp,
    'usv' => $usv,
  );

  //print json_encode($record) . "\n";
  scraperwiki::save(array('place', 'time'), $record);
}

?>
<?php

$html = scraperWiki::scrape("http://www.trmc.aec.gov.tw/utf8/big5/main.php");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

$timeZone = new DateTimeZone("Asia/Taipei");
foreach($dom->find('td.w_in_t') as $data) {
  $place = trim($data->plaintext);
  $dateStr = substr($data->find('a', 0)->title, 15, -4);
  $timestamp = DateTime::createFromFormat('Y\/m\/d H:i', $dateStr, $timeZone)->getTimestamp();
  $usv = floatval($data->next_sibling()->plaintext);

  $record = array(
    'place' => $place,
    'time' => $timestamp,
    'usv' => $usv,
  );

  //print json_encode($record) . "\n";
  scraperwiki::save(array('place', 'time'), $record);
}

?>
