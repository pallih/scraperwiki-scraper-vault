<?php

function get_codes($dom){
    foreach($dom->find("select") as $data){
     
         foreach($data->find("option") as $op) {
             
             $record = array('stockCode' => $op->value,
                              'stockSymbol' => $op->plaintext );
              $message = scraperwiki::save_sqlite(array("stockCode"), $record);
              #print_r($message); 
             
        }
    }
}

$html = scraperWiki::scrape("http://www.jamstockex.com/controller.php?action=view_stock_information&StockCode=102");           
# print $html . "\n";
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

print $dom;
#get_codes($dom);


?>
