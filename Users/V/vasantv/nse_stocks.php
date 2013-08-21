<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

foreach (range('A','Z') as $char)
{
    $dom = new simple_html_dom();

    for($pageNum = 0; $pageNum <= 10; $pageNum++)
    {
       $html = scraperWiki::scrape("http://www.kotaksecurities.com/stock-market-news/equity/1024/pe-ratio-NSE-All-".$char."/".$pageNum);               
       if($html == NULL)
       { continue; }
 
       $dom->load($html);   

   //print ("CHAR:".$char);
 
    foreach($dom->find('table[class="TableBG1"]') as $table){
     foreach($table->find('tr[class="tabbody"]') as $tr) {
            $stock = $tr->children(0)->plaintext;
            $close = $tr->children(1)->plaintext;
            $eps   = $tr->children(2)->plaintext;
            $pe    = $tr->children(3)->plaintext;
      
            $record = array(
                    'stock' => $stock,
                    'close' => $close,
                     'eps' => $eps,
                     'pe' => $pe
                    );
            //print_r($record);
            scraperwiki::save_sqlite(array("stock"),$record,"NSE_Stocks");
       }
  }
 }
    $dom->__destruct();
}
?>