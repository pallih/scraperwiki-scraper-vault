<?php

# from: JS / List of UK railway station locations 
# http://scraperwiki.com/scrapers/list_of_uk_railway_station_locations/

$domain = 'http://www.nationalrail.co.uk';

# Get the page into the DOM
require 'scraperwiki/simple_html_dom.php';           
$html = scraperWiki::scrape($domain . '/stations/codes/');           
$dom = new simple_html_dom();
$dom->load($html);

# Load postcode database to avoid HTTP calls
//scraperwiki::attach("uk_postcodes_from_codepoint", "ukp");

# Loop through each row in the table
$i = 0;
$rows = $dom->find("table[@border='1'] tr");
foreach($rows as $row){
    $i++;
    if ($i == 1) {continue;} // Skip <thead> row
    $cols = $row->find('td');

    # Determine the URL of the linked page (e.g. the info for 'WRK'
    $href = html_entity_decode($row->find('a', 0)->href);
    $url = $domain . $href;
    
    # Get the postcode from the linked page
    $html2 = scraperWiki::scrape($url);
    $dom2 = new simple_html_dom();
    $dom2->load($html2);
    $address = trim ($dom2->find('address', 0)->plaintext);
    $lines = explode ("\n", $address);
    $postcode = trim (array_pop ($lines));
    
    # Convert postcode to lat/lon
    list ($lat, $lng) = scraperwiki::gb_postcode_to_latlng($postcode);
    //$postcodeTrimmed = str_replace (' ', '', $postcode);
    //$latlng = scraperwiki::select("* from ukp.swdata where postcode='{$postcodeTrimmed}';");
    
    # Assemble the record
    $station = array(
        'code' => trim ($cols[1]->plaintext),
        'name' => html_entity_decode (trim ($cols[0]->plaintext)),
        'postcode' => $postcode,
        'latitude' => $lat,
        'longitude' => $lng,
        //'address' => $address,
        'url' => $url,
    );
    
    # Save the record
    scraperwiki::save(array('code'), $station);
    print_r ($record);
    
    # Limit while testing
    //if ($i == 10) {break;}
}

/*
    Useful pages:
    http://scraperwiki.com/scrapers/swansea_food_safety_inspections_1/edit/
    http://scraperwiki.com/docs/php/php_intro_tutorial/
    http://scraperwiki.com/docs/php/php_help_documentation/
    http://scraperwiki.com/views/postcode_and_geo_cheat_sheet/edit/
*/

?>