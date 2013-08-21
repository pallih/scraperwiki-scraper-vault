<?php
 //Because I can't clear the datastore with the button
 /*
 scraperwiki::sqliteexecute("DROP TABLE `t1`;");
 scraperwiki::sqliteexecute("DROP TABLE `swdata`;");
 scraperwiki::sqlitecommit();
 */

 require 'scraperwiki/simple_html_dom.php';    
 $url = 'http://www.bom.gov.au/products/IDQ60901/IDQ60901.94580.shtml';

 function tables($html) {
  return $html->find('table[@class!="stationdetails"]');
  //return $html->find('tbody');
 }
 function trs($table) {
   return $table->find('tr');
 }
 function tds($tr) {
  return $tr->find('td');
 }

 // Create DOM from URL
 $html = file_get_html($url);
 $uniques=array();

 //Something's going wrong when the table switches.
 foreach(tables($html) as $table) {
  $table_name=$table->id;
  foreach(trs($table) as $tr){
   if($tr->find('th')) {
    //Skip the header rows. (There are two per table, and they are formatted differently.)
    continue;
   } else {
    $data=array();
    foreach(tds($tr) as $td){
     $key=$td->headers;
     $value=$td->plaintext;
     $data[$key]=$value;
    }
    scraperwiki::save_sqlite($uniques,$data,$table_name);
    unset($data);
   }
  }
  unset($table_name);
 }

 ?>
