<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.boobpedia.com/boobs/Chloe_Vevrier");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);


foreach($dom->find('td') as $data){
                     print $data->plaintext . "\n";
                 }             

?>