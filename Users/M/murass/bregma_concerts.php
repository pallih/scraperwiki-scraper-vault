<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.myspace.com/bregmaband/shows");           
$dom = new simple_html_dom();
$dom->load($html);

$eventsContainer = $dom->find('ul[class=eventsContainer]', 0);
foreach($eventsContainer->find('li[class=moduleItem]') as $event) {
    $entryDate = $event->find('div[class=entryDate]', 0);
    $month = $entryDate->find('span[class=month]', 0);
    $day = $entryDate->find('span[class=day]', 0);
    $details = $event->find('div[class=details]', 0);

    $record = array(
        'date' => $day->plaintext . " " . getMonthNumber($month->plaintext), 
        'location' => trim(preg_replace('!\s+!', ' ', $details->find('span[class=fn]', 0)->plaintext))
    );

    scraperwiki::save(array('date'), $record);
}

function getMonthNumber($month_name)
{
    $month_name = trim($month_name);

    $months = array();
    $months['Jan'] = "Styczeń";
    $months['Feb'] = "Luty";
    $months['Mar'] = "Marzec";
    $months['Apr'] = "Kwiecień";
    $months['May'] = "Maj";
    $months['Jun'] = "Czerwiec";
    $months['Jul'] = "Lipiec";
    $months['Aug'] = "Sierpień";
    $months['Sep'] = "Wrzesień";
    $months['Oct'] = "Październik";
    $months['Nov'] = "Listopad";
    $months['Dec'] = "Grudzień";

    return $months[$month_name];
}

?>