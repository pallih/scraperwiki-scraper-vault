<?php
// Vars
$to = "info@johanrunesson.se";
$subject = "Veckans reklamblad (V. ".date("W").")";
$body = "<h3>Reklamblad vecka ".date("W")."</h3>";

// Init
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$ads = array();
$date = date("Y-m-d");

// Maxi
$ads["Maxi"] =  "http://www.e-magin.se/latestpaper/cv4gzm01/paper";

// Citygross
$html = scraperWiki::scrape("http://citygross.se/Butiker/Ljungby/");
$dom->load($html);
$counter = 1;
foreach($dom->find("div.thisWeeksAd") as $data){
    $link = $data->find("a");
    $ads["Citygross"] =  $link[0]->href;
}

// Hemköp
$html = scraperWiki::scrape("http://hemkop.se/showdoc.asp?docid=490&channelitemid=338327");
$dom->load($html);
$counter = 1;
foreach($dom->find("div#disposition div.columnset02 div.column02") as $data){
    $link = $data->find("a");
    $ads["Hemköp"] =  "http://hemkop.se".$link[0]->href;
}

// Mediamarkt
$ads["Mediamarkt"] =  "http://www.mediamarkt.se/webapp/wcs/stores/servlet/MultiChannelMarketInfo?storeId=15756&langId=-16";

// Elgiganten
$ads["Elgiganten"] =  "http://ipaper.ipapercms.dk/ElgigantenSE/Elgiganten/?scid=1757q";

// Output
$counter = 1;
foreach($ads as $name => $url) {
    // Save to db
    $record = array('id' => $counter, 'Namn' => $name, 'URL' => $url, 'Vecka' => date("W"), 'Datum' => $date);
    scraperwiki::save(array('id'), $record);
    $counter++;

    // Save text for email.
    //$body .= "<p><strong>".$name.": </strong>".$url."</p>";
}

//mail($to, $subject, $body);

?>