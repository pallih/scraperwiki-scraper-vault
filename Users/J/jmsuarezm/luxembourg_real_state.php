<?php
require 'scraperwiki/simple_html_dom.php';
ini_set('max_execution_time', 600);
setlocale(LC_ALL, 'fr_FR.UTF8');

//the firt time, we set manually the first page
$value = "/recherche/resultats/map/Centre/tr/by";
//if $value is a valid page
while ($value != "") {
    $htmlCentre = scraperWiki::scrape("http://www.athome.lu" . $value);
    $domCentre = new simple_html_dom();
    $domCentre->load($htmlCentre);
    //find the announces in the current page and store the records
    findAnnounces ($domCentre);
    //look for the next page link
    $value = "";
    foreach($domCentre->find('.next') as $data){
        $value = $data->href;
    }
}

/***************** Functions *********************/
function findAnnounces($strDataDom){
    //for each page, there are up to 10 records, each of them marked with DOM class 'plus'
    foreach($strDataDom->find('.plus') as $data){
        $value = $data->href;
        //is it a valid URL for an announce?
        if (strrpos ($value , "www.athome.lu/")){
            //go into the announce
            $htmlContent = scraperWiki::scrape($value);
            //look for the start of the json record wich has all the information of the announce
            //and manually trim it to the correct json format
            $strStart = strpos($htmlContent, "initGoogleMap");
            $strEnd = strpos($htmlContent, "#containerGoogleMap");
    
            $strData = substr ($htmlContent, $strStart, $strEnd - $strStart - 6);     
            $strData = ltrim($strData, "initGoogleMap([");
            //is it UTF format? just in case we convert it   
            $strDataUTF = iconv('UTF-8', 'ASCII//TRANSLIT', $strData);
            //the function will transfor the string into a json object and store it in the database
            storeJson($strDataUTF);
        }
    }
}

/*************************************************/
function storeJson($strData){
    $record=array(); 
    //decode the string
    $jsonVar = json_decode($strData);
    //if the decode ended with no error
    if (json_last_error() === JSON_ERROR_NONE) { 
        $record["id"] = $jsonVar -> id;
        $record["modifdate"] = $jsonVar -> modifdate;
        $record["inserted"] = $jsonVar -> inserted;
        $record["immotype"] = $jsonVar -> immotype;
        $record["price"] = $jsonVar -> price;
        $record["commission"] = $jsonVar -> commission;
        $record["location"] = $jsonVar -> location;
        $record["country"] = $jsonVar -> country;
        $record["region"] = $jsonVar -> region;
        $record["address"] = $jsonVar -> address;
        $record["postal_code"] = $jsonVar -> postal_code;
        $record["floor"] = $jsonVar -> floor;
        $record["surface"] = $jsonVar -> surface;
        $record["ground_surface"] = $jsonVar -> ground_surface;
        $record["superficieTerrain"] = $jsonVar -> superficieTerrain;
        $record["bedrooms_num"] = $jsonVar -> bedrooms_num;
        $record["carparks_num"] = $jsonVar -> carparks_num;
        $record["garages_num"] = $jsonVar -> garages_num;
        $record["open_kitchen"] = $jsonVar -> open_kitchen;
        $record["cellar"] = $jsonVar -> cellar;
        $record["attic"] = $jsonVar -> attic;
        $record["bathrooms_num"] = $jsonVar -> bathrooms_num;
        $record["bathroom"] = $jsonVar -> bathroom;
        $record["shower_room"] = $jsonVar -> shower_room;
        $record["separate_toilet"] = $jsonVar -> separate_toilet;
        $record["swimming_pool"] = $jsonVar -> swimming_pool;
        $record["sauna"] = $jsonVar -> sauna;
        $record["garden"] = $jsonVar -> garden;
        $record["fireplace"] = $jsonVar -> fireplace;
        $record["parquet"] = $jsonVar -> parquet;
        $record["elevator"] = $jsonVar -> elevator;
        $record["year_built"] = $jsonVar -> year_built;
        $record["availability_date"] = $jsonVar -> availability_date;
        $record["rooms_num"] = $jsonVar -> rooms_num;
        $record["living_room"] = $jsonVar -> living_room;
        $record["living_room_surface"] = $jsonVar -> living_room_surface;
        $record["shower_rooms_num"] = $jsonVar -> shower_rooms_num;
        $record["separate_toilets_num"] = $jsonVar -> separate_toilets_num;
        $record["terrace"] = $jsonVar -> terrace;
        $record["terrace_surface"] = $jsonVar -> terrace_surface;
        $record["balcony"] = $jsonVar -> balcony;
        $record["balcony_surface"] = $jsonVar -> balcony_surface;
        $record["garage_price"] = $jsonVar -> garage_price;
        $record["dining_room"] = $jsonVar -> dining_room;
        $record["washroom"] = $jsonVar -> washroom;
        $record["gas_heating"] = $jsonVar -> gas_heating;
        $record["oil_heating"] = $jsonVar -> oil_heating;
        $record["electric_heating"] = $jsonVar -> electric_heating;
        $record["wine_cellar"] = $jsonVar -> wine_cellar;
        $record["arranged_attic"] = $jsonVar -> arranged_attic;
        $record["finished_attic"] = $jsonVar -> finished_attic;
        $record["heating"] = $jsonVar -> heating;
        $record["building_start"] = $jsonVar -> building_start;
        $record["building_end"] = $jsonVar -> building_end;
        $record["area"] = $jsonVar -> area;
        $record["city"] = $jsonVar -> city;
        $record["price_by_m2"] = $jsonVar -> price_by_m2;
        $record["lift"] = $jsonVar -> lift;
        $record["energy_class"] = $jsonVar -> energy_class;
        $record["ground_contract"] = $jsonVar -> ground_contract;
        $record["thermal_insulation_class"] = $jsonVar -> thermal_insulation_class;
        $record["delivery_date"] = $jsonVar -> delivery_date;
        $record["basement"] = $jsonVar -> basement;
        $record["premium_property"] = $jsonVar -> premium_property;
        $record["status_banner"] = $jsonVar -> status_banner;
        $record["heat_pump"] = $jsonVar -> heat_pump;
        $record["geothermal"] = $jsonVar -> geothermal;
        $record["solar_panels"] = $jsonVar -> solar_panels;
        $record["dfp_transaction"] = $jsonVar -> dfp_transaction;
        $record["range_price_min"] = $jsonVar -> range_price -> min;
        $record["range_price_max"] = $jsonVar -> range_price -> max;
        
        //save the record
        scraperwiki::save(array('id'), $record);
    }    
} 

?>