<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://eventful.com/events?geo=region_id:984");
print $html;
print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 
foreach ($dom->find('span') as $span)
    array_push($arr, $span->plaintext);

print_r($arr);

scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"$arr"));







?><?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://eventful.com/events?geo=region_id:984");
print $html;
print "\n\nEND OF HTML\n\n"; 

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 
foreach ($dom->find('span') as $span)
    array_push($arr, $span->plaintext);

print_r($arr);

scraperwiki::save_sqlite(array("a"),array("a"=>1, "bbb"=>"$arr"));







?>