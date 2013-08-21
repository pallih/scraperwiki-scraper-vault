<?php
 #There's a bug in the website that causes the headers attribute of the first row to be named incorrectly.

 require 'scraperwiki/simple_html_dom.php';    
 $url = 'http://www.bom.gov.au/products/IDQ60901/IDQ60901.94580.shtml';

 function tables($html) {
  return $html->find('table[@class!="stationdetails"]');
 }
 function trs($table) {
   return $table->find('tr');
 }
 function tds($tr) {
  return $tr->find('td');
 }

 $html = file_get_html($url);
 $uniques=array();

 //Previous table's name, needed because of a bug in the webpage
 $table_name_prev="t1";
 //Table contents
 foreach(tables($html) as $table) {
  $table_name=$table->id;
  foreach(trs($table) as $tr){
   if($tr->find('th')) {
    //Skip the header rows. (There are two per table, and they are formatted differently.)
    //Later, we can add something to rename the columns based on headers
    continue;
   } else {
    $row=array();
    foreach(tds($tr) as $td){
     $key_raw=$td->headers;

     //If the previous table's name is used in the attribute, replace it with the current name
     $key=str_replace($table_name_prev, $table_name, $key_raw);

     unset($key_raw);
     $value=$td->plaintext;
     if ($key!=''){
       $row[$key]=$value;
     }
    }
    scraperwiki::save_sqlite($uniques,$row,$table_name);
    unset($row);
   }
  }
  $table_name_prev=$table_name;
  unset($table_name);
 }
 foreach($html->find('th') as $th){
  $header_id=$th->id;
  $header_description=$th->plaintext;
  $row=array(
    "header_id" => $header_id,
    "header_description" => $header_description
  );
  scraperwiki::save_sqlite($uniques,$row,'headers');
 }
 ?>
