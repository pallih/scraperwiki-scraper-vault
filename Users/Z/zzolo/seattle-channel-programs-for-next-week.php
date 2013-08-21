<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

// Set up some variables
$current_time = time();
$current_date = date('d-m-Y');
$day_interval = (60 * 60 * 24);
$days_forward = 7;
$program_link_base = 'http://www.seattlechannel.org/schedule/';

// Define headers/fields
$headers = array();
$headers[] = 'id';
$headers[] = 'timestamp';
$headers[] = 'program_date';
$headers[] = 'program';
$headers[] = 'time';
$headers[] = 'link';

$id = 0;
for ($i = 0; $i <= $days_forward; $i++) {
    // Get the page for the day
    $data_string = date('d-m-Y', $current_time + ($day_interval * $i));
    $url = "http://www.seattlechannel.org/schedule/default.asp?whichDay=" . $data_string;
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    // This is the most accurate way to get the fields, but we only
    // want to do two at a time.
    $set = 0;
    foreach($dom->find('td.channelText') as $data) {
        if ($set % 2 == 0) {
            $time = custom_clean($data->plaintext);
            $record = array();
        }
        else {
            $link = $data->find('a');
            $record = array(
                'id' => $id,
                'timestamp' => $current_time,
                'program_date' => $data_string,
                'program' => custom_clean($link[0]->plaintext),
                'time' => $time,
                'link' => $program_link_base . $link[0]->href,
            );
            scraperwiki::save(array('id'), $record);
            $time = '';
            $id += 1;
        }
        $set += 1;
    }
}


/**
 * Function to clean up strings
 */
function custom_clean($value) {
    return trim(str_replace('&nbsp;', ' ', $value));
}
?>