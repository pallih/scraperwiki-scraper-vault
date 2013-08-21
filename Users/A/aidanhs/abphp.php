<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
{
    # Store data in the datastore
    print $data . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>