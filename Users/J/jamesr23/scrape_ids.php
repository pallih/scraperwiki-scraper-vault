<?php

## Get first URL
$html = scraperWiki::scrape("http://mapit.jenny.212.110.187.249.xip.io/areas/PFL.html");

require 'scraperwiki/simple_html_dom.php';     
     
$dom = new simple_html_dom();
$list = new simple_html_dom();
$dom->load($html);

#$links = $dom->find("font[@size='1'] a");
#foreach($links as $link){
#print $link . "\n";
#}

foreach($dom->find("li") as $data){

$list->load($data);
$header = $list->find("h3");
$id = $list->find("p");
print strip_tags($header[0]) . ", " . strip_tags(substr($id[0],6,5)) . "\n";

        $record = array(
'name' => strip_tags($header[0]),
'id' => strip_tags(substr($id[0],6,5))
 );

     scraperwiki::save(array('name'), $record);  
    }


     



?><?php

## Get first URL
$html = scraperWiki::scrape("http://mapit.jenny.212.110.187.249.xip.io/areas/PFL.html");

require 'scraperwiki/simple_html_dom.php';     
     
$dom = new simple_html_dom();
$list = new simple_html_dom();
$dom->load($html);

#$links = $dom->find("font[@size='1'] a");
#foreach($links as $link){
#print $link . "\n";
#}

foreach($dom->find("li") as $data){

$list->load($data);
$header = $list->find("h3");
$id = $list->find("p");
print strip_tags($header[0]) . ", " . strip_tags(substr($id[0],6,5)) . "\n";

        $record = array(
'name' => strip_tags($header[0]),
'id' => strip_tags(substr($id[0],6,5))
 );

     scraperwiki::save(array('name'), $record);  
    }


     



?><?php

## Get first URL
$html = scraperWiki::scrape("http://mapit.jenny.212.110.187.249.xip.io/areas/PFL.html");

require 'scraperwiki/simple_html_dom.php';     
     
$dom = new simple_html_dom();
$list = new simple_html_dom();
$dom->load($html);

#$links = $dom->find("font[@size='1'] a");
#foreach($links as $link){
#print $link . "\n";
#}

foreach($dom->find("li") as $data){

$list->load($data);
$header = $list->find("h3");
$id = $list->find("p");
print strip_tags($header[0]) . ", " . strip_tags(substr($id[0],6,5)) . "\n";

        $record = array(
'name' => strip_tags($header[0]),
'id' => strip_tags(substr($id[0],6,5))
 );

     scraperwiki::save(array('name'), $record);  
    }


     



?>