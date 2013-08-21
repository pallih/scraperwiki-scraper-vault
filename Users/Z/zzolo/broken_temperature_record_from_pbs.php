<?php

// This scraper aims to create a machine readable feed
// from the PBS temperature record page:
// http://www.pbs.org/newshour/widgets/temp-records/historical/year_records.html          
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.pbs.org/newshour/widgets/temp-records/historical/year_records.html");
$dom = new simple_html_dom();
$dom->load($html);

$count = 0;
foreach($dom->find("table tr") as $rows) {
    $count++;

    $data = $rows->find("td");
    if (!empty($data[3]->plaintext) && $count > 1) {
        $record = array(
            'id' => $data[5]->plaintext . '--' . str_replace(' ', '-', $data[0]->plaintext),
            'station_name' => $data[0]->plaintext,
            'county' => $data[1]->plaintext,
            'state' => $data[2]->plaintext,
            'record' => $data[3]->plaintext,
            'previous_record' => $data[4]->plaintext,
            'record_date' => $data[5]->plaintext,
            'previous_record_date' => $data[6]->plaintext,
            'timestamp' => time(),
        );

        scraperwiki::save(array('id'), $record);
    }
}

?>
