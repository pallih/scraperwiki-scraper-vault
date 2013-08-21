<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$html = scraperwiki::scrape("http://www.handball.no/kamper.asp?AvdId=12370&mal=2&lag=6294");
$dom->load($html);

#print $dom."\n";

$table = $dom->find("table",0);
$records = array();

#foreach($table->find("tr.second") as $tr_dato){
    #print $tr_dato->plaintext."\n";
#}
$i = 0;

foreach($table->find("tr") as $tr){
    $j = 0;
    foreach($tr->find("td") as $data){
       #print $data->plaintext."\t";
       $records[i][j] = $data->plaintext;
       $j = $j + 1;
    }
    $i = $i + 1;
    #print"\n";
}

print_r($records);



?>