<?php
// Get the page.
$html = scraperwiki::scrape("http://www.seattlefoundation.org/npos/Pages/default.aspx");

// Put the page into dom.
require  'scraperwiki/simple_html_dom.php';



$dom = new simple_html_dom();
$dom->load($html);

$i = 0;
$record = array();
foreach($dom->find('table#cbqwp tr td div.link-item') as $row) {

    if ($i < 5){
        print_r($row->children[0]);
        $record['url'] = $row->children[0]->attr['href'];
    }
    // Store data in the datastore

    // scraperwiki::save(array('name','link', 'contact', 'location'), $record);
    $i++;
}


?>
