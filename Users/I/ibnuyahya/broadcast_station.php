<?php
    
    $html = scraperWiki::scrape("http://www.skmm.gov.my/link_file/registers1/aa.asp?aa=AABroadcast&fpg=");       
    
    require 'scraperwiki/simple_html_dom.php';           
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $li = $dom->find('.PageList',0)->find('li');
    
    $max_paging = $li[count($li)-1]->innertext;
    
    $start      = strpos($max_paging,'fpg=');
    $end        = strpos($max_paging,"'>") . "\n";
    $max_paging = substr($max_paging, $start + 4, $end - ( $start + 4 ) );

    $column_name = array('No','Assignment_Holder','Assignment_No','Location','TX_Assign','Region','Expiry_Date');
    scraperwiki::sqliteexecute("drop table if exists broadcast_station"); 
    scraperwiki::sqliteexecute('CREATE TABLE `broadcast_station` (`No` integer,`Assignment_Holder` text, `Assignment_No` text, `Location` text,`TX_Assign` text,`Region` text,  `Expiry_Date` text )');
    $records = array();
    for($page = 1 ; $page <= $max_paging; $page++)
    {
        $html = scraperWiki::scrape("http://www.skmm.gov.my/link_file/registers1/aa.asp?aa=AABroadcast&fpg=" . $page);
    
        $dom->load($html);
        $x = 0;
        foreach($dom->find('.previewTable',0)->find('tr') as $trs){
            
            $tds = $trs->find('td');
            $record = array();
            $i = 0;
            foreach($tds as $td){
                $record[$column_name[$i]] = $td->innertext;
                $i++;
            }
            
            
               
            if($x > 0){
                $record['No'] = (int)$record['No'];
                scraperwiki::save_sqlite(array('No','Assignment_Holder','Assignment_No','Location','TX_Assign','Region','Expiry_Date'), $record,$table_name="broadcast_station");
            }
            $x++;
        }    
    }

?>
