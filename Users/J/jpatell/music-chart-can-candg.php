<?php
$html = scraperWiki::scrape("http://www.music-chart.info/Canada/archive/genre/22/Christian%20and%20Gospel/2011/10/11");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[class='text']") as $data){
    $as = $data->find("a");
    $item = $as[0]->plaintext;
    $record = array(
        'song' => $item, 
    );
    scraperwiki::save(array('song'), $record);
}

?>
