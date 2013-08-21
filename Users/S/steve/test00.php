<?php

$url="http://mzalendo.com/Members.ListAll.php";
$html = scraperWiki::scrape($url);

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table#mytable tr") as $data){
    $ths = $data->find("th a");
$tds = $data->find("td a");
if (!$ths[0]){
continue;
}
    $record = array(
        'name' => $ths[0]->plaintext,
'party' => $tds[0]->plaintext,
'constituency' => $tds[1]->plaintext
    );
    print_r($record);
}


?>