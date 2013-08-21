<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.ndbc.noaa.gov/data/realtime2/64046.txt");
print $html;

scraperwiki::save(array('data'), array('data' => $html->plaintext));


?>