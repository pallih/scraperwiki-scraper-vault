<?php

scraperwiki::httpresponseheader('Content-Type', 'text/html; charset=Shift_JIS');
$html =  scraperWiki::scrape("http://www.u-tokyo.ac.jp/public/public01_02_2011_j.html");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); $dom->load($html);
$key = 1;

foreach($dom->find("table[@class='plane'] tr") as $data){
     $tds = $data->find("td");
     $links = $data->find("a");
     

     //$record[] = array(
     //$record = array(
     //    'key' => $key,
     //    'date' => $tds[0]->plaintext,
     //    'title' => $links[0]->plaintext,
     //    'link' => $links[0]->href
     //);
     //print_r($record);
     scraperwiki::save_sqlite(array("key"),array("key"=>$key,"date"=>$tds[0]->plaintext,"title"=>$links[0]->plaintext,"link" => $links[0]->href));
     $key = $key + 1;
} 
//scraperwiki::save_sqlite(array("key"),$record);
?>
<?php

scraperwiki::httpresponseheader('Content-Type', 'text/html; charset=Shift_JIS');
$html =  scraperWiki::scrape("http://www.u-tokyo.ac.jp/public/public01_02_2011_j.html");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); $dom->load($html);
$key = 1;

foreach($dom->find("table[@class='plane'] tr") as $data){
     $tds = $data->find("td");
     $links = $data->find("a");
     

     //$record[] = array(
     //$record = array(
     //    'key' => $key,
     //    'date' => $tds[0]->plaintext,
     //    'title' => $links[0]->plaintext,
     //    'link' => $links[0]->href
     //);
     //print_r($record);
     scraperwiki::save_sqlite(array("key"),array("key"=>$key,"date"=>$tds[0]->plaintext,"title"=>$links[0]->plaintext,"link" => $links[0]->href));
     $key = $key + 1;
} 
//scraperwiki::save_sqlite(array("key"),$record);
?>
