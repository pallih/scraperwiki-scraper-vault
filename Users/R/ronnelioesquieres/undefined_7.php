<?php

require 'scraperwiki/simple_html_dom.php'; $html_content = scraperwiki::scrape("https://scraperwiki.com/"); $html = str_get_html($html_content); 
foreach ($html->find("div.featured a") as $el) { print $el . "\n"; } 
print $el->href . "\n";
$el = $html->find("div#footer_inner strong",0); print $el . "\n";
print $el->innertext . "\n";
$eg = str_get_html('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>'); print $eg->plaintext . "\n"; // 'A thing goes boom up on the tree' 
?>
