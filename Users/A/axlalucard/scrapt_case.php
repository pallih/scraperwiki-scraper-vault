<?php
require 'scraperwiki/simple_html_dom.php';   

$url[] = "cpu";
$url[] = "motherboard";
$url[] = "memory";
$url[] = "internal-hard-drive";
$url[] = "video-card";
$url[] = "power-supply";
$url[] = "case";
$url[] = "monitor";



$html = scraperWiki::scrape("http://pcpartpicker.com/parts/case/");


         
$dom = new simple_html_dom();
$dom->load($html);
unset($html);


foreach($dom->find("id=\"list_table\" tr") as $data){
    $tds = $data->find("td");
    $tdsa = $data->find("td a");

    if(!empty($tds[0])){
      

        $html_a = scraperWiki::scrape("http://pcpartpicker.com".$tdsa[0]->href); 
        $dom_a = new simple_html_dom();
        $dom_a->load($html_a);        
        
        $table_a = $dom_a->find("table class=\"box-table-a\"");
        
        $rekod_a["href"]= $tdsa[0]->href;
        foreach($table_a[0]->find("tr") as $data_a){   
             $tds_a = $data_a->find("td");
                
             $rekod_a[$tds_a[0]->plaintext] = $tds_a[1]->plaintext;
                    
        }
        
        scraperwiki::save(array('href'), $rekod_a);    
        //print json_encode($rekod_a) . "\n";
        $dom_a ->__destruct();
    }
    
}

$dom->__destruct();




?>