<?php

$html = scraperWiki::scrape("http://www.ted.com/talks/quick-list");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("table.downloads tr") as $data){
    if ($data->find("th")) continue;
    $tds = $data->find("td");
    if (!$tds) continue;

    $download_links = $tds[4]->find("a");
    $title_a = $tds[2]->find("a");
    $ted_link = "http://www.ted.com".$title_a[0]->href;
    $record = array(
        'published' => $tds[0]->plaintext, 
        'event' => $tds[1]->plaintext, 
        'title' => $tds[2]->plaintext, 
        'duration' => $tds[3]->plaintext, 
        'download_link_low' => $download_links[0]->href,
        'download_link_regular' => $download_links[1]->href,
        'download_link_high' => $download_links[2]->href,
        'ted_link' => $ted_link
    );
    //print_r($record);
    scraperwiki::save(array('title','ted_link'), $record);
}

?>
<?php

$html = scraperWiki::scrape("http://www.ted.com/talks/quick-list");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("table.downloads tr") as $data){
    if ($data->find("th")) continue;
    $tds = $data->find("td");
    if (!$tds) continue;

    $download_links = $tds[4]->find("a");
    $title_a = $tds[2]->find("a");
    $ted_link = "http://www.ted.com".$title_a[0]->href;
    $record = array(
        'published' => $tds[0]->plaintext, 
        'event' => $tds[1]->plaintext, 
        'title' => $tds[2]->plaintext, 
        'duration' => $tds[3]->plaintext, 
        'download_link_low' => $download_links[0]->href,
        'download_link_regular' => $download_links[1]->href,
        'download_link_high' => $download_links[2]->href,
        'ted_link' => $ted_link
    );
    //print_r($record);
    scraperwiki::save(array('title','ted_link'), $record);
}

?>
