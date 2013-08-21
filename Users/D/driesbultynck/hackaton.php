<?php
//url ingeven
//site doorcrawlen > ook sitemap meepakken vanuit robots.txt
//body opvragen
//zoeken naar e-mailadressen (goed en slecht geschreven)
//zoeken naar contactpagina > forms opsporen
//check by url of naam in bio > zoeken naar twitter, linkedin of facebook? > check ook op url
//count ook social shares
//save list by date

//uitbreidingen:
// Adwords scraping example > http://oreilly.com/pub/h/2745
// check buzzstream voor verbeteringen
//Multiple threads via php requests
//timeout functie toevoegen als delay gebruikt wordt? Max x opzoekingen per minuut?
//check if pages have Analytics code > eender welk stats pakket
//sites opzoeken via thema's + in combo met wikipedia structuur etc (zie post) + Google top 10, 20, 30, 40, 50, ... per keyword of thema
//check 404's van pagina
//zoeken naar rich snippets > contact etc...
//zoeken naar comments per pagina? of thema?
//outbound links checken
//nofollow links checken
//interne links checken - dofollow links checken
//backlinks checken
//hubs vinden of clusters advh backlinks etc...
//outbound links tellen om linkpartners te ontdekken
//check for partner pages (en partner keywords in tekst)
// google insights?
//Analytics data koppelen?
//bing & yahoo mogelijheden?

//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'keywords' => 'web analytics, seo', 'url' => 'wijs.be', 'depth' => '2', 'country' => 'belgium', 'lang' => 'nederlands')
);

//stuff we need to ruse
//function to get client id
function searchForId($client, $array) {
   foreach ($array as $key => $val) {
       if ($val['client'] === $client) {
           return $key;
       }
   }
   return null;
}


//Start hacking
//get details data by client
$selectedClient = searchForId('Dries Bultynck', $arrData);
$keywords = $arrData[$selectedClient]['keywords'];
$url = $arrData[$selectedClient]['url'];
$arrKeywords = explode(',',$keywords);
/*
foreach($arrKeywords as $keyword){
    echo($keyword);
}
*/

// scrape emails (@ or at) - of link naar contact pagina + contact gegevens per persoon


// save per date
$now = getdate();
//print_r($now);
$saveDate = $now;
$showDate = $arrWDay[$now['wday']].' - '.$now['mday'].'/'.$now['mon'].'/'.$now['year'].' - '.$now['hours'].':'.$now['minutes'];
//echo($showDate);

function delay(){
    global $minDelay, $maxDelay;    
    $delay = rand($minDelay,$maxDelay);
    sleep($delay);
    //controle voor seconden vertraging
    //$newNow = getdate();
    //echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
}

// auto run on specific days of month etc. > week, per 2 weeks, per month on day x, ... > hour needed?
//$setTermAutoRun = "month + day";

// export als Json om, om te zetten naar html preview, excel export of samenvoegen met GA data?
// ! Stats to compare by date of year, weekday of month, weekday of month per year, per hour per month, per hour per weekday , ...


//scrape top 10 google op keyword
// ! check keywords per keywords per site
// ! check land per land > ook taal per taal?
$html = file_get_contents("http://www.google.be/search?q=wijs&hl=nl&start=0");
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@id='ires']//h3//a") as $node)
{
    delay();
    echo('i = '.$i);
    echo $node->getAttribute("href")."\n";
    //historische data bijhouden van de top 100?
    //hoe sitelinks uitfilteren? tel aantal H3's binnen div?
    //echo $node->nodeValue;
    $i++;
}

//Loop om door pagina's te gaan
//decay ook nodig voor tussen pagina's per 10 url's > Controle voor beginnen met volgende sessie van 10 url's.
/*
for($i=1;$i<=$depth;$i++){
    echo $i;
}
*/

?>

