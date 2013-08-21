<?php

## Get first URL
$html = scraperWiki::scrape("http://www.20000-names.com/male_english_names.htm");

## Loop through the rest of the URLs and attach them to $html
for ($i=2; $i<=17; $i++){
$html = $html . scraperWiki::scrape("http://www.20000-names.com/male_english_names_" . str_pad($i, 2, "0", STR_PAD_LEFT) . ".htm");      
     }

require 'scraperwiki/simple_html_dom.php';     
     
$dom = new simple_html_dom();
$dom->load($html);

#$links = $dom->find("font[@size='1'] a");
#foreach($links as $link){
#print $link . "\n";
#}

foreach($dom->find("font[@color='#9393FF']") as $data){

        $record = array(
'name' => strip_tags($data)
 );

      scraperwiki::save(array('name'), $record);  
    }


     



?>
<?php

## Get first URL
$html = scraperWiki::scrape("http://www.20000-names.com/male_english_names.htm");

## Loop through the rest of the URLs and attach them to $html
for ($i=2; $i<=17; $i++){
$html = $html . scraperWiki::scrape("http://www.20000-names.com/male_english_names_" . str_pad($i, 2, "0", STR_PAD_LEFT) . ".htm");      
     }

require 'scraperwiki/simple_html_dom.php';     
     
$dom = new simple_html_dom();
$dom->load($html);

#$links = $dom->find("font[@size='1'] a");
#foreach($links as $link){
#print $link . "\n";
#}

foreach($dom->find("font[@color='#9393FF']") as $data){

        $record = array(
'name' => strip_tags($data)
 );

      scraperwiki::save(array('name'), $record);  
    }


     



?>
