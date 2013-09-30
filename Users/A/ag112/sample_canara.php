<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://jobsearch.naukri.com/mynaukri/mn_newsmartsearch.php?js=1&xz=1_0_5&qp=websphere&ql=ncr%2Cchandigarh&farea=Select&qf%5B%5D=&qe=&qm=-1&uen=&usl=&fsug=");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
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

$html = scraperwiki::scrape("http://jobsearch.naukri.com/mynaukri/mn_newsmartsearch.php?js=1&xz=1_0_5&qp=websphere&ql=ncr%2Cchandigarh&farea=Select&qf%5B%5D=&qe=&qm=-1&uen=&usl=&fsug=");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>