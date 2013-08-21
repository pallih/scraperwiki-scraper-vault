<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range('A', 'Z') as $char)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://www.medindia.net/doctors/drug_information/home.asp?alpha=".$char);               
    
    $dom->load($html);

   //print ("CHAR:".$char);
 
   foreach($dom->find('a[class="ta15blue tbold"]') as $data){
            $record = array('name' => $data->plaintext);
            //print_r($record);
            scraperwiki::save_sqlite(array("name"),$record,"Druglist");
    }
    
    $dom->__destruct();
}
?>
