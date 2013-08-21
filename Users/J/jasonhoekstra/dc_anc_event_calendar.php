<?php

require 'scraperwiki/simple_html_dom.php';

$year = '2012';

$results = array();

for ($month = 1; $month <= 12; $month++) {
    $html_content = scraperwiki::scrape('http://app.calendar.rrc.dc.gov/monthView.aspx?thisDate='.$month.'/1/'.$year.'&cdlCalendars=44');
    $html = str_get_html($html_content);
    
    foreach ($html->find("div#whitebox1 table td a") as $link) { 
        $title = $link->title;
        $url = $link->href;
        if (substr($title, 0, 3) == 'ANC') {
            $thisdate_start_pos = strpos($url, 'thisDate=');
            $thisdate_end_pos = strpos($url, '&', $thisdate_start_pos);
            $event_date = substr($url, $thisdate_start_pos + 9, $thisdate_end_pos - $thisdate_start_pos - 9);
            $event_date = str_replace('.', '/', $event_date);

            $anc_end_pos = strpos($title, ' ', 5);
            $anc = substr($title, 4, $anc_end_pos - 4);

            $result = array();
            $result['event_title'] = $title;
            $result['event_url'] = $url;
            $result['event_date'] = $event_date;
            $result['anc'] = $anc;
            $results[] = $result;
        }
    }
}

// print json_encode($results);

scraperwiki::save_sqlite(array('event_url'), $results);

?>
