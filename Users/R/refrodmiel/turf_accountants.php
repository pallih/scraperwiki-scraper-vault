<?php

# Get data from the page
 $data = file_get_contents('http://www.localstore.co.uk/cr2/417/67/bookmaker/city-of-bristol/p1');
 $regex = '/var map_results = \[(.+?)\]/';
 preg_match($regex,$data,$match);
 var_dump($match);
# echo $match[1];

# Data is a string (of objects) parse it into Array of Objects

 $bookiesA = explode("id", $match[1]); 

# rip out the unnecessary stuff from each long string

$splitstring = explode(":", $bookiesA[1]); 

$bname = str_replace(',"cuisine"', "", $splitstring[2]);
$blat = str_replace(',"longitude"', "", $splitstring[4]);
$blng = str_replace(',"url"', "", $splitstring[5]);

#get rid of quote on latlong - make numeric
$blat = str_replace('"', "", $blat);
$blng = str_replace('"', "", $blng);

$record = array("company" => $bname, "lat" => $blat, "long" => $blng);

print_r($record);

scraperwiki::save(array('company'), $record);

#To Do - Foreach loop.

?>
