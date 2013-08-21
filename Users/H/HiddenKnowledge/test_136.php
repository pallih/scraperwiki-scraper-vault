<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$html = scraperWiki::scrape("http://www.niftyhost.us/support/forum-4.html");
$dom->load($html); 
foreach($dom->find("a.subject_new") as $data)
{ //print_r($data->innertext . "\n");
$i += 1;
$url = "http://niftyhost.us/support/" . $data->href;
$name = array('id' => $i, 'name' => $data->innertext, 'url' => $url);
scraperwiki::save(array('id'), $name);
}
?>
