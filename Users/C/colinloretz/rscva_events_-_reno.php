<?php

require 'scraperwiki/simple_html_dom.php';           

$html = scraperWiki::scrape("http://www.visitrenotahoe.com/reno-tahoe/what-to-do/events");           

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("#results-body .results-content h4 a") as $data){
    $record = array(
        'event' => $data->plaintext, 
        'event_url' => $data->href
    );
    scraperwiki::save(array('event'), $record);    
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';           

$html = scraperWiki::scrape("http://www.visitrenotahoe.com/reno-tahoe/what-to-do/events");           

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("#results-body .results-content h4 a") as $data){
    $record = array(
        'event' => $data->plaintext, 
        'event_url' => $data->href
    );
    scraperwiki::save(array('event'), $record);    
}


?>
