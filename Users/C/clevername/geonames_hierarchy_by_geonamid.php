<?php
$geonameid = 2657896;
$request = simplexml_load_file("http://api.geonames.org/hierarchy?geonameId=" . $geonameid . "&username=pinpads");
echo $request->geoname[0]->name;
?><?php
$geonameid = 2657896;
$request = simplexml_load_file("http://api.geonames.org/hierarchy?geonameId=" . $geonameid . "&username=pinpads");
echo $request->geoname[0]->name;
?>