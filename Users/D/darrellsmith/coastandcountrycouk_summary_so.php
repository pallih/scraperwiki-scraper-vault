<?php

require_once 'scraperwiki/simple_html_dom.php';


$maxpages = 9;

$i = 1;
while($i<=$maxpages){

    $url = "http://www.coastandcountry.co.uk/special-offers-one/amount-10/page-".$i;
    #require_once 'scraperwiki/simple_html_dom.php';
    $dom = new simple_html_dom();
    // Load HTML from a URL
    $html = file_get_html($url);
    $dom->load($html);
    foreach($dom->find('div[class=property-result]') as $entry){

        // Get Prices
        foreach($entry->find('span[class=price-range]') as $data){
          $prices = explode("-",$data->plaintext);    
          $low = @str_replace("&pound;","",$prices[0]);
          $high = @str_replace("&pound;","",$prices[1]);      
        }

    
        foreach($entry->find('div[class=property-result-links]') as $data){
           $element = $data->find('a');
           $link = $element[0];
           $cotturl = str_replace("/cottage-details/","",$link->getAttribute('href'));
        }         
    

$record = array(
            'COTTAGE_URL'    => $cotturl, 
            'PRICE_LOW'      => $low,            
            'PRICE_HIGH'     => $high,            
            );
     
    print_r($record);
    scraperwiki::save(array('COTTAGE_URL'), $record); 

    
   
    }
$i++;
}
    
    












?>