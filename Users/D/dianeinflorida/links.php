<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx");
 

$dom = new simple_html_dom();
$dom->load($html);
$links= $dom->find('.membername');
$arr = array(); 
foreach ($links->find('href') as $link)
    array_push($arr, $link->plaintext);

print_r($arr);

?>