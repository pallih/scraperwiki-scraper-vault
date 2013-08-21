<?php
######################################
# Basic PHP scraper
######################################

require 'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.bbc.co.uk/radio4/factual/desertislanddiscs_archive.shtml");

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('a') as $data)
{
    # Store data in the datastore
    if (preg_match("#^/radio4/factual#", $data->href, $matches)) {
        preg_match("#^/radio4/factual/desertislanddiscs_(\d{8}).shtml#", $data->href, $matches)
        print $data->href . "\n";
        print $matches . "\n";
    }

    #print $data->plaintext . "\n\n";
    # scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>