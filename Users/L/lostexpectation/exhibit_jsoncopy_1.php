<?php

//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('irish_president_engagementsjson'); 

$trips = scraperwiki::select("* from irish_president_engagementsjson.swdata where date > date('now','-7 day');");

$alltrips = array(); 
foreach ($trips as $trip)
{
$tripinfo = $trip["info"];
$triplabel = $trip["label"];

$tripinfo = str_replace('(', '', $tripinfo);
$tripinfo = str_replace(')', ',', $tripinfo);
$triplabel = str_replace('(', '', $triplabel);
$triplabel = str_replace(')', ',', $triplabel);
//print $triplabel;
$trip["info"] = $tripinfo;
$trip["label"] = $triplabel;

$alltrips[] = $trip;

}

//header('Content-type: application/json');
scraperwiki::httpresponseheader('Content-Type', 'application/json', 'charset=utf8');
//print "{ \"items\": ".json_encode($alltrips) ."}";


$callback = $_GET['callback'];
if ($callback) {
    header("Content-Type: text/javascript; charset=utf8");
    echo $callback . "(" . json_encode($alltrips) . ");";
} else {
    header("Content-type: application/json");
    echo json_encode($alltrips);
}

// {label}    {id}    {type}    {day}    {date}            {year}    {time}    {startdate}    {latlng}        {arasnotaras}    {details}        {place}    {act}    {issue}    {constitutional}    {destf}    {address}    {days}        {destination}                  

?>      