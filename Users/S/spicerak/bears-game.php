<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://espn.go.com/nfl/team/_/name/chi/chicago-bears");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[class=mod-container]') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://espn.go.com/nfl/team/_/name/chi/chicago-bears");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[class=mod-container]') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>
