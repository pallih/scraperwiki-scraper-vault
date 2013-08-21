<?php

/* NOME, BANDEIRA, PRECO, GEOLOC */
$baseurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=fuel_scraper_anp_2&query=";
$stations = json_decode(file_get_contents($baseurl . urlencode("select cities.estado, cities.nome, gas_station.id, gas_station.razao_social, gas_station.endereco from 'cities', 'gas_station' where gas_station.id_cidade = cities.id")));
$prices = json_decode(file_get_contents($baseurl . urlencode("select gas_price.combustivel, gas_price.preco_venda, gas_station.id from 'gas_station', 'gas_price' where gas_station.id = gas_price.id_posto")));
$geoURL = "https://maps.google.com/maps/api/geocode/json?sensor=false&region=br&address=";

$data = null; $diesel = null; $etanol = null; $gasolina = null; $glp = null; $latlng = null;
for ($i = 0; $i < count($stations); $i++) {
    for ($j = 0; $j < count($prices); $j++) {
        if ($prices[$j]->id == $stations[$i]->id) {
            switch($prices[$j]->combustivel) {
                case "Diesel":
                    $diesel = $prices[$j]->preco_venda;
                    break;
                case "Etanol":
                    $etanol = $prices[$j]->preco_venda;
                    break;
                case "Gasolina":
                    $gasolina = $prices[$j]->preco_venda;
                    break;
                case "GLP":
                    $glp = $prices[$j]->preco_venda;
                    break;
            }
        }
    }
    
    $geocode = json_decode(file_get_contents($geoURL . urlencode($stations[$i]->endereco.", ".$stations[$i]->nome.", ".$stations[$i]->estado)));
    
    $data[$i] = array(
        "id"       => $stations[$i]->id,
        "nome"     => $stations[$i]->razao_social,
        "endereco" => $stations[$i]->endereco,
        "cidade"   => $stations[$i]->nome,
        "estado"   => $stations[$i]->estado,
        "diesel"   => $diesel,
        "etanol"   => $etanol,
        "gasolina" => $gasolina,
        "glp"      => $glp,
        "lat"   => $geocode->results[0]->geometry->location->lat,
        "lng"   => $geocode->results[0]->geometry->location->lng
    );
}

scraperwiki::sqliteexecute("drop table if exists postos");
scraperwiki::sqliteexecute("create table postos(id integer, nome text, endereco text, cidade text, estado text, diesel real, etanol real, gasolina real, glp real, lat real, lng real)");
scraperwiki::save_sqlite(array("id"), $data, $table_name="postos");

?>