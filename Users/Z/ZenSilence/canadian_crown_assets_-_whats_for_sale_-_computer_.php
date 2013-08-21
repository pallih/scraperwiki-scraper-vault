<?php
######################################
# Canadian Crown Assets - [What's for Sale] - Computer Equipment, Parts and Accessories
# Written by: Zen_Silence
######################################

function grabData($haystack, $start, $end) {
    return trim(html_entity_decode(substr($haystack, (strpos($haystack, $start)+strlen($start)+1), (strpos($haystack, $end) - strlen($start) - 1 - strpos($haystack, $start)))));
}

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://crownassets.pwgsc.gc.ca/mn-eng.cfm?&snc=wfsav&sc=ach-shop&str=1&rpp=25&sr=1&sf=aff-post&so=DESC&vndsld=0&lci=&srchtype=&hpcs=7000&hpsr=");

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[class=width68 floatLeft]') as $data) {    
    scraperwiki::save(array('Item'), 
            array('Item' => grabData($data->plaintext, "Item", "Posted"),
                  'Posted' => grabData($data->plaintext, "Posted", "Closing"),
                  'Closing' => grabData($data->plaintext, "Closing", "Remaining"),
                  'Remaining' => grabData($data->plaintext, "Remaining", "Location "),
                  'Location' => grabData($data->plaintext, "Location ", "Sale Account")
                 ));
}

?>