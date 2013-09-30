<?php
require 'scraperwiki/simple_html_dom.php';   
function get_string_between($string, $start, $end){
    $string = " ".$string;
    $ini = strpos($string,$start);
    if ($ini == 0) return "";
    $ini += strlen($start);
    $len = strpos($string,$end,$ini) - $ini;
    return substr($string,$ini,$len);
}
$count=0;
//print_r(scraperwiki::show_tables());      
while($count < 5){
  $count++;       
  $html_content = scraperwiki::scrape("http://www.elks.org/lodges/contactus.cfm?LodgeNumber=".$count);
  $html = str_get_html($html_content);
  $el = $html->find("iframe",0);
  if(isset($el->src)){ 
    $q = $el->src;
    $q = str_replace("<head>","",$q);
    $q = str_replace("hl=en&amp;","",$q);
    $q = str_replace('http://maps.google.com/maps?q=','',$q);
    $q = str_replace("+(",'","',$q);
    $q = str_replace(")",'"',$q);
    $q = str_replace(" No. ",'","',$q);
    $pos = strpos($q,"&amp;");
    $q = substr($q,0,$pos);
    $q = str_replace("+"," ",$q);
    $q = '"' . $q;
    //scraperwiki::save(array('lodge'.$count), array("address" => $q));
    print $q;
    //$message = scraperwiki::save_sqlite(array("lodge"), array("number"=>$count, "address"=>$q));
    //print_r($message); 
  }
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';   
function get_string_between($string, $start, $end){
    $string = " ".$string;
    $ini = strpos($string,$start);
    if ($ini == 0) return "";
    $ini += strlen($start);
    $len = strpos($string,$end,$ini) - $ini;
    return substr($string,$ini,$len);
}
$count=0;
//print_r(scraperwiki::show_tables());      
while($count < 5){
  $count++;       
  $html_content = scraperwiki::scrape("http://www.elks.org/lodges/contactus.cfm?LodgeNumber=".$count);
  $html = str_get_html($html_content);
  $el = $html->find("iframe",0);
  if(isset($el->src)){ 
    $q = $el->src;
    $q = str_replace("<head>","",$q);
    $q = str_replace("hl=en&amp;","",$q);
    $q = str_replace('http://maps.google.com/maps?q=','',$q);
    $q = str_replace("+(",'","',$q);
    $q = str_replace(")",'"',$q);
    $q = str_replace(" No. ",'","',$q);
    $pos = strpos($q,"&amp;");
    $q = substr($q,0,$pos);
    $q = str_replace("+"," ",$q);
    $q = '"' . $q;
    //scraperwiki::save(array('lodge'.$count), array("address" => $q));
    print $q;
    //$message = scraperwiki::save_sqlite(array("lodge"), array("number"=>$count, "address"=>$q));
    //print_r($message); 
  }
}

?>
