<?php

require_once 'scraperwiki/simple_html_dom.php';

 $urlArr = array( "http://www.coastandcountry.co.uk/special-offers-one/amount-10/page-",11,
  "http://www.coastandcountry.co.uk/special-offers-two/amount-10/page-",2,
    "http://www.coastandcountry.co.uk/special-offers-three/amount-10/page-",1,
    "http://www.coastandcountry.co.uk/special-offers-four/amount-10/page-",1);

foreach($urlArr as $url){
 $i = 1;
 $pos = array_search($url , $urlArr);
 $limit = $urlArr[$pos+1];
echo $limit; 
    while($i <= $limit){
   
    echo $url.$i;
        $dom = new simple_html_dom();
        // Load HTML from a URL
        $html = file_get_html($url.$i);
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
            scraperwiki::save(array('COTTAGE_URL'), $record); 
        }
    $i++;
    }
    unset($dom);
}

?><?php

require_once 'scraperwiki/simple_html_dom.php';

 $urlArr = array( "http://www.coastandcountry.co.uk/special-offers-one/amount-10/page-",11,
  "http://www.coastandcountry.co.uk/special-offers-two/amount-10/page-",2,
    "http://www.coastandcountry.co.uk/special-offers-three/amount-10/page-",1,
    "http://www.coastandcountry.co.uk/special-offers-four/amount-10/page-",1);

foreach($urlArr as $url){
 $i = 1;
 $pos = array_search($url , $urlArr);
 $limit = $urlArr[$pos+1];
echo $limit; 
    while($i <= $limit){
   
    echo $url.$i;
        $dom = new simple_html_dom();
        // Load HTML from a URL
        $html = file_get_html($url.$i);
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
            scraperwiki::save(array('COTTAGE_URL'), $record); 
        }
    $i++;
    }
    unset($dom);
}

?><?php

require_once 'scraperwiki/simple_html_dom.php';

 $urlArr = array( "http://www.coastandcountry.co.uk/special-offers-one/amount-10/page-",11,
  "http://www.coastandcountry.co.uk/special-offers-two/amount-10/page-",2,
    "http://www.coastandcountry.co.uk/special-offers-three/amount-10/page-",1,
    "http://www.coastandcountry.co.uk/special-offers-four/amount-10/page-",1);

foreach($urlArr as $url){
 $i = 1;
 $pos = array_search($url , $urlArr);
 $limit = $urlArr[$pos+1];
echo $limit; 
    while($i <= $limit){
   
    echo $url.$i;
        $dom = new simple_html_dom();
        // Load HTML from a URL
        $html = file_get_html($url.$i);
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
            scraperwiki::save(array('COTTAGE_URL'), $record); 
        }
    $i++;
    }
    unset($dom);
}

?>