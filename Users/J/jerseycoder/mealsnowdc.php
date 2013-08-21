<?php
######################################
# MealsNowDC - provides organization names, times and location data of kitchens offering meals to the homeless in DC
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://creatorexport.zoho.com/showRss.do?viewlinkId=3&fileType=rss&link=true&complete=true&sharedBy=dcfoodfinder");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('item') as $data)
{
    # Store data in the datastore
    #print $data->plaintext . "\n";
    $values = array(
        'title' => $data->'zc:organization',
        'link' => $data->'zc:resourceServices',
    );
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

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