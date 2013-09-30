<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
print "Hello, coding in the cloud!";

$html = scraperWiki::scrape("https://twitter.com/search?q=%23repidee13");
//print $html."/n";

$dom = new simple_html_dom();
$dom->load($html);

//<div class="navsubpage" id="menuleftpages";

foreach($dom->find("div[@class='content']") as $data){
$tds = $data->find("p[@class='tweet-text']");
if(count($tds)>0){
for($i = 0; $i<count($tds); $i++){
$record = array( 'tweet' => $tds[$i]->plaintext);
print json_encode($record) . "\n";
}
}
}

?>