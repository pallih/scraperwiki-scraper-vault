<?php

$html = scraperWiki::scrape("http://mtm-power.com/index.php/de/produkte/acdc-module?view=serie&sid=115");           
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table tr") as $data)
echo $data;
?>
