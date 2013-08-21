<?php
######################################
# SJ Station Situation scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$stationIDs = array('cst','g', 'lp', 'nr', 'm', 'sk'); // TODO: Add dynamic list of stations

foreach ($stationIDs as $station) {
    $stationID = $station;
    $theURL = "http://www5.trafikverket.se/trafikinformation/WebPage/TrafficSituationCity.aspx?JF=11&station=74," . $stationID . "&arrivals=0&nostat=1";
    print("Scraping " . $stationID . "\n");
    scrapeURL($theURL, "#TrafficSituationCityComponent_trafficSituationDepartureDataGrid", $stationID);
}
            

function scrapeURL($pageURL, $tableName, $stationID) {
    $html = scraperwiki::scrape($pageURL);
    $dom = new simple_html_dom();
    $dom->load($html);

    $newurl = $dom->find("a");
    $newhref = get_href($newurl[0]);

    # URL found, fetch it
    if ($newhref != "") {
        
        $html = scraperwiki::scrape(html_entity_decode($newhref));
        $dom->load($html);

        # parse it
        $grid = $dom->find($tableName,0 );

        scrapeTable($grid, $stationID);
    }
}

# Support functions


function scrapeTable($inputGrid, $stationID) {


    $entries = $inputGrid->find("tr");
    $rowCount = 0;
    
    foreach ($entries as $entry) {

        $trainDepartureTime = "";
        $isDeviationInDeparture = "";
        $trainDeviatingDepartureTime = "";
        $trainName = ""; 
        $trainLink = "";
        $trainDestination = "";
        $trainOperatorName = "";
        $trainOperatorLink = "";
        $trainCurrentState = "";
        $trainCurrentStatePlace = "";
        $trainDeviationInMinutes = "";
        $trainDeviationType = "";
        $trainType = "";
        $trainTrack = "";

                
        $cells = $entry->find("td");
        $colCount = 0;
        if ($rowCount > 0)
        foreach ($cells as $cell) {

            $divs = $cell->find("div");
            $divCount = 0;
            $isDeviationInDeparture = false;
            foreach ($divs as $div) {

                $data = strip_tags_attributes($div, '<a>', 'href' );
                
                if ($colCount == 0) {
                    if ($divCount == 0) {
                        $trainDepartureTime = $data;
                        # print("Ordinarie avgångstid: " . $trainDepartureTime);
                    }
                    if ($divCount == 1) {
                        if ($data == "Avgick") {
                            $isDeviationInDeparture = true;
                        } else {
                            $isDeviationInDeparture = false;
                        }
                    }
                    if ( ($divCount == 2) && ($isDeviationInDeparture==true) ) {
                        $trainDeviatingDepartureTime = $data;
                        # print("\nAvgick: ". $data);
                    }
                }
    
                if ($colCount == 1) {

                    // 1. Tåg nr + länk
                    if ($divCount == 0) {
                        $trainLink = get_href($data);
                        $trainName = str_replace(" till", "", strip_tags(fix_chars($data)));
                        $trainName = str_replace("Tåg nr ", "", $trainName);
                        # print("Tåg nr: ". $trainName);
                    }
                    // 2. Destination
                    if ($divCount == 1) {
                        $trainDestination = fix_chars($data);
                        # print(" Till: " . $trainDestination );
                    }
                    // 3. Operatör + länk
                    if ($divCount == 2) {
                        $trainOperatorLink = get_href($data);
                        $trainOperatorName = fix_chars(trim(strip_tags($data)));  
                        # print (" Operatör: " . $trainOperatorName . " (" . $trainOperatorLink . ")" );
                    }
                }

                if ($colCount == 2) {
                    // Tåg som just passerat / ankommit
                    if ($divCount == 0) {
                        if (strpos($data, "Ankom")) {
                            $trainCurrentState = "ARRIVED";
                            $trainCurrentStatePlace = str_replace("Ankom ", "", fix_chars($data));
                        } else {
                            $trainCurrentState = "PASSED";
                            $trainCurrentStatePlace = str_replace("Passerade ", "", fix_chars($data));
                        }
                        # print("--> " . $trainCurrentState . " " . $trainCurrentStatePlace );
                    }
                    // Avvikelse i minuter
                    if ($divCount == 1) {
                        if (strpos($data, "tidig")) {
                            $trainDeviationInMinutes = str_replace(" min tidig", "", fix_chars($data));
                            $trainDeviationType = "EARLY";
                        } else {
                            $trainDeviationInMinutes = str_replace(" min försenad", "", fix_chars($data));
                            $trainDeviationType = "EARLY";
                        }
                        # print(" (" . $trainDeviationInMinutes . " " . $trainDeviationType . ")");
                        
                    }
                }

                if ($colCount == 3) {
                    // Hämta tågtyp
                    if ($divCount == 0) {
                        $trainType = fix_chars($data);
                        # print("Tågtyp: " . $trainType);
                    }
                }

                if ($colCount == 4) {
                    if ($divCount == 0) {
                        $trainTrack = trim($data);
                        # print("Spår: " . $data);
                    }
                }
                
                $divCount++;
            }

            # print("\n");
            $colCount++;
        }

        // trainDepartureTime, isDeviationInDeparture, trainDeviatingDepartureTime
        // trainName, trainLink, trainDestination, trainOperatorName, trainOperatorLink, 
        // trainCurrentState, trainCurrentStatePlace
        // trainDeviationInMinutes, trainDeviationType
        // trainType, trainTrack
        

        $dataset = array( 
                        'StationID' => $stationID,
                        'Avgång' => $trainDepartureTime,
                        'Avvikelse' => $isDeviationInDeparture,
                        'AvvikelseAvgång' => $isDeviationInDeparture,
                        'TågNamn' => $trainName,
                        'TågLänk' => $trainLink,
                        'Destination' => $trainDestination,
                        'Operatör' => $trainOperatorName,
                        'OperatörLänk' => $trainOperatorLink,
                        'Aktuellt' => $trainCurrentState,
                        'AktuelltPlats' => $trainCurrentStatePlace,
                        'AvvikelseMinuter' => $trainDeviationInMinutes,
                        'AvvikelseTyp' => $trainDeviationType,
                        'TågTyp' => $trainType,
                        'Spår' => $trainTrack
                        ) ;
        if ($rowCount > 0) {
            scraperwiki::save( array('Avgång', 'TågNamn'), $dataset );
            #print("Tågnamn : " . $trainName);
        }

        #print( "\n" );
        $rowCount++;
    }

}

function strip_tags_attributes($string,$allowtags=NULL,$allowattributes=NULL){ 
    $string = strip_tags($string,$allowtags); 
    if (!is_null($allowattributes)) { 
        if(!is_array($allowattributes)) 
            $allowattributes = explode(",",$allowattributes); 
        if(is_array($allowattributes)) 
            $allowattributes = implode(")(?<!",$allowattributes); 
        if (strlen($allowattributes) > 0) 
            $allowattributes = "(?<!".$allowattributes.")"; 
        $string = preg_replace_callback("/<[^>]*>/i",create_function( 
            '$matches', 
            'return preg_replace("/ [^ =]*'.$allowattributes.'=(\"[^\"]*\"|\'[^\']*\')/i", "", $matches[0]);'    
        ),$string); 
    } 
    return $string; 
} 

function fix_chars( $str ) {
    $str = str_replace("Ã¥", "å", $str);
    $str = str_replace("Ã¤", "ä", $str);
    $str = str_replace("Ã", "Ö", $str);
    $str = str_replace("Ö¶", "ö", $str);
    $str = str_replace("&#246;", "ö", $str);
    $str = str_replace("&#228;", "ä", $str);
    $str = str_replace("&#229;", "å", $str);
    $str = str_replace("&#196;", "Ä", $str);
    $str = str_replace("&#214;", "Ö", $str);
    $str = str_replace("&#197;", "Å", $str);

    return $str;
}

function get_href($inputString) {
    if (preg_match('/href="([^"]*)"/i', $inputString , $regs))
    {
        $result = $regs[1];
    } else {
        $result = "";
    }
    return $result ;
}

?>