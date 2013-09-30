<?php

# Blank PHP

$url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/ha.csv";
$json = array();
$row = 1;
if (($handle = fopen($url, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
        
        //This is the array
        $formatedOpenDate = substr($data[10], 6, 2)."/".substr($data[10], 4,2)."/".substr($data[10], 0, 4);
        
        $fieldsarray = array("code" => $data[0], "name" => ucwords(strtolower($data[1])), "it_code" => $data[2], "sha_code" => "", "address1" => ucwords(strtolower($data[4])), "address2" => ucwords(strtolower($data[5])), "address3" => ucwords(strtolower($data[6])), "address4" => ucwords(strtolower($data[7])), "address5" => ucwords(strtolower($data[8])), "postcode" => $data[9], "open_date" => $formatedOpenDate, "close_date" => $data[11]);

        scraperwiki::save_sqlite(array("name"), $fieldsarray);
    }
    fclose($handle);
}
echo json_encode($json);
?><?php

# Blank PHP

$url = "http://www.connectingforhealth.nhs.uk/systemsandservices/data/ods/datafiles/ha.csv";
$json = array();
$row = 1;
if (($handle = fopen($url, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
        
        //This is the array
        $formatedOpenDate = substr($data[10], 6, 2)."/".substr($data[10], 4,2)."/".substr($data[10], 0, 4);
        
        $fieldsarray = array("code" => $data[0], "name" => ucwords(strtolower($data[1])), "it_code" => $data[2], "sha_code" => "", "address1" => ucwords(strtolower($data[4])), "address2" => ucwords(strtolower($data[5])), "address3" => ucwords(strtolower($data[6])), "address4" => ucwords(strtolower($data[7])), "address5" => ucwords(strtolower($data[8])), "postcode" => $data[9], "open_date" => $formatedOpenDate, "close_date" => $data[11]);

        scraperwiki::save_sqlite(array("name"), $fieldsarray);
    }
    fclose($handle);
}
echo json_encode($json);
?>