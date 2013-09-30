<?php

# Blank PHP
print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://www.heinemann-dutyfree.com/fraport_en/cigarettes-cigars/cigars");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span[@class='product-name']") as $data){
    $tds = $data->find("a");
    $record = array('product' => $tds[0]->plaintext);
    scraperwiki::save(array('product'), $record);
}




?>
<?php

# Blank PHP
print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("http://www.heinemann-dutyfree.com/fraport_en/cigarettes-cigars/cigars");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span[@class='product-name']") as $data){
    $tds = $data->find("a");
    $record = array('product' => $tds[0]->plaintext);
    scraperwiki::save(array('product'), $record);
}




?>
