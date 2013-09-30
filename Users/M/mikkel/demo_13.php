<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.heinemann-dutyfree.com/fraport_en/cigarettes-cigars/cigars");
$html = str_get_html($html_content);
foreach ($html->find("span[class='product-name']") as $name) {
    print $name->plaintext . "\n";
}


?>
