<?php

$html = scraperWiki::scrape("http://37.128.191.200/latest.php");

require "scraperwiki/simple_html_dom.php";
$dom = new simple_html_dom();
$dom->load($html);

scraperwiki::attach("xbmc_noobroom");

$data = scraperwiki::select(           
    "* from xbmc_noobroom.swdata"
);

foreach($data as $d){
print_r($d["noobid"]." ");
}

print "\n";

$i=0;
foreach($dom->find("a") as $Movie){
    if($i==10) break;
    $noobId = preg_replace('/\/\?(\d+$)/', '$1', $Movie->href);
    $i++;
print_r($noobId." ");
}



?>
