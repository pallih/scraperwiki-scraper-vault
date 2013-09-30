<?php
$html = scraperWiki::scrape("http://www.norwich.gov.uk/intranet_docs/saferfoodawards/FoodRatings.html");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table table.fsr") as $data){
    $ths = $data->find("th");
    $tds = $data->find("td");
    $record = array(
        'premises' => $ths[0]->plaintext, 
        'visit_date' => date($tds[0]->plaintext)
    );
    print_r($record);
}

?>
<?php
$html = scraperWiki::scrape("http://www.norwich.gov.uk/intranet_docs/saferfoodawards/FoodRatings.html");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table table.fsr") as $data){
    $ths = $data->find("th");
    $tds = $data->find("td");
    $record = array(
        'premises' => $ths[0]->plaintext, 
        'visit_date' => date($tds[0]->plaintext)
    );
    print_r($record);
}

?>
