<?php

// This scraper gets all the Minnesota Pollution Control Agency
// facilities as listed in the Environmental Data Access DB.
require 'scraperwiki/simple_html_dom.php';

$url = "http://cf.pca.state.mn.us/data/edaAir/pointList.cfm";
$html = scraperwiki::scrape($url);

// Parse Dom
$dom = new simple_html_dom();
$dom->load($html);
$count = 0;

// There is only one table with no identifiying attributes.
foreach($dom->find("table[id=smalltable] tr") as $rows) {
    $count++;

    // First row is header
    $data = $rows->find("td");
    if ($count > 1) {
        // Massage
        $link = $data[0]->find('a', 0);
        $href = isset($link->href) ? 'http://cf.pca.state.mn.us/data/edaAir/' . $link->href : '';

        // Create record
        if (!empty(trim($data[0]->plaintext))) {
            $record = array(
                'permit_id' => trim($data[0]->plaintext),
                'permit_url' => $href,
                'facility_name' => $data[1]->plaintext,
                'city' => $data[2]->plaintext,
                'county' => $data[3]->plaintext,
                'timestamp' => time(),
            );
            scraperwiki::save(array('permit_id'), $record);
        }
    }
}

?>
