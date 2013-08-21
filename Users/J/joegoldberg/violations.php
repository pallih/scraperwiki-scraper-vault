<?php

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("CREATE TABLE if not exists Violations (Inspection Numeric, ID int, Type string, Standard text, Issuance NUMERIC, Abate NUMERIC, Current Numeric, Initial Numeric, Contest Numeric, Last_Event Text)");

for ($i = 1;$i < 6000; $i++){
    $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/industry.search?sic=&sicgroup=&naicsgroup=&naics=23&state=All&officetype=All&office=All&startmonth=12&startday=31&startyear=2012&endmonth=01&endday=01&endyear=2010&opt=&optt=&scope=&fedagncode=&owner=&emph=&emphtp=&p_start=&p_finish=".(15880+($i-1)*20)."&p_sort=&p_desc=DESC&p_direction=Next&p_show=20");
    $dom = new simple_html_dom();
    $dom->load($html);

    $records = array();
    $trs = array();
    $tds = array();

    $table = $dom ->find('table',5);
    $trs = $table->find('tr');


    foreach($trs as $tr){
        $td = $tr->find('td', 10);
        $violation = $td->plaintext;
        if($violation != "Vio"){
        if($violation != '&nbsp;'){
            echo "got {$td->plaintext}\n";
            $td2 = $tr->find('td',2);
            $activity_number = trim($td2->plaintext);
            $record = array('activity'=>$activity_number);
            $records[] = $record;
        }
        }
    }
    
    if($records != ''){
    foreach ($records as $record){

        $html = scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=" . $record['activity']);
        $dom = new simple_html_dom();
        $dom->load($html);

        $table = $dom->find('table',9);
        $trs = $table->find('tr');
        $first = true;
        foreach($trs as $tr){
            if(!$first){
            $id = $tr->find('td',2)->plaintext;
            $type = $tr->find('td',3)->plaintext;
            $standard = $tr->find('td',4)->plaintext;
            $issuance = $tr->find('td',5)->plaintext;
            $abate = $tr->find('td',6)->plaintext;
            $current = $tr->find('td',7)->plaintext;
            $initial = $tr->find('td',8)->plaintext;
            $contest = $tr->find('td',9)->plaintext;
            $lastEvent = $tr->find('td',10)->plaintext;
        



            scraperwiki::sqliteexecute("INSERT INTO Violations (Inspection,ID,Type,Standard,Issuance,Abate,Current,Initial,Contest,Last_Event) VALUES " 
            ."('".$record['activity']."','".$id."','".$type."','".$standard."','".$issuance."','".$abate."','".$current."','".$initial."','".$contest."','".$lastEvent."')");
            scraperwiki::sqlitecommit();
            }
            $first = false;
        }
    }   
}
}
    


?>
