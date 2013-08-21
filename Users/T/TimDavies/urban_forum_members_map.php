<?php

# Blank PHP
$xml = scraperWiki::scrape("http://www.urbanforum.org.uk/map.php");

$dom = simplexml_load_string($xml);

foreach($dom->marker as $marker) {
    unset($entry);
    foreach($marker->attributes() as $attribute => $value) {
        $entry[(string)$attribute] = str_replace("#","",strip_tags((string)$value));
    }

    print_r($entry);
    scraperwiki::save_sqlite(array('name'), $entry);
}


?>
