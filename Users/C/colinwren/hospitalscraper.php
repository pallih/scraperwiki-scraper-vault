<?php

# Blank PHP

$url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/ts.csv";
$json = array();
$row = 1;
if (($handle = fopen($url, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
        
        //This is the array
        if($data[3] == "Q36"){
        $formatedOpenDate = substr($data[10], 0, 4)."-".substr($data[10], 4,2)."-".substr($data[10], 6, 2)." 00:00";
        
        $domdoc = new DOMDocument();
        $geoURL = "http://where.yahooapis.com/geocode?q=".str_replace(" ", "", $data[9]);
        $domdoc->load($geoURL);
        
        $georesult = $domdoc->getElementsByTagName("Result")->item(0);
        $lat = $georesult->getElementsByTagName("latitude")->item(0)->nodeValue;
        $long = $georesult->getElementsByTagName("longitude")->item(0)->nodeValue;
        
        $fieldsarray = array("code" => $data[0], "name" => str_replace("Nhs", "NHS", ucwords(strtolower($data[1]))), "it_code" => $data[2], "sha_code" => $data[3], "address1" => ucwords(strtolower($data[4])), "address2" => ucwords(strtolower($data[5])), "address3" => ucwords(strtolower($data[6])), "address4" => ucwords(strtolower($data[7])), "address5" => ucwords(strtolower($data[8])), "postcode" => $data[9], "lat" => $lat, "lng" => $long, "open_date" => $formatedOpenDate, "close_date" => "9999-12-31 00:00");

scraperwiki::save_sqlite(array("code"),$fieldsarray);
    }
    }
    fclose($handle);
}
//echo json_encode($json);

?>
.adslot-overlay {position: absolute; font-family: arial, sans-serif; background-color: rgba(0,0,0,0.65); border: 2px solid rgba(0,0,0,0.65); color: white !important; margin: 0; z-index: 2147483647; text-decoration: none; box-sizing: border-box; text-align: left;}.adslot-overlay-iframed {top: 0; left: 0; right: 0; bottom: 0;}.slotname {position: absolute; top: 0; left: 0; right: 0; font-size: 13px; font-weight: bold; padding: 3px 0 3px 6px; vertical-align: middle; background-color: rgba(0,0,0,0.45); text-overflow: ellipsis; white-space: nowrap; overflow: hidden;}.slotname span {text-align: left; text-decoration: none; text-transform: capitalize;}.revenue {position: absolute; bottom: 0; left: 0; right: 0; font-size: 11px; padding: 3px 0 3px 6px; vertial-align: middle; text-align: left; background-color: rgba(0,0,0,0.45); font-weight: bold; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;}.revenue .name {color: #ccc;}.revenue .horizontal .metric {display: inline-block; padding-right: 1.5em;}.revenue .horizontal .name {padding-right: 0.5em;}.revenue .vertical .metric {display: block; line-height: 1.5em; margin-bottom: 0.5em;}.revenue .vertical .name, .revenue .vertical .value {display: block;}.revenue .square .metric, .revenue .button .metric {display: table-row;}.revenue .square .metric {line-height: 1.5em;}.revenue .square .name, .revenue .square .value, .revenue .button .value {display: table-cell;}.revenue .square .name {padding-right: 1.5em;}.revenue .button .name {display: block; margin-right: 0.5em; width: 1em; overflow: hidden; text-overflow: clip;}.revenue .button .name:first-letter {margin-right: 1.5em;}a.adslot-overlay:hover {border: 2px solid rgba(58,106,173,0.9);}a.adslot-overlay:hover .slotname {border-bottom: 1px solid rgba(81,132,210,0.9); background-color: rgba(58,106,173,0.9);}a.adslot-overlay:hover .revenue {border-top: 1px solid rgba(81,132,210,0.9); background-color: rgba(58,106,173,0.9);}div.adslot-overlay:hover {cursor: not-allowed; border: 2px solid rgba(64,64,64,0.9);}div.adslot-overlay:hover .slotname {border-bottom: 1px solid rgba(128,128,128,0.9); background-color: rgba(64,64,64,0.9);}div.adslot-overlay:hover .revenue {border-top: 1px solid rgba(128,128,128,0.9); background-color: rgba(64,64,64,0.9);}
<?php

# Blank PHP

$url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/ts.csv";
$json = array();
$row = 1;
if (($handle = fopen($url, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
        
        //This is the array
        if($data[3] == "Q36"){
        $formatedOpenDate = substr($data[10], 0, 4)."-".substr($data[10], 4,2)."-".substr($data[10], 6, 2)." 00:00";
        
        $domdoc = new DOMDocument();
        $geoURL = "http://where.yahooapis.com/geocode?q=".str_replace(" ", "", $data[9]);
        $domdoc->load($geoURL);
        
        $georesult = $domdoc->getElementsByTagName("Result")->item(0);
        $lat = $georesult->getElementsByTagName("latitude")->item(0)->nodeValue;
        $long = $georesult->getElementsByTagName("longitude")->item(0)->nodeValue;
        
        $fieldsarray = array("code" => $data[0], "name" => str_replace("Nhs", "NHS", ucwords(strtolower($data[1]))), "it_code" => $data[2], "sha_code" => $data[3], "address1" => ucwords(strtolower($data[4])), "address2" => ucwords(strtolower($data[5])), "address3" => ucwords(strtolower($data[6])), "address4" => ucwords(strtolower($data[7])), "address5" => ucwords(strtolower($data[8])), "postcode" => $data[9], "lat" => $lat, "lng" => $long, "open_date" => $formatedOpenDate, "close_date" => "9999-12-31 00:00");

scraperwiki::save_sqlite(array("code"),$fieldsarray);
    }
    }
    fclose($handle);
}
//echo json_encode($json);

?>
.adslot-overlay {position: absolute; font-family: arial, sans-serif; background-color: rgba(0,0,0,0.65); border: 2px solid rgba(0,0,0,0.65); color: white !important; margin: 0; z-index: 2147483647; text-decoration: none; box-sizing: border-box; text-align: left;}.adslot-overlay-iframed {top: 0; left: 0; right: 0; bottom: 0;}.slotname {position: absolute; top: 0; left: 0; right: 0; font-size: 13px; font-weight: bold; padding: 3px 0 3px 6px; vertical-align: middle; background-color: rgba(0,0,0,0.45); text-overflow: ellipsis; white-space: nowrap; overflow: hidden;}.slotname span {text-align: left; text-decoration: none; text-transform: capitalize;}.revenue {position: absolute; bottom: 0; left: 0; right: 0; font-size: 11px; padding: 3px 0 3px 6px; vertial-align: middle; text-align: left; background-color: rgba(0,0,0,0.45); font-weight: bold; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;}.revenue .name {color: #ccc;}.revenue .horizontal .metric {display: inline-block; padding-right: 1.5em;}.revenue .horizontal .name {padding-right: 0.5em;}.revenue .vertical .metric {display: block; line-height: 1.5em; margin-bottom: 0.5em;}.revenue .vertical .name, .revenue .vertical .value {display: block;}.revenue .square .metric, .revenue .button .metric {display: table-row;}.revenue .square .metric {line-height: 1.5em;}.revenue .square .name, .revenue .square .value, .revenue .button .value {display: table-cell;}.revenue .square .name {padding-right: 1.5em;}.revenue .button .name {display: block; margin-right: 0.5em; width: 1em; overflow: hidden; text-overflow: clip;}.revenue .button .name:first-letter {margin-right: 1.5em;}a.adslot-overlay:hover {border: 2px solid rgba(58,106,173,0.9);}a.adslot-overlay:hover .slotname {border-bottom: 1px solid rgba(81,132,210,0.9); background-color: rgba(58,106,173,0.9);}a.adslot-overlay:hover .revenue {border-top: 1px solid rgba(81,132,210,0.9); background-color: rgba(58,106,173,0.9);}div.adslot-overlay:hover {cursor: not-allowed; border: 2px solid rgba(64,64,64,0.9);}div.adslot-overlay:hover .slotname {border-bottom: 1px solid rgba(128,128,128,0.9); background-color: rgba(64,64,64,0.9);}div.adslot-overlay:hover .revenue {border-top: 1px solid rgba(128,128,128,0.9); background-color: rgba(64,64,64,0.9);}
