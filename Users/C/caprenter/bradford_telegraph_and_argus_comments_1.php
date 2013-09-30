<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$url = scraperwiki::scrape("http://gfweb-dev.cloudapp.net/en/IATI/Index");
#print $url;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($url);
echo count($dom->find('div.containerLarge'));
//die;

foreach($dom->find('div.containerLarge') as $html)
{
    foreach($html->find('a') as $element) {
        $link =  "http://gfweb-dev.cloudapp.net" . $element->href;         
    


    scraperwiki::save(array('link'), array('link' => $link));
    }
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$url = scraperwiki::scrape("http://gfweb-dev.cloudapp.net/en/IATI/Index");
#print $url;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($url);
echo count($dom->find('div.containerLarge'));
//die;

foreach($dom->find('div.containerLarge') as $html)
{
    foreach($html->find('a') as $element) {
        $link =  "http://gfweb-dev.cloudapp.net" . $element->href;         
    


    scraperwiki::save(array('link'), array('link' => $link));
    }
}

?>