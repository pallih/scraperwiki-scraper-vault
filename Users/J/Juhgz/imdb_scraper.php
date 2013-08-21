<?php

$html = scraperWiki::scrape("http://www.imdb.com/title/tt0265208/");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("p[@itemprop]") as $description);
str_replace("&#x27;", "'", $description);
print $description . "\n";

foreach($dom->find("span[@class='nobr'] a[@title='See all release dates']") as $release_date);
print $release_date . "\n";

foreach($dom->find("div[@class='infobar'] &nbsp;&nbsp;") as $runtime);
print $runtime . "\n";

foreach($dom->find("div[@class='infobar'] a[@href]") as $genres);
print $genres . "\n";

?>
