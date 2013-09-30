<?php
######################################
# This scraper tries to parse the paragraphs from
# http://www.thefoodtrust.org/php/headhouse/allmarkets/philadelphia.php
# (I'm sure there is a better way to do this, but the markup is pretty ambiguous)
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.thefoodtrust.org/php/headhouse/allmarkets/philadelphia.php");

// Use the PHP Simple HTML DOM Parser
$dom = new simple_html_dom();
$dom->load($html);

// The serendipity_title class only exists on the first <p> of the <td> we want to scrape, so we get its parent.
$first_paragraph = $dom->find('p.serendipity_title');
$table_cell = $first_paragraph[0]->parent;

$all_paragraphs = $table_cell->find('p');    // Get all of the <p> tags in the table cell.

// Loop through all of the paragraphs and only keep ones that have text
$non_empty_paragraphs = array();
foreach($all_paragraphs as $p) {
    $plaintext = trim($p->plaintext);
    if($plaintext != '&nbsp;' && $plaintext != '') {
        $non_empty_paragraphs[] = $p->outertext;
    }
}

// Kind of a convoluted way of abstracting the days away from the other <p> tags
$struct_data = array();
foreach($non_empty_paragraphs as $x) {
    if(strpos($x, 'serendipity_title') !== false) continue;    // We don't need the section title

    if(strpos($x,'Text-TheFoodTrust') !== false) {
        $the_day = strip_tags($x);
    } else {
        $struct_data[$the_day][] = $x;
    }
}

// This assoc array will represent a record in the db
$market = array();

foreach($struct_data as $day=>$markets) {
    $i = 0;

    // Every four elements in struct_data make up the information for one market.
    foreach($markets as $mkt) {
        switch($i%4) {
            case 0:
                $market['day'] = $day;
                $key_name = 'title';
                break;
            case 1:
                $key_name = 'address';
                break;
            case 2:
                $key_name = 'time';
                break;
            case 3:
                $key_name = 'status';
                break;

        }
        $market[$key_name] = strip_tags($mkt);

        // If we are on the last attribute of the market, there are some special things we need to do
        if($i%4 == 3) {
            // First, geocode the address of the market
            // I'm trying to handle the style of address that comes up a few times on this site. When the address is given as
            // something like "Wharton Street, between 29th and Hollywood streets" the geocoder can handle it. So I do a check 
            // for the word "between" and if its there, I change the [geocoder] address to "Wharton and 29th".
            $addy = $market['address'];
            if(strpos($addy, 'between') !== false) {
                $addy_parts = explode('and',$addy);
                $addy = trim(str_replace('between','and', $addy_parts[0]));
            } 
            $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($addy).',+Philadelphia,+PA&sensor=false&output=json';

            // Retrieve the URL contents
            $geodata = file_get_contents($geocode_url);

            // Parse the returned json
            $geo_json = json_decode($geodata);
            $latlng = ($geo_json->status != 'ZERO_RESULTS') ? $latlng = array($geo_json->results[0]->geometry->location->lat, $geo_json->results[0]->geometry->location->lng) : array('0.0','0.0');

            // Second, save the market record in the db.
            scraperwiki::save(array('title'), $market, date('Y-m-d h:i:s'), array($latlng[0] , $latlng[1]));

            // Clear the $market var
            $market = array();
        }
        $i++;
    }
}

?><?php
######################################
# This scraper tries to parse the paragraphs from
# http://www.thefoodtrust.org/php/headhouse/allmarkets/philadelphia.php
# (I'm sure there is a better way to do this, but the markup is pretty ambiguous)
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.thefoodtrust.org/php/headhouse/allmarkets/philadelphia.php");

// Use the PHP Simple HTML DOM Parser
$dom = new simple_html_dom();
$dom->load($html);

// The serendipity_title class only exists on the first <p> of the <td> we want to scrape, so we get its parent.
$first_paragraph = $dom->find('p.serendipity_title');
$table_cell = $first_paragraph[0]->parent;

$all_paragraphs = $table_cell->find('p');    // Get all of the <p> tags in the table cell.

// Loop through all of the paragraphs and only keep ones that have text
$non_empty_paragraphs = array();
foreach($all_paragraphs as $p) {
    $plaintext = trim($p->plaintext);
    if($plaintext != '&nbsp;' && $plaintext != '') {
        $non_empty_paragraphs[] = $p->outertext;
    }
}

// Kind of a convoluted way of abstracting the days away from the other <p> tags
$struct_data = array();
foreach($non_empty_paragraphs as $x) {
    if(strpos($x, 'serendipity_title') !== false) continue;    // We don't need the section title

    if(strpos($x,'Text-TheFoodTrust') !== false) {
        $the_day = strip_tags($x);
    } else {
        $struct_data[$the_day][] = $x;
    }
}

// This assoc array will represent a record in the db
$market = array();

foreach($struct_data as $day=>$markets) {
    $i = 0;

    // Every four elements in struct_data make up the information for one market.
    foreach($markets as $mkt) {
        switch($i%4) {
            case 0:
                $market['day'] = $day;
                $key_name = 'title';
                break;
            case 1:
                $key_name = 'address';
                break;
            case 2:
                $key_name = 'time';
                break;
            case 3:
                $key_name = 'status';
                break;

        }
        $market[$key_name] = strip_tags($mkt);

        // If we are on the last attribute of the market, there are some special things we need to do
        if($i%4 == 3) {
            // First, geocode the address of the market
            // I'm trying to handle the style of address that comes up a few times on this site. When the address is given as
            // something like "Wharton Street, between 29th and Hollywood streets" the geocoder can handle it. So I do a check 
            // for the word "between" and if its there, I change the [geocoder] address to "Wharton and 29th".
            $addy = $market['address'];
            if(strpos($addy, 'between') !== false) {
                $addy_parts = explode('and',$addy);
                $addy = trim(str_replace('between','and', $addy_parts[0]));
            } 
            $geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?address='.urlencode($addy).',+Philadelphia,+PA&sensor=false&output=json';

            // Retrieve the URL contents
            $geodata = file_get_contents($geocode_url);

            // Parse the returned json
            $geo_json = json_decode($geodata);
            $latlng = ($geo_json->status != 'ZERO_RESULTS') ? $latlng = array($geo_json->results[0]->geometry->location->lat, $geo_json->results[0]->geometry->location->lng) : array('0.0','0.0');

            // Second, save the market record in the db.
            scraperwiki::save(array('title'), $market, date('Y-m-d h:i:s'), array($latlng[0] , $latlng[1]));

            // Clear the $market var
            $market = array();
        }
        $i++;
    }
}

?>