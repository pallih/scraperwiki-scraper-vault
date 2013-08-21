<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.example.com");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
//$dom = new simple_html_dom();
//$dom->load($html);

//foreach($dom->find('td') as $data)
//{
//    # Store data in the datastore
//    print $data->plaintext . "\n";
//    scraperwiki::save(array('data'), array('data' => $data->plaintext));
//}



?>