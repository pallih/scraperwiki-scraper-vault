<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("https://my.usfirst.org/myarea/index.lasso?event_type=FRC");
print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td') as $data)
{
    print $data->plaintext . "\n";
}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

foreach($dom->find('td') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?><?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("https://my.usfirst.org/myarea/index.lasso?event_type=FRC");
print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td') as $data)
{
    print $data->plaintext . "\n";
}

# Then we can store this data in the datastore. Uncomment the following four lines and run
# the scraper again.

foreach($dom->find('td') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store.
?>