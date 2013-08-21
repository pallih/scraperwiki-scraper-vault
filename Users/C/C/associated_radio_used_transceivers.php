<?php
// Pull from Associated Radio's Used Section
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://associatedradio.com/uitem_list.php?ucat=HF%20Transceivers");

$dom = new simple_html_dom();
$dom->load($html);

$count = 0;
foreach($dom->find("div.page table tbody tr") as $data){
    $count++;
    if($count == 1)
        continue;
    if($count%2)
        continue;

    $tds = $data->find("td");
    $imgs = $data->find("img");
    $record = array(
        'image' => '<img src="http://associatedradio.org/'.$imgs[0]->src .'" />', 
        'manufacturer' => $tds[1]->plaintext,
        'model' => $tds[2]->plaintext,
        'description' => $tds[3]->plaintext,
        'price' => $tds[4]->plaintext
    );
    scraperwiki::save(array('description'), $record);
}


?>
