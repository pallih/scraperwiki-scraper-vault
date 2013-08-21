<?php
# Blank PHP

$html = scraperwiki::scrape('http://visualartists.ie/category/listings/');
#echo $html;

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('div id="stats" class="clearfloat"') as $data){
    print $data->plaintext . "\n";
} 

?>
