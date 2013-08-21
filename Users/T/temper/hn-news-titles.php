<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://news.ycombinator.com/news");
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td.title a') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>