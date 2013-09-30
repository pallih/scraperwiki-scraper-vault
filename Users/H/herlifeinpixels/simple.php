<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

//$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");
//print $html;
//print "\n\nEND OF HTML\n\n"; 

$html_content = scraperwiki::scrape("http://ragial.com/cheap/iRO-Renewal/");
$html = str_get_html($html_content);

$dom = new simple_html_dom();
$dom->load($html);

// ---------------- DOM elements ----------------- //
// ID of item name = nmr
// Quantity = amt
// Price = pc
// Standard Price = std
// ----------------------------------------------- //

$arr = array(); 
foreach ($dom->find('tr') as $row) {
    foreach ($row->find('td[pc]') as $col) {
        array_push($arr, $col->plaintext);
    };
};

print_r($arr);

?><?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

//$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");
//print $html;
//print "\n\nEND OF HTML\n\n"; 

$html_content = scraperwiki::scrape("http://ragial.com/cheap/iRO-Renewal/");
$html = str_get_html($html_content);

$dom = new simple_html_dom();
$dom->load($html);

// ---------------- DOM elements ----------------- //
// ID of item name = nmr
// Quantity = amt
// Price = pc
// Standard Price = std
// ----------------------------------------------- //

$arr = array(); 
foreach ($dom->find('tr') as $row) {
    foreach ($row->find('td[pc]') as $col) {
        array_push($arr, $col->plaintext);
    };
};

print_r($arr);

?>