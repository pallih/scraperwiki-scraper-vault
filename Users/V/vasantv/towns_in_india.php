<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

$cityArr = array('bangalore','chennai','pune','hyderabad','ahmedabad','kolkata','kochi','Delhi-NCR','delhi','gurgaon','nashik','jaipur');

foreach ($cityArr as $city) {
foreach (range('A','Z') as $char)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.commonfloor.com/localities/index/city/$city/c/".$char);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[cellspacing="2"]') as $table){
            foreach($table->find('td[width="150px"]') as $td) {
            $locality = trim($td->plaintext);
            $record = array(
                    'city' => $city,
                    'locality' => $locality            
                    );
            print_r($record);
            scraperwiki::save_sqlite(array("city","locality"),$record,"Localities");
     }
 }  
    $dom->__destruct();
}

}
?><?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

$cityArr = array('bangalore','chennai','pune','hyderabad','ahmedabad','kolkata','kochi','Delhi-NCR','delhi','gurgaon','nashik','jaipur');

foreach ($cityArr as $city) {
foreach (range('A','Z') as $char)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.commonfloor.com/localities/index/city/$city/c/".$char);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('table[cellspacing="2"]') as $table){
            foreach($table->find('td[width="150px"]') as $td) {
            $locality = trim($td->plaintext);
            $record = array(
                    'city' => $city,
                    'locality' => $locality            
                    );
            print_r($record);
            scraperwiki::save_sqlite(array("city","locality"),$record,"Localities");
     }
 }  
    $dom->__destruct();
}

}
?>