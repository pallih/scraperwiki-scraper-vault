<?php

scraperwiki::httpresponseheader('Content-Type', 'text/xml; charset=utf-8');

//Scraper by Ændrew Rininsland, licensed openly. Uses data from Transport for London. Information wants to be free.

scraperwiki::attach("tfl_bus_route_aggregator", "src"); 

$routes = scraperwiki::select( "route, coords from src.swdata order by id asc" );

// THIS IS ABSOLUTELY ESSENTIAL - DO NOT FORGET TO SET THIS
@date_default_timezone_set("GMT");

$writer = new XMLWriter();
// Output directly to the user

$writer->openURI('php://output');
$writer->startDocument('1.0');

$writer->setIndent(4);

$writer->startElement('kml');
$writer->writeAttribute('xmlns', 'http://www.opengis.net/kml/2.2');
$writer->startElement('Document');

$writer->writeElement('name', 'Transport for London bus routes');
$writer->writeElement('description', 'Taken from TfL\'s bus routes feed, scraped once a month.');
/*
$writer->startElement('Style');

$writer->startElement('LineStyle');
$writer->writeElement('color', '7f00ffff');
$writer->writeElement('width', '4');
$writer->endElement(); //lineStyle

$writer->startElement('PolyStyle');
$writer->writeElement('color', '7f00ff00');
$writer->endElement(); //polystyle

$writer->endElement(); //style
*/
foreach ($routes as $route) {

$writer->startElement('Placemark');
$writer->writeElement('name', $route['route']);
$writer->startElement('LineString');
//$writer->writeElement('extrude', '1');
$writer->writeElement('tessellate', '1');
$writer->writeElement('altitudeMode', 'clampToGround');
$coords = str_replace("\n", ';', $route['coords']);
$writer->writeElement('coordinates', $coords);
$writer->endElement(); //linestring
$writer->endElement(); //placemark

}

$writer->endElement(); //Document
$writer->endElement(); //kml
?>
<?php

scraperwiki::httpresponseheader('Content-Type', 'text/xml; charset=utf-8');

//Scraper by Ændrew Rininsland, licensed openly. Uses data from Transport for London. Information wants to be free.

scraperwiki::attach("tfl_bus_route_aggregator", "src"); 

$routes = scraperwiki::select( "route, coords from src.swdata order by id asc" );

// THIS IS ABSOLUTELY ESSENTIAL - DO NOT FORGET TO SET THIS
@date_default_timezone_set("GMT");

$writer = new XMLWriter();
// Output directly to the user

$writer->openURI('php://output');
$writer->startDocument('1.0');

$writer->setIndent(4);

$writer->startElement('kml');
$writer->writeAttribute('xmlns', 'http://www.opengis.net/kml/2.2');
$writer->startElement('Document');

$writer->writeElement('name', 'Transport for London bus routes');
$writer->writeElement('description', 'Taken from TfL\'s bus routes feed, scraped once a month.');
/*
$writer->startElement('Style');

$writer->startElement('LineStyle');
$writer->writeElement('color', '7f00ffff');
$writer->writeElement('width', '4');
$writer->endElement(); //lineStyle

$writer->startElement('PolyStyle');
$writer->writeElement('color', '7f00ff00');
$writer->endElement(); //polystyle

$writer->endElement(); //style
*/
foreach ($routes as $route) {

$writer->startElement('Placemark');
$writer->writeElement('name', $route['route']);
$writer->startElement('LineString');
//$writer->writeElement('extrude', '1');
$writer->writeElement('tessellate', '1');
$writer->writeElement('altitudeMode', 'clampToGround');
$coords = str_replace("\n", ';', $route['coords']);
$writer->writeElement('coordinates', $coords);
$writer->endElement(); //linestring
$writer->endElement(); //placemark

}

$writer->endElement(); //Document
$writer->endElement(); //kml
?>
