<?php
require 'scraperwiki/simple_html_dom.php';
$findbrewerydata = "td[@width='20%'] a";
$findbeerodddata = "tr.dataTableRowAlternate";
$findbeerevendata = "table[@style='border-bottom: 0px solid #d7d7d7;']";
$findbeerevenrowdata = "tr.dataTableRow";
break;
$html = scraperWiki::scrape("http://www.ratebeer.com/browsebrewers-A.htm");
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find($findbrewerydata) as $brewerydata)
{
$breweryrecord = getbrewerylink($brewerydata);
$breweryhtmllink = "http://www.ratebeer.com" . $breweryrecord['Brewery Link'];
$breweryhtml = scraperWiki::scrape($breweryhtmllink);
$brewerydom = new simple_html_dom();
$brewerydom->load($breweryhtml);

getbreweryinfo($brewerydom,$breweryrecord);
foreach($brewerydom->find($findbeerodddata) as $data)
{
getbeerdata($data,$breweryrecord['Brewery ID']);
}
foreach($brewerydom->find($findbeerevendata) as $data)
{
foreach($data->find($findbeerevenrowdata) as $TRdata)
{
getbeerdata($TRdata,$breweryrecord['Brewery ID']);
}
}
}


function getbrewerylink($brewerydata){
$brewerylink = $brewerydata->getAttribute('href');
$breweryexplodelink = explode('/', $brewerylink);
$breweryid = $breweryexplodelink[3];
$breweryname = utf8_encode($brewerydata->plaintext);
$breweryrecord = array( 'Brewery ID' => $breweryid, 'Brewery' => $breweryname, 'Brewery Link' => $brewerylink );
return $breweryrecord;
}

function getbreweryinfo($brewerydom,$breweryrecord){
foreach($brewerydom->find("td[@width='130'] a") as $breweryinfo)
{
$link = $breweryinfo->getAttribute("href");
$ismap = strpos($link, "http://maps.google.com");
if ($ismap !== false)
{
$breweryrecord["address"] = utf8_encode($breweryinfo->plaintext);
}
$istel = strpos($link, "tel:");
if ($istel !== false)
{
$breweryrecord["telephone"] = $breweryinfo->plaintext;
}
}
foreach($brewerydom->find("td[@width='130'] span.beerfoot") as $breweryinfo)
{
$breweryrecord["hours"] = $breweryinfo->plaintext;
}
$breweryrecord["blank"] = "";
//print_r($breweryrecord);
scraperwiki::save_sqlite(array('Brewery ID'), $breweryrecord, $table_name="brewerydata");
}

function getbeerdata($data,$breweryid) {
$scrapetime = date(DATE_RFC822);
settype($scrapetime, "string");
$beerinfo = $data->find("td");
$beerlink = $data->find("td a");
$beerotherinfo = 0;
settype($beerotherinfo, "string");
if ($data->find("td span.rip"))
{
$beerotherinfo = $data->find("td span.rip");
$beerotherinfo = stringtest($beerotherinfo[0]->plaintext);
};
if ($beerotherinfo == "0")
{
$a=3;
$b=4;
$c=5;
$d=6;
$e=7;
} elseif ($beerotherinfo == "R"){
$a=4;
$b=5;
$c=6;
$d=7;
$e=8;
} elseif ($beerotherinfo == "A"){
$a=3;
$b="";
$c="";
$d="";
$e=7;
};
$beerlinkhref = $beerlink[0]->getAttribute("href");
$beerexplodelink = explode('/', $beerlinkhref);
$beerid = $beerexplodelink[3];
//preg_match("/[0-9]+/", $beerlinkhref, $beerid);
$beernamearray = explode('/', $beerlinkhref, 4);
$beername = ucwords(str_replace("-", " ", $beernamearray[2]));
$beerrecord = array( 'Beer ID' => $beerid, 'Brewery ID' => $breweryid, 'Beer Name' => $beername, 'Beer Link' => $beerlink[0]->getAttribute("href"), 'ABV' => stringtest($beerinfo[$a]->plaintext), 'Score' => stringtest($beerinfo[$b]->plaintext), 'Overall' => stringtest($beerinfo[$c]->plaintext), 'Style' => stringtest($beerinfo[$d]->plaintext), 'Ratings' => stringtest($beerinfo[$e]->plaintext), 'Scrape' => $scrapetime, 'Other' => $beerotherinfo, 'Blank' =>"");
//print_r($beerrecord);
scraperwiki::save_sqlite(array('Beer ID'), $beerrecord, $table_name="beerdata");
}

function stringtest($test) {
if ($test == ''){
$test = " ";
return $test;
} else {
$test = str_replace("&nbsp;", "", $test);
return $test;
}
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
$findbrewerydata = "td[@width='20%'] a";
$findbeerodddata = "tr.dataTableRowAlternate";
$findbeerevendata = "table[@style='border-bottom: 0px solid #d7d7d7;']";
$findbeerevenrowdata = "tr.dataTableRow";
break;
$html = scraperWiki::scrape("http://www.ratebeer.com/browsebrewers-A.htm");
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find($findbrewerydata) as $brewerydata)
{
$breweryrecord = getbrewerylink($brewerydata);
$breweryhtmllink = "http://www.ratebeer.com" . $breweryrecord['Brewery Link'];
$breweryhtml = scraperWiki::scrape($breweryhtmllink);
$brewerydom = new simple_html_dom();
$brewerydom->load($breweryhtml);

getbreweryinfo($brewerydom,$breweryrecord);
foreach($brewerydom->find($findbeerodddata) as $data)
{
getbeerdata($data,$breweryrecord['Brewery ID']);
}
foreach($brewerydom->find($findbeerevendata) as $data)
{
foreach($data->find($findbeerevenrowdata) as $TRdata)
{
getbeerdata($TRdata,$breweryrecord['Brewery ID']);
}
}
}


function getbrewerylink($brewerydata){
$brewerylink = $brewerydata->getAttribute('href');
$breweryexplodelink = explode('/', $brewerylink);
$breweryid = $breweryexplodelink[3];
$breweryname = utf8_encode($brewerydata->plaintext);
$breweryrecord = array( 'Brewery ID' => $breweryid, 'Brewery' => $breweryname, 'Brewery Link' => $brewerylink );
return $breweryrecord;
}

function getbreweryinfo($brewerydom,$breweryrecord){
foreach($brewerydom->find("td[@width='130'] a") as $breweryinfo)
{
$link = $breweryinfo->getAttribute("href");
$ismap = strpos($link, "http://maps.google.com");
if ($ismap !== false)
{
$breweryrecord["address"] = utf8_encode($breweryinfo->plaintext);
}
$istel = strpos($link, "tel:");
if ($istel !== false)
{
$breweryrecord["telephone"] = $breweryinfo->plaintext;
}
}
foreach($brewerydom->find("td[@width='130'] span.beerfoot") as $breweryinfo)
{
$breweryrecord["hours"] = $breweryinfo->plaintext;
}
$breweryrecord["blank"] = "";
//print_r($breweryrecord);
scraperwiki::save_sqlite(array('Brewery ID'), $breweryrecord, $table_name="brewerydata");
}

function getbeerdata($data,$breweryid) {
$scrapetime = date(DATE_RFC822);
settype($scrapetime, "string");
$beerinfo = $data->find("td");
$beerlink = $data->find("td a");
$beerotherinfo = 0;
settype($beerotherinfo, "string");
if ($data->find("td span.rip"))
{
$beerotherinfo = $data->find("td span.rip");
$beerotherinfo = stringtest($beerotherinfo[0]->plaintext);
};
if ($beerotherinfo == "0")
{
$a=3;
$b=4;
$c=5;
$d=6;
$e=7;
} elseif ($beerotherinfo == "R"){
$a=4;
$b=5;
$c=6;
$d=7;
$e=8;
} elseif ($beerotherinfo == "A"){
$a=3;
$b="";
$c="";
$d="";
$e=7;
};
$beerlinkhref = $beerlink[0]->getAttribute("href");
$beerexplodelink = explode('/', $beerlinkhref);
$beerid = $beerexplodelink[3];
//preg_match("/[0-9]+/", $beerlinkhref, $beerid);
$beernamearray = explode('/', $beerlinkhref, 4);
$beername = ucwords(str_replace("-", " ", $beernamearray[2]));
$beerrecord = array( 'Beer ID' => $beerid, 'Brewery ID' => $breweryid, 'Beer Name' => $beername, 'Beer Link' => $beerlink[0]->getAttribute("href"), 'ABV' => stringtest($beerinfo[$a]->plaintext), 'Score' => stringtest($beerinfo[$b]->plaintext), 'Overall' => stringtest($beerinfo[$c]->plaintext), 'Style' => stringtest($beerinfo[$d]->plaintext), 'Ratings' => stringtest($beerinfo[$e]->plaintext), 'Scrape' => $scrapetime, 'Other' => $beerotherinfo, 'Blank' =>"");
//print_r($beerrecord);
scraperwiki::save_sqlite(array('Beer ID'), $beerrecord, $table_name="beerdata");
}

function stringtest($test) {
if ($test == ''){
$test = " ";
return $test;
} else {
$test = str_replace("&nbsp;", "", $test);
return $test;
}
}

?>
