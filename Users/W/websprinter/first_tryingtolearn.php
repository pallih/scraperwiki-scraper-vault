<?php

require 'scraperwiki/simple_html_dom.php'; $html_content = scraperwiki::scrape("https://scraperwiki.com/"); $html = str_get_html($html_content);

$dpUrl = "https://scraperwiki.com/";
foreach ($html->find("div.tags a") as $el) { 

print $el . "\n"; 
print $dpUrl . $el->href . "\n";
print $el->innertext . "\n";


}

?>

