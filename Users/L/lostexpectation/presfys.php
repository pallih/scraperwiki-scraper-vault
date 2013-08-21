<?php

require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Europe/Dublin');

// Get the most recently scraped date from the DB
$max = scraperwiki::select('date FROM swdata ORDER by date DESC LIMIT 1');
// If none start in 1997
if(!$max) $max = strtotime('2000-01-01');
else {
    $max = strtotime($max[0]['date']);
    $year = date('Y',$max);
    if($year < date('Y')) $year++;
    $max = strtotime($year.'-01-01');
}

echo 'Scraping engagements from '.date('Y',$max)."\n";

// Scrape the page with the list of weeks for that year
$html = scraperwiki::scrape('http://president.ie/index.php?section=6&lang=eng&year='.date('Y',$max));

//Fetch all the week IDs
preg_match_all('/engagement=([0-9]{5,7})/',$html,$dates);

// Fetch all the week start dates
preg_match_all('|Week beginning ([a-z0-9 ]{10,30})</a>|i',$html,$first);

// Work from the start of the year forwards to today
krsort($dates[1]);

// Loop through the weeks and scrape pages
foreach($dates[1] as $key => $week) {
    // Make week beginning date into unix time
    $f = strtotime($first[1][$key]);
    // Deduce if this is new information
    if($max < $f) {
        // Scrape the engagements from the given week
        $html = scraperwiki::scrape('http://president.ie/index.php?section=6&engagement='.$week.'&lang=eng');
        // Remove annoying tabs, newlines etc
        $html = preg_replace('/\s+/',' ',$html);

#####


}

function save_data($data) {
    if(isset($data['date'])) {
     
            scraperwiki::save_sqlite(array('id','title'),$data);
            echo "\t".$data['time'].': '.$data['place'].' / '.$data['info']."\n";
            return true;
        } else return false;
    } else return false;
}
?>
