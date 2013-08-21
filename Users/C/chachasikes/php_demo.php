<?php

echo "This is a sample Scraper.";
// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$target = "http://www.golflink.com.au/HandicapHistory.aspx?golflink_no=6911800002";
$html = file_get_html($target);

echo $html;

$dom = new simple_html_dom();
$dom->load($html);

// Get all of the contents of all paragraphs.
#$arr = array(); 
#foreach ($dom->find('p') as $p)
#    array_push($arr, $p->plaintext);

    
#scraperwiki::save($arr, $arr);



?>
