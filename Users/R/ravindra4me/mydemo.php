<?php

$html = scraperWiki::scrape("http://www.amazon.com/Samsung-i9100-Unlocked-Smartphone-Touchscreen/product-reviews/B004QTBQ2C");   
require 'scraperwiki/simple_html_dom.php';       
     $dom = new simple_html_dom();
     $dom->load($html); 
     foreach($dom->find("table[@id='productReviews'] tr") as $data)
     {     
            $tds = $data->find("text");  
                if(count($tds) > 0){
                    print(count($tds));
                    foreach($tds as $text)
                    {
                        print($text);
                    }
                }
                print("\n");
            
         //   $record = array('country' => $tds[0]->plaintext, 'years_in_school' => intval($tds[4]->plaintext));
         //   scraperwiki::save(array('country','years_in_school') , $record);           
     } 

?>
