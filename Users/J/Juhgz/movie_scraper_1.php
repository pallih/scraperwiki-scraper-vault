<?php
$html = scraperWiki::scrape("http://www.1channel.ch/watch-1724-The-Girl-Next-Door");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();$dom->load($html);

foreach($dom->find("div[@class='stage_navigation movie_navigation'] h1.titles a") as $title);
print $title . "\n";

foreach($dom->find("div[@class='movie_thumb'] img") as $pic);
print $pic . "\n";

foreach($dom->find("table[@class='movie_version'] span[@class='movie_version_link'] a[@href]") as $version1_link);
print $version1_link . "\n";
foreach($dom->find("table[@class='movie_version'] span[@class='version_host']") as $version1_host);
print $version1_host;

foreach($dom->find("table[@class='movie_version'] span[@class='movie_version_link'] a[@href]") as $version2_link);
print $version2_link . "\n";
foreach($dom->find("table[@class='movie_version'] span[@class='version_host']") as $version2_host);
print $version2_host;

foreach($dom->find("table[@class='movie_version'] span[@class='movie_version_link'] a[@href]") as $version3_link);
print $version3_link . "\n";
foreach($dom->find("table[@class='movie_version'] span[@class='version_host']") as $version3_host);
print $version3_host;

foreach($dom->find("table[@class='movie_version'] span[@class='movie_version_link'] a[@href]") as $version4_link);
print $version4_link . "\n";
foreach($dom->find("table[@class='movie_version'] span[@class='version_host']") as $version4_host);
print $version4_host;

foreach($dom->find("table[@class='movie_version'] span[@class='movie_version_link'] a[@href]") as $version5_link);
print $version5_link . "\n";
foreach($dom->find("table[@class='movie_version'] span[@class='version_host']") as $version5_host);
print $version5_host;
 
?>


