<?php

require 'scraperwiki/simple_html_dom.php';

for ($i = 1;$i < 6000; $i++) {
    $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/industry.search?sic=&sicgroup=&naicsgroup=&naics=23&state=All&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2010&opt=&optt=&scope=&fedagncode=&owner=&emph=&emphtp=&p_start=&p_finish=".(19680+($i-1)*20)."&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);

    $records = array();
    $trs = array();
    $tds = array();

    $table = $dom ->find('table',5);
    $trs = $table->find('tr');
    echo "there are ".count($trs)." rows.";
    foreach($trs as $tr){ 
        $td = $tr->find('td', 2);
        $activity_number = trim($td->plaintext);
        if( $activity_number != "Activity" ){   
            echo "got td->plaintext {$td->plaintext}\n";
            $record = array('activity'=>$activity_number);
            $records[] = $record;
        }
    }
    

    
    foreach ($records as $record) {

        $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=" . $record['activity']);
        $dom = new simple_html_dom();
        $dom->load($html);

        if($dom ==''){continue;}

            $table_a = $dom->find('table', 1);
            $td_a = $table_a->find('td',1);

            $table_b = $dom->find('table', 4);   
  
            $table_c = $dom->find('table', 5);
            $tr_a = $table_c->find('tr', 0);
            $tr_b = $table_c->find('tr', 1);
            $tr_c = $table_c->find('tr', 2);
            $tr_d = $table_c->find('tr', 3);
            $tr_e = $table_c->find('tr', 4);
            $union = $tr_b->find('td', 2);
                       
            $table_d = $dom->find('table', 6);
            $tr_f = $table_d->find('tr',0);
            $tr_g = $table_d->find('tr',1);
            $tr_h = $table_d->find('tr',2);
            $tr_i = $table_d->find('tr',3);
            $tr_j = $table_d->find('tr',4);


            
$scraped = array(
'Inspection' => $td_a->plaintext,
'Nr, Report_ID, Open_Date' => $table_b->plaintext,
'Location' => $tr_a->plaintext,
'Address'=> $tr_b->plaintext,
'SIC' => $tr_c->plaintext,
'NAICS' => $tr_d->plaintext,
'Mailing' => $tr_e->plaintext,
'Union Status' => $union->plaintext,
'Inspection Type' => $tr_f->plaintext,
'Scope,Notice' => $tr_g ->plaintext,
'Ownership' => $tr_h ->plaintext,
'Safety/Health, Close Conference' => $tr_i ->plaintext,
'Close Case' => $tr_j ->plaintext,
);
       scraperwiki::save(array('Nr, Report_ID, Open_Date'), $scraped);

    }
}
