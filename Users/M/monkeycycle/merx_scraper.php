<?php

require 'scraperwiki/simple_html_dom.php';

print "Hello, scraping in the cloud!";

$RemoteURL[16704901] = 'http://www.raqs.merx.com/public/contract/contractHistoryView.jsf?id=16704901';


$html = scraperWiki::scrape("$RemoteURL[16704901]");
// print $html . "\n";


$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("form") as $data){
    print_r($data);
}


?>