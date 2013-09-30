<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.cityofboston.gov/government/citydept.asp");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div.content_main_sub a') as $data)
{
    # Store data in the datastore
    $values = array(
        'title' => $data->plaintext,
        'link' => $data->href,
    );

    scraperwiki::save(array('title'), $values);
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.cityofboston.gov/government/citydept.asp");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div.content_main_sub a') as $data)
{
    # Store data in the datastore
    $values = array(
        'title' => $data->plaintext,
        'link' => $data->href,
    );

    scraperwiki::save(array('title'), $values);
}

?>