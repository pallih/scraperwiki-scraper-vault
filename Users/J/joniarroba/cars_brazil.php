<?php

$html = scraperWiki::scrape("http://www.icarros.com.br/catalogo/listaversoes.jsp");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("div.lista") as $data) {

    $uls = $data->find("ul[class='']");
    $cars = getMainInfo($uls);
    $cars = getImageLink($uls, $cars);
    $cars = getVersions($uls, $cars);
    
}

print_r($cars);
/*
foreach($cars as $car) {
    $record = array(
        'model' => $car['model'] 
    );
}
print_r($record);
scraperWiki::save(array("model"), $record);
*/


function getMainInfo($uls) {
    $num_car = 0;
    foreach ($uls as $ul) {
            $lis = $ul->find("li.modelo");
    
            foreach ($lis as $li) {
                $links = $li->find("h1 a");
                foreach ($links as $link) {
                    $model = $link->plaintext;
                    $arr = explode(' ', trim($model));
                    $cars[$num_car]['brand'] = $arr[0];
                    $cars[$num_car]['model'] = $model;
                    $num_car++;
                }
            }
        }
    return $cars;
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

function getVersions($uls, $cars) {
    $num_car = 0;

    foreach ($uls as $ul) {
        $lis = $ul->find("li.modelo");
        foreach ($lis as $li) {
            $uls_versions = $li->find("ul");
            $num_version = 0;
            $a_version = array();
            foreach ($uls_versions as $ul_versions) {
                $links = $ul_versions->find("a");

                foreach ($links as $link) {
                    $version =  $link->plaintext;
                    $a_version[$num_version] = $version;              

                }
                $num_version++;       
            }
            $cars[$num_car]['version'] = $a_version;
            $num_car++;
        }
    }
    return $cars;
}


