<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.tvrage.com/shows/id-5820/printable?nogs=1&nocrew=1&season=1");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div p') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
    
}
foreach($dom->find('h1 a') as $data2)
{
    # Store data in the datastore
    print $data2->plaintext . "\n";
    
    scraperwiki::save(array('data3'), array('data3' => $data2->plaintext));
    
}

$i = 1;
foreach ($data2 as $title)
{
    print $title->plaintext;
    print $data[$i]->plaintext;
    $i = $i + 1;
print $i;
}
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.tvrage.com/shows/id-5820/printable?nogs=1&nocrew=1&season=1");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div p') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
    
}
foreach($dom->find('h1 a') as $data2)
{
    # Store data in the datastore
    print $data2->plaintext . "\n";
    
    scraperwiki::save(array('data3'), array('data3' => $data2->plaintext));
    
}

$i = 1;
foreach ($data2 as $title)
{
    print $title->plaintext;
    print $data[$i]->plaintext;
    $i = $i + 1;
print $i;
}
?>