<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.hcsheriff.gov/cor/display.php?day=1");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('h3') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.hcsheriff.gov/cor/display.php?day=1");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('h3') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>