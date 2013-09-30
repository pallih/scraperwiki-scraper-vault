<?php
$site = 'http://www.officialworldgolfranking.com/rankings/default.sps';
require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape($site );
$dom = new simple_html_dom();
$dom->load($html);
$headers = array();
foreach($dom->find("table tr td[class='rnkHead']") as $data) {
    $headers[] = $data->plaintext;
}
$i = 0;
$rows = $dom->find("table tr td[class='rnkText']");
if (count($rows) < 50) {
    die();
}

foreach($dom->find("table tr td[class='rnkText']") as $data) {
    
$record[$headers[$i]] = str_replace('&nbsp;', '', str_replace(array("\r", "\r\n", "\n"), '', $data->plaintext));
    
    $i++;
    if ($i >= count($headers)) {
        scraperwiki::save_sqlite(array('Player'), $record); 

        $record = array();
        $i = 0;
    }
}
//
<?php
$site = 'http://www.officialworldgolfranking.com/rankings/default.sps';
require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape($site );
$dom = new simple_html_dom();
$dom->load($html);
$headers = array();
foreach($dom->find("table tr td[class='rnkHead']") as $data) {
    $headers[] = $data->plaintext;
}
$i = 0;
$rows = $dom->find("table tr td[class='rnkText']");
if (count($rows) < 50) {
    die();
}

foreach($dom->find("table tr td[class='rnkText']") as $data) {
    
$record[$headers[$i]] = str_replace('&nbsp;', '', str_replace(array("\r", "\r\n", "\n"), '', $data->plaintext));
    
    $i++;
    if ($i >= count($headers)) {
        scraperwiki::save_sqlite(array('Player'), $record); 

        $record = array();
        $i = 0;
    }
}
//
