<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("https://scraperwiki.com/");
$html = str_get_html($html_content);
foreach ($html->find("div.featured a") as $el)
 { print $el . "\n";   print $el->href . "\n"; }
$el = $html->find("div#footer_inner strong",0);
 print $el . "\n";
 print $el->innertext . "\n";

?>

