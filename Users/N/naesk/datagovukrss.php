<?php

$html = scraperWiki::scrape("http://data.gov.uk/data/%2A/rss.xml");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("//channel/item") as $data){
    $postTitle = $data->find("/title");
    $record = array(
        'postT' => $postTitle[0]->plaintext, 
    );
        //print_r($record);
        scraperwiki::save(array('postT'), $record);

}

?>
<?php

$html = scraperWiki::scrape("http://data.gov.uk/data/%2A/rss.xml");           
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("//channel/item") as $data){
    $postTitle = $data->find("/title");
    $record = array(
        'postT' => $postTitle[0]->plaintext, 
    );
        //print_r($record);
        scraperwiki::save(array('postT'), $record);

}

?>
