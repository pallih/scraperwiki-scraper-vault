<?php
// A scraper for airline information from PHL.org

require "scraperwiki/simple_html_dom.php"; 

// Base URL for PHL flight info.
define("BASE_URL", "http://www.phl.org/cgi-bin/fidscooltext.pl");

// Get rid of whitespace and spaces
function removeSpaces($text) {
    return trim(str_replace("&nbsp;", "", $text));
}

// Save a record to the data store.
function saveData($unique, $flight_data) {
      scraperWiki::save_sqlite($unique, $flight_data);
}

// Scrape the HTML from the page.
function scrapeHTML($param, $type) {
    
    $html = scraperWiki::scrape("http://www.norwegian.no/fly/lavpris/?D_City=CPH&A_City=DUB&TripType=2&D_Day=1&D_Month=201104&R_Day=1&R_Month=201104&AdultCount=1&ChildCount=0&InfantCount=0");
    $dom = new simple_html_dom(); 
    $dom->load($html);
    
    // Iterate over table rows and get flight details.
    foreach($dom->find("TR[@HEIGHT='25']") as $data){ 
    
        // Flight details.
        $tds = $data->find("div");
    
        $airline = removeSpaces($tds[0]->plaintext);
        $flight_type = $type;
        $flight_num = removeSpaces($tds[1]->plaintext);
        $destination = removeSpaces($tds[2]->plaintext);
        $time = removeSpaces($tds[3]->plaintext);
        $gate = removeSpaces($tds[4]->plaintext);
        $remarks = removeSpaces($tds[5]->plaintext);
    
        // Skip header row. Cheesy, but effective.
        if($airline == "Airline") {
            continue;
        }
    
        // Set the date.
        $date = date("m.d.y");
    
        // Build up record to store.
        $flight_data = array("date"=>$date, 
                             "airline"=>$airline,
                             "flight_type" => $flight_type,
                             "flight_num"=>$flight_num, 
                             "destination"=>$destination, 
                             "time"=>$time, "gate"=>$gate, 
                             "remarks"=>$remarks
                            );
    
        // Save the record.
        saveData(array("date", "airline", "flight_type", "flight_num"), $flight_data);
        
    }

    $dom->clear();

}

// Departures.
scrapeHTML("dflno", "DEPARTURE");

// Arrivals.
scrapeHTML("aflno", "ARRIVAL");


?>
