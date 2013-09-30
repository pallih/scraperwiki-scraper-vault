<?php

$html = scraperWiki::scrape("http://http://www.kulturbolaget.se/?section=calendarium");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div id=") as $data){
    $tds = $data->find("td");
    $record = array(
        'band' => $tds[0]->plaintext, 
        'date' => $tds[1]->plaintext
    );
    print_r($record);
}

?>
<?php

$html = scraperWiki::scrape("http://http://www.kulturbolaget.se/?section=calendarium");           
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div id=") as $data){
    $tds = $data->find("td");
    $record = array(
        'band' => $tds[0]->plaintext, 
        'date' => $tds[1]->plaintext
    );
    print_r($record);
}

?>
