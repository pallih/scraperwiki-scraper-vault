<?php

######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


for ($i = 0; $i <= 19; $i++) {

$html = scraperwiki::scrape("http://www.museumsportal-berlin.de/museen/mp/$i.html");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[class=museums-liste] ul li a') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
}
 

?><?php

######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


for ($i = 0; $i <= 19; $i++) {

$html = scraperwiki::scrape("http://www.museumsportal-berlin.de/museen/mp/$i.html");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[class=museums-liste] ul li a') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
}
 

?>