<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

$counter = 1;
foreach (range('B','Z') as $char)
{
    $dom = new simple_html_dom();

    $html = scraperWiki::scrape("http://imanashik.org/Doctor%20directory_".$char.".html");
    $dom->load($html);

   //print ("CHAR:".$char);
 
   
   foreach($dom->find('td[width="272"]') as $data_table){
            $data = $data_table->plaintext;

            $record = array('counter'=> $counter,'data'=>$data);
            //print_r($record);
            scraperwiki::save_sqlite(array("counter"),$record,"Nashik_Docs");
            $counter++;
   }
     
   $dom->__destruct();
}
?>