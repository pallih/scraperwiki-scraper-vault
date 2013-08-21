<?php
require 'scraperwiki/simple_html_dom.php'; 
$i=1;
$html;
while ($i < 2200){
    $html = $html . scraperWiki::scrape("http://www.airteamimages.com/search.php?picnum=50&srch_page=1"+$i);
}
echo $html;                 
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='image'] a") as $data){
    $tds = $data->href;
    $url= "http://www.airteamimages.com".$tds;
$record = array(
            'country' => $url
           
);
    //print json_encode($url) . "\n";
 

 scraperwiki::save(array('country'), $record);             
}
?>
