<?php
require 'scraperwiki/simple_html_dom.php';     

$base_url = "http://www.icarros.com.br/fiat/mille/1993/ficha-tecnica";
$html = scraperWiki::scrape($base_url);     
     
$dom = new simple_html_dom();
$dom->load($html);

$a_fuel = array();

$a_fuel = getFuel($dom);

$count = 1;
$record = array();
foreach ($a_fuel as $kmain => $vmain) {
    foreach ($vmain as $kengine => $vengine) {        
        foreach ($vengine as $kversion => $vversion) {
            print $kversion . " | " . $vversion . "\n";
            $record[$kversion] = $vversion;            
        }
        $record['id'] = $count;
        scraperwiki::save(array('id'), $record);
        $count++;        
    }
}

function getFuel($dom) {
    $motor_table = $dom->find("table.listafichatecnica", 0);
    $a_fuel = array();
    $fuel_rows = $motor_table->find("tbody tr");

    // The car has no engine data
    if (count($fuel_rows) == 9) {
        $a_fuel['combustible']['Álcool'] = getUnknownFuel($fuel_rows);
    }
    else if (getFirstFuelType($dom) == 'Álcool') {
        $a_fuel['combustible']['Álcool'] = getFirstFuel($fuel_rows);
        $a_fuel['combustible']['Gasolina'] = getSecondFuel($fuel_rows);                 
    }
    else if (getFirstFuelType($dom) == 'Gasolina') {
        $a_fuel['combustible']['Gasolina'] = getFirstFuel($fuel_rows);
        $a_fuel['combustible']['Álcool'] = getSecondFuel($fuel_rows);       
    }
     
    return $a_fuel;
}


// Developers sometimes get bored and these ones sometimes have 
// the first column with alcohol as fuel and other random times 
// have the first column with gasoline as a fuel.
// Therefore this must be detected.
function getFirstFuelType($dom) {
    $motor_table = $dom->find("table.listafichatecnica", 0);
    $a_fuel = array();
    $fuel_row = $motor_table->find("tbody tr", 3);
    $a_details = array();

    $type = trim($fuel_row->find("td", 1)->plaintext);
    //print $type . "\n";
    return $type;
}

// Gets the fuel data of an engine with N/A data. 
// e.g: http://www.icarros.com.br/volkswagen/gol/1998/ficha-tecnica/1739
function getUnknownFuel($fuel_rows) {
    $num_rows = 0;    
    $a_details = array();
    foreach ($fuel_rows as $fuel_row) {    
        if ($num_rows > 1) {
            $tds = $fuel_row->find("td");                       
            $key = trim($tds[0]->plaintext);
            $value = trim($tds[1]->plaintext);
            $a_details[$key] = $value;                        
        }
        $num_rows++;    
    }
    return $a_details;
}

// Gets the fuel data of an alcohol engine.
// e.g: http://www.icarros.com.br/volkswagen/gol/2007/ficha-tecnica/4186
function getFirstFuel($fuel_rows) {
    $num_rows = 0;
    $flag = false;
    $a_details = array();
    foreach ($fuel_rows as $fuel_row) {    
        if ($num_rows > 0) {
            $tds = $fuel_row->find("td");                       
            $key = trim($tds[0]->plaintext);
            $value = trim($tds[1]->plaintext);
            if ($key == 'Combustível') {
                $flag = true;                
            }
            if ($flag === true) {
                $a_details[$key] = $value;                        
            }
        }
        $num_rows++;    
    }
    return $a_details;
}

// Gets the fuel data of a gasoline engine.
// e.g: http://www.icarros.com.br/volkswagen/gol/2007/ficha-tecnica/4186
function getSecondFuel($fuel_rows) {
    $num_rows = 0;
    $flag = false;
    $a_details = array();
    foreach ($fuel_rows as $fuel_row) {    
        if ($num_rows > 0) {
            $tds = $fuel_row->find("td");                       
            if (count($tds) === 3) {
                $key = trim($tds[0]->plaintext);
                $value = trim($tds[2]->plaintext);
                if ($key == 'Combustível') {
                    $flag = true;
                }        
                if ($flag === true) {
                    $a_details[$key] = $value;                        
                }
            }
        }
        $num_rows++;        
    }
    return $a_details;
}