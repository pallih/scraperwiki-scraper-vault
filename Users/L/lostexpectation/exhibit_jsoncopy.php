<?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('irish_president_engagementsjson'); 

$trips = scraperwiki::select("* from irish_president_engagementsjson.swdata where date > date('now','-7 day');");


$alltrips = array(); 
foreach ($trips as $trip)
{
$tinfo = $trip["info"];
//print $tinfo;
$tlabel = $trip["label"];
//tlabel = str_replace('(','\(',$tlabel);
//$tlabel = str_replace(')','\)',$tlabel);
//$tinfo = str_replace('(','\(',$tinfo);
//$tinfo = str_replace(')','\)',$tinfo);
$tlabel = addslashes($tlabel);
$tinfo = addslashes($tinfo);
//$alltrip = $tinfo,$tplace;
//$trip["info"] = addslashes($tinfo);
//$trip["label"] = addslashes($tlabel);
//$tlabel = str_replace('\\\\(','\(',$tlabel);
//$tlabel = str_replace('\\\\)','\)',$tlabel);
//$tinfo = str_replace('\\\\(','\(',$tinfo);
//$tinfo = str_replace('\\\\)','\)',$tinfo);

$trip["info"] = $tinfo;
$trip["label"] = $tlabel;
$alltrip['info'] = $trip['info'];
$alltrip['label'] = $trip['label'];
$alltrip['latlng'] = $trip['latlng'];
$alltrip['startdate'] = $trip['startdate'];
$alltrip['type'] = $trip['type'];
$alltrips[] = $alltrip;
}

header('Content-type: application/json');
print "{ \"items\": ".json_encode($alltrips) ."}";



// {label}    {id}    {type}    {day}    {date}            {year}    {time}    {startdate}    {latlng}        {arasnotaras}    {details}        {place}    {act}    {issue}    {constitutional}    {destf}    {address}    {days}        {destination}                  

?>      
<?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('irish_president_engagementsjson'); 

$trips = scraperwiki::select("* from irish_president_engagementsjson.swdata where date > date('now','-7 day');");


$alltrips = array(); 
foreach ($trips as $trip)
{
$tinfo = $trip["info"];
//print $tinfo;
$tlabel = $trip["label"];
//tlabel = str_replace('(','\(',$tlabel);
//$tlabel = str_replace(')','\)',$tlabel);
//$tinfo = str_replace('(','\(',$tinfo);
//$tinfo = str_replace(')','\)',$tinfo);
$tlabel = addslashes($tlabel);
$tinfo = addslashes($tinfo);
//$alltrip = $tinfo,$tplace;
//$trip["info"] = addslashes($tinfo);
//$trip["label"] = addslashes($tlabel);
//$tlabel = str_replace('\\\\(','\(',$tlabel);
//$tlabel = str_replace('\\\\)','\)',$tlabel);
//$tinfo = str_replace('\\\\(','\(',$tinfo);
//$tinfo = str_replace('\\\\)','\)',$tinfo);

$trip["info"] = $tinfo;
$trip["label"] = $tlabel;
$alltrip['info'] = $trip['info'];
$alltrip['label'] = $trip['label'];
$alltrip['latlng'] = $trip['latlng'];
$alltrip['startdate'] = $trip['startdate'];
$alltrip['type'] = $trip['type'];
$alltrips[] = $alltrip;
}

header('Content-type: application/json');
print "{ \"items\": ".json_encode($alltrips) ."}";



// {label}    {id}    {type}    {day}    {date}            {year}    {time}    {startdate}    {latlng}        {arasnotaras}    {details}        {place}    {act}    {issue}    {constitutional}    {destf}    {address}    {days}        {destination}                  

?>      
<?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('irish_president_engagementsjson'); 

$trips = scraperwiki::select("* from irish_president_engagementsjson.swdata where date > date('now','-7 day');");


$alltrips = array(); 
foreach ($trips as $trip)
{
$tinfo = $trip["info"];
//print $tinfo;
$tlabel = $trip["label"];
//tlabel = str_replace('(','\(',$tlabel);
//$tlabel = str_replace(')','\)',$tlabel);
//$tinfo = str_replace('(','\(',$tinfo);
//$tinfo = str_replace(')','\)',$tinfo);
$tlabel = addslashes($tlabel);
$tinfo = addslashes($tinfo);
//$alltrip = $tinfo,$tplace;
//$trip["info"] = addslashes($tinfo);
//$trip["label"] = addslashes($tlabel);
//$tlabel = str_replace('\\\\(','\(',$tlabel);
//$tlabel = str_replace('\\\\)','\)',$tlabel);
//$tinfo = str_replace('\\\\(','\(',$tinfo);
//$tinfo = str_replace('\\\\)','\)',$tinfo);

$trip["info"] = $tinfo;
$trip["label"] = $tlabel;
$alltrip['info'] = $trip['info'];
$alltrip['label'] = $trip['label'];
$alltrip['latlng'] = $trip['latlng'];
$alltrip['startdate'] = $trip['startdate'];
$alltrip['type'] = $trip['type'];
$alltrips[] = $alltrip;
}

header('Content-type: application/json');
print "{ \"items\": ".json_encode($alltrips) ."}";



// {label}    {id}    {type}    {day}    {date}            {year}    {time}    {startdate}    {latlng}        {arasnotaras}    {details}        {place}    {act}    {issue}    {constitutional}    {destf}    {address}    {days}        {destination}                  

?>      
<?php
# Blank PHP
//$sourcescraper = 'irish_president_engagementstest';

//$s = scraperwiki::scrape($sourcescraper, $limit=250);
// = scraperwiki::attach($sourcescraper, $limit=250);
scraperwiki::attach('irish_president_engagementsjson'); 

$trips = scraperwiki::select("* from irish_president_engagementsjson.swdata where date > date('now','-7 day');");


$alltrips = array(); 
foreach ($trips as $trip)
{
$tinfo = $trip["info"];
//print $tinfo;
$tlabel = $trip["label"];
//tlabel = str_replace('(','\(',$tlabel);
//$tlabel = str_replace(')','\)',$tlabel);
//$tinfo = str_replace('(','\(',$tinfo);
//$tinfo = str_replace(')','\)',$tinfo);
$tlabel = addslashes($tlabel);
$tinfo = addslashes($tinfo);
//$alltrip = $tinfo,$tplace;
//$trip["info"] = addslashes($tinfo);
//$trip["label"] = addslashes($tlabel);
//$tlabel = str_replace('\\\\(','\(',$tlabel);
//$tlabel = str_replace('\\\\)','\)',$tlabel);
//$tinfo = str_replace('\\\\(','\(',$tinfo);
//$tinfo = str_replace('\\\\)','\)',$tinfo);

$trip["info"] = $tinfo;
$trip["label"] = $tlabel;
$alltrip['info'] = $trip['info'];
$alltrip['label'] = $trip['label'];
$alltrip['latlng'] = $trip['latlng'];
$alltrip['startdate'] = $trip['startdate'];
$alltrip['type'] = $trip['type'];
$alltrips[] = $alltrip;
}

header('Content-type: application/json');
print "{ \"items\": ".json_encode($alltrips) ."}";



// {label}    {id}    {type}    {day}    {date}            {year}    {time}    {startdate}    {latlng}        {arasnotaras}    {details}        {place}    {act}    {issue}    {constitutional}    {destf}    {address}    {days}        {destination}                  

?>      
