<?php
require 'scraperwiki/simple_html_dom.php'; 
$html = scraperWiki::scrape("http://www.vbce.ca/index.cfm?fuseaction=fx_services.Gold&Silver"); 

function get_codes($dom){
    foreach($dom->find('tr[class^="list_row"]') as $data){
        $tds = $data->find("td");
       
             
              //print $tds[0]->plaintext . "\n";
               $record = array('item'=>$tds[0]->plaintext,
                               'BUY_CND'=>$tds[1]->plaintext,
                               'SELL_CND'=>$tds[2]->plaintext,
                               'BUY_US'=>$tds[3]->plaintext,
                               'SELL_US'=>$tds[4]->plaintext);
            scraperwiki::save_sqlite(array("item"), $record);

             print_r($record);
             
       
    }

}

           
     
$dom = new simple_html_dom();
$dom->load($html);

//print $dom;
get_codes($dom);


?>
