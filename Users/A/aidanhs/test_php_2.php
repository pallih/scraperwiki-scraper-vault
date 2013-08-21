<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("https://scraperwiki.com/hello_world.html");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $td)
{
    # Store data in the datastore
    print $td . "\n";
    scraperwiki::save(array('td'), array('td' => $td->plaintext));
}

?>
