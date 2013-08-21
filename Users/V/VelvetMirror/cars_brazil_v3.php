<?php
require 'scraperwiki/simple_html_dom.php';     
$base_url = "http://www.icarros.com.br/catalogo/index.jsp";

//$brands = getBrands($base_url);
$versions = getModelsYears("/volkswagen/gol/");

function getBrands($base_url) {
    $html = scraperWiki::scrape($base_url);     
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("table.diretorio tr");

    foreach ($rows as $row) {
        $columns = $row->find("td a");
        foreach ($columns as $column) {
            $brand_name = $column->plaintext;
            $brand_url = $column->href;
            $brands[$brand_name] =  getModels($brand_url);
        }
    }
    return $brands;
}

function getModels($brand_url) {
    $url = "http://www.icarros.com.br" . $brand_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("li.modelo h1 a");

    foreach($rows as $row) {
        $model_name = $row->plaintext;
        $url = $row->href;
        $models[$model_name] = getVersions($url);
    }
    return $models;
}

function getModelsYears($model_url) {
    $url = "http://www.icarros.com.br" . $model_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("div.outrosanosmodelo tbody tr");

    $count = 0;
    foreach ($rows as $row) {
        if ($count > 0) {
            $year = $row->find("td", 0)->plaintext;
            $year_url = $row->find("td a", 0)->href;
            $versions[$year] = getYears($year_url);
        }
        $count++;
    }
}

function getYears($year_url) {
    $url = "http://www.icarros.com.br" . $year_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);    
    
    $rows = $dom->find("table.listaversoesofertas tbody tr");

    $count = 0;
    foreach($rows as $row) {
        if ($count > 0) {
            $version_url = $row->find("td a", 0)->href;
            print $version_url . "\n";
            $info = getInfoVersion("http://www.icarros.com.br" . $version_url);
            print_r($info);
            exit;
        }
        $count++;
    }
    exit;
}

function getInfoVersion($base_url) {
    $html = scraperWiki::scrape($base_url);     
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $engine_table = $dom->find("table.listafichatecnica", 0);
    $dimensions_table = $dom->find("table.listafichatecnica", 1);
    $mechanics_table = $dom->find("table.listafichatecnica", 2);
    $serial_items_table = $dom->find("table.listafichatecnica", 3);

    if ($engine_table != null) {
        $a_motor = getMotor($dom);
    }
    if ($dimensions_table != null) {
        $a_dimensions = getDimensions($dom); 
    }
    if ($mechanics_table != null) {
        $a_mechanics = getMechanics($dom);
    }

    if ($serial_items_table != null) {
        $a_serial_items = getSerialItems($dom);
    }
    $a_average_valuation = getValuation($dom);
    $a_segment = getSegment($dom, $base_url);

    $a_technical_data = array_merge($a_motor, $a_dimensions, $a_mechanics, $a_average_valuation, $a_segment, $a_serial_items);

    return $a_technical_data;
}

function getMotor($dom) {
    $motor_table = $dom->find("table.listafichatecnica", 0);
    $a_motor = array();

    $motor_row = $motor_table->find("tbody tr", 1);    
    $key = trim($motor_row->find("td", 0)->plaintext);
    $value = trim($motor_row->find("td", 1)->plaintext);
    $a_motor[$key] = $value;

    $power_row = $motor_table->find("tbody tr", 2);
    $key = trim($power_row->find("td", 0)->plaintext);
    $value = trim($power_row->find("td", 1)->plaintext);
    $a_motor[$key] = $value;

    $a_motor = array_merge($a_motor, getFuel($dom));
  
    return $a_motor;
}

function getSegment($dom, $base_url) {
    $general_vision_link = $dom->find("li.li_primeiro a", 0)->href;
    $general_vision_url = "http://www.icarros.com.br" . $general_vision_link;
    $html = scraperWiki::scrape($general_vision_url);

    $general_vision_dom = new simple_html_dom();
    $general_vision_dom->load($html);

    $segments = $general_vision_dom->find("div.classemercado");

    $segment_found = null;
    foreach ($segments as $segment) {
        $segment_name = $segment->find("h3.subtitlesimple", 0)->plaintext;
        $a_url = parse_url($base_url);
        $links = $segment->find("div.listaversoes a"); 

        foreach ($links as $link) {
            if ($a_url['path'] == $link->href) {
                $segment_found = $segment_name;                
            }
        }
    }
    $a_segment_found['Classe mercado'] = $segment_found;
    return $a_segment_found;
}

function getValuation($dom) {
    $general_vision_link = $dom->find("li.li_primeiro a", 0)->href;
    $general_vision_url = "http://www.icarros.com.br" . $general_vision_link;
    $html = scraperWiki::scrape($general_vision_url);
    $general_vision_dom = new simple_html_dom();
    $general_vision_dom->load($html);
    $average_valuation = trim($general_vision_dom->find("div.notamedia", 0)->plaintext);
    $a_average_valuation['Avaliação Geral'] = $average_valuation;
 
    return $a_average_valuation;
}

function getSerialItems($dom) {
    $serial_items_table = $dom->find("table.listafichatecnica", 3);
    $a_serial_items = array();
    $count = 0;
    $serial_items_row = $serial_items_table->find("tbody tr");
    
    $label = "Item de série ";
    foreach ($serial_items_row as $row) {
        if ($count > 0) {        
            $value = trim($row->find("td", 0)->plaintext);
            $a_serial_items[$label . $count] = $value;
        }
        $count++;
    }    
  
    return $a_serial_items;
}

function getMechanics($dom) {
    $dimensions_table = $dom->find("table.listafichatecnica", 2);
    $a_dimensions = array();
    $count = 0;
    $dimensions_row = $dimensions_table->find("tbody tr");
    
    foreach ($dimensions_row as $row) {
        if ($count > 0) {
            $key = trim($row->find("td", 0)->plaintext);
            $value = trim($row->find("td", 1)->plaintext);
            $a_dimensions[$key] = $value;
        }
        $count++;
    }    
  
    return $a_dimensions;
}

function getDimensions($dom) {
    $dimensions_table = $dom->find("table.listafichatecnica", 1);
    $a_dimensions = array();
    $count = 0;

    $dimensions_row = $dimensions_table->find("tbody tr");    
    
    foreach ($dimensions_row as $row) {
        if ($count > 0) {
            $key = trim($row->find("td", 0)->plaintext);
            $value = trim($row->find("td", 1)->plaintext);
            $a_dimensions[$key] = $value;
        }
        $count++;
    }    
  
    return $a_dimensions;
}

function getFuel($dom) {
    $motor_table = $dom->find("table.listafichatecnica", 0);
    $a_fuel = array();
    $fuel_rows = $motor_table->find("tbody tr");

    // The car has no engine data
    if (count($fuel_rows) == 9) {
        $a_fuel['combustible']['Gasolina'] = getUnknownFuel($fuel_rows);
    }
    else if (getFirstFuelType($dom) == 'Álcool') {
        $a_fuel['combustible']['Álcool'] = getFirstFuel($fuel_rows);
        $secondFuel = getSecondFuel($fuel_rows);
        if (empty($secondFuel) == false) {
            $a_fuel['combustible']['Gasolina'] = getSecondFuel($fuel_rows);  
        }               
    }
    else if (getFirstFuelType($dom) == 'Gasolina') {
        $a_fuel['combustible']['Gasolina'] = getFirstFuel($fuel_rows);
        $secondFuel = getSecondFuel($fuel_rows);  
 
        if (empty($secondFuel) == false) {
            $a_fuel['combustible']['Álcool'] = getSecondFuel($fuel_rows);       
        }                       

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