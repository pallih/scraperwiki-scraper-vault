<?php

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=data+mining") ;
#print $html;


$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}


?>
