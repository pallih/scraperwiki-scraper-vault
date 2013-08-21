<?php

# Source: KEK http://rcwww.kek.jp/norm/dose.html

$html = scraperWiki::scrape("http://rcwww.kek.jp/norm/dose.html");

$data = preg_replace('/<[^>]*>/', "", $html);
#print $data;

$pattern = "/([^\s|^\(|^\)]+)/i";
preg_match_all($pattern, $data, $matches);

$date = $matches[1][2]. " ". $matches[1][3]. "JST";
#print $date;
$record_datetime = date_create($date);

$record = array(
    'name' => "KEK",
    'radiation' => $matches[1][0],
    'units' => $matches[1][1],
    'datetime' => $record_datetime
);
#print_r($record);
scraperwiki::save(array('datetime'), $record);

?>
