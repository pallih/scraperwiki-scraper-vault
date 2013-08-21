<?php
require 'scraperwiki/simple_html_dom.php';     

$urls = array( 
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=2&app=20&sop=&pas=1&lis=&pag=1&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=1&app=20&sop=&pas=1&lis=&pag=2&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=2&app=20&sop=&pas=1&lis=&pag=3&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=3&app=20&sop=&pas=1&lis=&pag=4&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=4&app=20&sop=&pas=1&lis=&pag=5&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=4&app=20&sop=&pas=1&lis=&pag=6&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=4&app=20&sop=&pas=1&lis=&pag=7&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=5&app=20&sop=&pas=1&lis=&pag=8&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=5&app=20&sop=&pas=1&lis=&pag=9&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=5&app=20&sop=&pas=1&lis=&pag=10&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=6&app=20&sop=&pas=1&lis=&pag=11&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=6&app=20&sop=&pas=1&lis=&pag=12&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=6&app=20&sop=&pas=1&lis=&pag=13&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=7&app=20&sop=&pas=1&lis=&pag=14&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=7&app=20&sop=&pas=1&lis=&pag=15&ord=4",
    "http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=7&app=20&sop=&pas=1&lis=&pag=16&ord=4",
);

foreach ($urls as $url) {

    $html = scraperWiki::scrape("http://www.icarros.com.br/catalogo/listaversoes.jsp?bid=2&app=20&sop=&pas=1&lis=&pag=1&ord=4");     
      
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("div.lista") as $data) {
        $uls = $data->find("ul[class='']");
        $cars = getCarsInfo($uls);
    }
}

function getCarsInfo($uls) {
    $cars = array();
    foreach ($uls as $ul) {
            $lis = $ul->find("li.modelo");
    
            foreach ($lis as $li) {
                $links = $li->find("h1 a");
                foreach ($links as $link) {
                    // Full model name, e.g: Volkswagen Golf
                    $full_model = $link->plaintext;
                    
                    // Array with full model name, e.g: $a_full_model[0] = Wolkswagen, $a_full_model[1] = Golf
                    $a_full_model = explode(' ', trim($full_model));

                    // String with the car brand, e.g: Wolkswagen
                    $brand = $a_full_model[0];

                    // Array with first word and the rest of the string, e.g: $a_model[0] = Chevrolet, $a_model[1] = Corsa Hatch
                    $a_model = explode (' ', $full_model, 2);

                    // String with the card model, e.g: Corsa Hatch
                    $model = $a_model[1];

                    // Contains the models for each brand.
                    $cars[$brand][$model] = $model;
                }
                // Searches for the <ul> tag containing the versions.
                $uls_versions = $li->find("ul");                          
                $a_version = array();  
                // Each $ul_versions represents one version.
                foreach ($uls_versions as $ul_versions) {
                    $links = $ul_versions->find("a");
                    
                    // Extracts the version name from the link.
                    foreach ($links as $link) {
                        $version =  $link->plaintext;
                        $version_link = $link->href;
                        //print $version_link . "\n";
                    }                    
                    
                    // $a_version contains all the current model versions.
                    $a_version[$version] = getInfoVersion($version_link);
                    // Asigns to each model all it's versions.
                    $cars[$brand][$model] = $a_version;   
                    $record['brand'] = $brand;
                    $record['model'] = $model;
                    $record['version'] = $version;   
                    foreach($a_version[$version] as $kversion => $vversion) {                   
                      $record[$kversion] = $vversion;                      
                      scraperwiki::save(array('version'), $record);
                    }              
                }                      
            } 
    }
    return $cars;
}

function getInfoVersion($version_link) {
    $BASE_URL = "http://www.icarros.com.br";
    $html = scraperWiki::scrape($BASE_URL . $version_link);
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $engine_table = $dom->find("table.listafichatecnica", 0);
    $dimensions_table = $dom->find("table.listafichatecnica", 1);
    $mechanics_table = $dom->find("table.listafichatecnica", 2);
    $serial_items_table = $dom->find("table.listafichatecnica", 3);

    $a_engine = array();
    $a_dimensions = array();
    $a_mechanics = array();
    $a_serial_items = array();

    if ($engine_table != null) {
        $a_engine = getDetails($engine_table);
    }
    
    if ($dimensions_table != null) {
        $a_dimensions = getDetails($dimensions_table);    
    }

    if ($mechanics_table != null) {
        $a_mechanics = getDetails($mechanics_table);
    }

    if ($serial_items_table != null) {
        $a_serial_items = getSerialItems($serial_items_table);        
    }

    $a_info = array_merge($a_engine, $a_dimensions, $a_mechanics, $a_serial_items);

    return $a_info;
}

function getSerialItems($table) {
    $rows = $table->find("tr");

    $a_details = array();

    $num_rows = 0;
    $label = "Item de série ";
    foreach ($rows as $row) {
        if ($num_rows > 0) {
            $tds = $row->find("td");       
            $value = trim($tds[0]->plaintext);            
            $a_details[$label . $num_rows] = $value;
        }
        $num_rows++;
    }     
    return $a_details;
}

function getDetails($table) {
    $rows = $table->find("tr");

    $a_details = array();

    $num_rows = 0;
    foreach ($rows as $row) {
        if ($num_rows > 0) {
            $tds = $row->find("td");       
            $key = trim($tds[0]->plaintext);
            $value = trim($tds[1]->plaintext);
            $a_details[$key] = $value;
        }
        $num_rows++;
    }       
    return $a_details;
}

function getImageLink($uls, $cars) {
    $num_car = 0;
    foreach ($uls as $ul) {
        $lis = $ul->find("li.imagem");
        
        foreach ($lis as $li) {
            $links = $li->find("img");       
            foreach($links as $link) {
                $cars[$num_car]['pic'] = $link->src;
                $num_car++;
            }
        }
    }    
    return $cars;
}