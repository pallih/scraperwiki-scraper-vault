<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$links = array();

# 216 is the current total items past the last page of hotdocs listings
for($i = 0; $i < 225; $i = $i + 12)
{
    if($i == 0){
        $html = scraperwiki::scrape("http://www.hotdocs.ca/film/title/all");
    } else {
        $html = scraperwiki::scrape("http://www.hotdocs.ca/film/title/all/P" . $i . "/");
    }
    #print $html;
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

    #foreach($dom->find('td.desc')->find('h3')->find('a') as $data)
    foreach($dom->find('td.desc') as $data)
    {
        #print $data->plaintext . "\n";
        #print $data->first_child() . "\n";
        print $data->first_child()->first_child()->href . "\n";
        $link = $data->first_child()->first_child()->href;
        array_push($links, $link);
    }
}

print count($links);

# Store data in the datastore
print_r($links);
#scraperwiki::save($dom->find('td.desc'),array('links'));

?>