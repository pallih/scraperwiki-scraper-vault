<?php

# Blank PHP
$url = 'http://www.insomniabs.net/maps3/CicloviasSense.kml';

$xml_content = scraperwiki::scrape($url);

$xml = new SimpleXMLElement($xml_content);

$placemarks =$xml->Document->Placemark;
foreach($placemarks as $placemark) {
    $name = (string) $placemark->name;
    if (substr($name, 0, 5) === 'Estac') {
        $row = new stdClass();
        $row->estacion    = $name;

        list($longitud, $latitud) = explode(',', (string) $placemark->Point->coordinates);
        $row->longitud = $longitud;
        $row->latitud  = $latitud;
        scraperwiki::save_sqlite(array("estacion"),$row);
        //print_r($row);
    }
}

?>
<?php

# Blank PHP
$url = 'http://www.insomniabs.net/maps3/CicloviasSense.kml';

$xml_content = scraperwiki::scrape($url);

$xml = new SimpleXMLElement($xml_content);

$placemarks =$xml->Document->Placemark;
foreach($placemarks as $placemark) {
    $name = (string) $placemark->name;
    if (substr($name, 0, 5) === 'Estac') {
        $row = new stdClass();
        $row->estacion    = $name;

        list($longitud, $latitud) = explode(',', (string) $placemark->Point->coordinates);
        $row->longitud = $longitud;
        $row->latitud  = $latitud;
        scraperwiki::save_sqlite(array("estacion"),$row);
        //print_r($row);
    }
}

?>
