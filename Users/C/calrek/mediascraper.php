<?php

$html = scraperWiki::scrape("http://geocities.ws/calrek/milkyway/index.html");
echo $html;
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();

$dom->load($html);

$arr = array(); 

foreach($dom->find("div[class='file mp3 private']") as $data){

    
    $tds = $data->find("div a");
    
    if($tds){
        $title = $tds[0]->plaintext;
        $date = date('F jS\, Y ');
        $record = array(
            'title' => substr($title, + 0 , -4),
            'link' => $tds[1]->href,
            'description' => $tds[1]->href,
            'enclosure url' => $tds[1]->href,
            'url' => $tds[1]->href,
            'day' => $date
        );
        scraperwiki::save(array('url'), $record); 

    }

}
?>
<?php

$html = scraperWiki::scrape("http://geocities.ws/calrek/milkyway/index.html");
echo $html;
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();

$dom->load($html);

$arr = array(); 

foreach($dom->find("div[class='file mp3 private']") as $data){

    
    $tds = $data->find("div a");
    
    if($tds){
        $title = $tds[0]->plaintext;
        $date = date('F jS\, Y ');
        $record = array(
            'title' => substr($title, + 0 , -4),
            'link' => $tds[1]->href,
            'description' => $tds[1]->href,
            'enclosure url' => $tds[1]->href,
            'url' => $tds[1]->href,
            'day' => $date
        );
        scraperwiki::save(array('url'), $record); 

    }

}
?>
