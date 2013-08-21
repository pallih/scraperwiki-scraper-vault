<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

// Set up some variables.  We only get a hundred records for example purposes
$start_id = 194314;
$end_id = 194316;
$month = 01;
$year = 2011;
$base_link = 'http://www2.cityofseattle.net/util/services/calendar/DrawCalender.asp';
// Example: http://www2.cityofseattle.net/util/services/calendar/DrawCalender.asp?PC=194414&Month=7&FC=A&D=6
$empty_page = 'no records';

// Define types array
$types = array(
    'images/leafrecyclegarbagecal.gif' => 'Leaf, Recycling, Garbage',
    'images/leafgarbagecal.gif' => 'Leaf, Garbage',
    'images/garbagecal.gif' => 'Garbage',
    'images/leafrecyclecal.gif' => 'Leaf, Recycling',
);

$id = 0;
for ($i = $start_id; $i <= $end_id; $i++) {
    // Get the page for the day
    $query_string = '?PC=' . $i . '&Month=' . $month . '&FC=A&D=6';
    $url = $base_link . $query_string;
    $html = scraperwiki::scrape($url);

    $record = array();
    if (trim($html) != $empty_page) {
        $record['id'] = $id;
        $dom = new simple_html_dom();
        $dom->load($html);
    
        // Get address
        $address_dom = $dom->find('table#Table2 tr td[width="540"] font');
        $record['address'] = custom_clean(str_replace('Service Address:', '', $address_dom[0]->plaintext));

        // Find date
        $days_dom = $dom->find('table#Table3 tr td[width="14.28%"] font');
        foreach ($days_dom as $day_dom) {
            // Check for image
            $image_dom = $day_dom->find('img');
            if (!empty($image_dom[0])) {
                $record['date'] = $year . '-' . $month . '-' . $day_dom->plaintext;
                $record['type'] = $types[$image_dom[0]->src];
                scraperwiki::save(array('id'), $record);
                $id += 1;
            }
        }
    }
}

/**
 * Function to clean up strings
 */
function custom_clean($value) {
    return trim(str_replace('&nbsp;', ' ', $value));
}
?>