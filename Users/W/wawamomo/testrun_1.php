<?php
# Blank PHP
print "Hello, coding in the cloud!";
$html = scraperWiki::scrape("http://www.nalsimafrend.jp/tachilog/");
print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div.entry") as $data){
    $tds = $data->find("p");
    $record = array(
        'kiji01' => $tds[0]->plaintext, 
        'kiji02' => $tds[1]->plaintext
    );
    print_r($record);
}
    scraperwiki::save(array('kiji01'), $record);

?>
