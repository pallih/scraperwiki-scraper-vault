<?php
$url = "https://docs.google.com/a/simon-ops.com/spreadsheet/pub?key=0Anxp9Kw6BG01dE16SUF5Uk5sVjdNdVNfVnh0bDVnclE&single=true&gid=4&range=D3:E3&output=html";
$html = scraperWiki::scrape($url);
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);
$ptr = 0;
foreach($dom->find("table tr") as $data){
    $tds = $data->find("td.s1");

    $record = array(
        'status' => str_replace('%','',$tds[0]->plaintext)
    );
    scraperwiki::save(array('status'),$record);
}


?>