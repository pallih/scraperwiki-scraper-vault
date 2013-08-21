<?php
    
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$url = "http://www.standardzilla.com/contact/";
$html = scraperwiki::scrape($url);
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('body') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>