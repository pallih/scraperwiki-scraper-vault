<?php
//Want a list of all the medal events? Me too! This does that.

require 'scraperwiki/simple_html_dom.php';

 /* the following is a manual scrape of http://www.london2012.com/schedule-and-results/ because LOCOG's webmaster's a bastard. */

$html = file_get_html('http://dev.aendrew.com/2012_schedule.html');

/* $sports = $html->find('div.sN a');

foreach ($sports as $sport)
    $sports_list[] = $sport->plaintext;
$i = 0;
foreach($html->find('div[class=barWrap]') as $key => $days) {
   */
    foreach($html->find('span[class=medalday]') as $day) {
        $sport = preg_replace('#^\/(([a-z]|-)+)\/.*$#', '$1', $day->parent()->href);
        $text = $day->plaintext;
        $lines = explode("\n", $text);
        $day_bits = explode(" ", $lines[0] . ' 2012');
        $day = $day_bits[1] . ' ' . $day_bits[0] .  ' ' . $day_bits[2]; 
        $day = strtotime($day);
        unset($lines[0]);
        unset($lines[1]);
        $final[$sport][$day][] = $lines;
    }
//}

print_r($final); exit;
foreach($final as $key => $sport){
    foreach ($sport as $key2 => $day) {
        foreach ($day as $events) 
        {
            foreach ($events as $event) {
                if (!empty($event) && !empty($key2)){
                    $write[] = array(
                        "id" => (integer) '',
                        "sport" => ucfirst($key),
                        "event" => $event,
                        "date" => date("Y-m-d", $key2)
                    );
                    
                }
            }
        }
    }
}
$write = array_map("unserialize", array_unique(array_map("serialize", $write)));
//print_r($write);
//for ($i = 0; $i < count($write); $i++) {
$i = 0;
foreach($write as $stuff) {
       if (empty($stuff['event'])) {
        unset($stuff); }
    else {
   $stuff['id'] = $i + 1; 
    $rows[] = array(
        "id" => (integer) $stuff['id'],
        "sport" => (string) $stuff['sport'],
        "event" => (string) $stuff['event'],
        "date" => (string) $stuff['date'],
    );
    }
    $i++;
}

//print_r($rows);


scraperwiki::save_sqlite(array("id"), $rows);
?>