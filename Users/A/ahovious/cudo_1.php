<?php
require "scraperwiki/simple_html_dom.php";
$html = scraperWiki::scrape("http://cudo.com.au/brisbane");
$dom = new simple_html_dom();
$dom->load($html);
$counter = 0;
if (! function_exists('pcntl_fork')) die('PCNTL functions not available on this PHP installation'); 
//foreach($dom->find("div.deal") as $data){
//print_r($data);
    $h1 = $dom->find("h1");
    $Price = $dom->find("span.priceAmount");
    $Value = $dom->find("span.valueAmt");
    $Savings = $dom->find("span.saveAmt");
    $Percentage = $dom->find("span.valPercentage");
    $Sold = $dom->find("span.offerAmount");
    $TimeLeft = $dom->find("p.countdown_amount");

$record = array(
        "Name" => $h1[0]->plaintext,
        "Price" => $Price[0]->plaintext,
        "Value" => $Value[0]->plaintext,
        "Savings" => $Savings[0]->plaintext,
        "Percentage" => $Percentage[0]->plaintext,
        "Sold" => $Sold[0]->plaintext,
        "TimeLeft" => $TimeLeft[0]->plaintext
        
        //"position" => $tds[3]->plaintext,
        //"url" => $person_url,
        //"info" => $person_info
    );
    print_r($record);
   scraperwiki::save_sqlite($record,$record);

//}
?>