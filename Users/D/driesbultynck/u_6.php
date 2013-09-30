<?php
//settings
//http://code.google.com/apis/analytics/docs/articles/gdataAnalyticsAdWords.html

$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'keywords' => 'web analytics, seo', 'url' => 'wijs.be', 'depth' => '2', 'country' => 'belgium', 'lang' => 'nederlands'),
   '1'  => array('client' => 'Dries Bultynck', 'keywords' => 'web analytics, seo', 'url' => 'driesbultynck.be', 'depth' => '2', 'country' => 'belgium', 'lang' => 'nederlands')
);

//set day of week
// ! expand languages
$arrWDay = array('1' => 'maandag','2' => 'dinsdag','3' => 'woensdag','4' => 'donderdag','5' => 'vrijdag','6' => 'zaterdag','7' => 'zondag',);

//set ccTLD
$arrCCTLD = array('belgium'=>'be');

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

//herken url met matched url > zo ja > schrijf weg in array met keyword + ranking


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
$html = file_get_contents("http://www.google.com/search?q=used%20mercedes%20benz%20truck&hl=en&start=0");
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
//echo $html; //> opslaan in database en finito

/*
// alle links > betaald + organisch
foreach($x->query("//h3//a") as $node)
{
    //delay();
    //echo('i = '.$i);
    echo $node->getAttribute("href")."\n";
    //historische data bijhouden van de top 100?
    //hoe sitelinks uitfilteren? tel aantal H3's binnen div?
    //echo $node->nodeValue;
    $i++;
}
*/

//Loop om door pagina's te gaan
//decay ook nodig voor tussen pagina's per 10 url's > Controle voor beginnen met volgende sessie van 10 url's.
/*
for($i=1;$i<=$depth;$i++){
    echo $i;
}
*/

//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=uEkZUOrNOIi5hAeaiYHoDA&start=0&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=2EkZUIfKK9OZhQen6YDgAQ&start=10&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=AEoZULmTM5SYhQe6woHYDQ&start=20&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639

?>

<?php
//settings
//http://code.google.com/apis/analytics/docs/articles/gdataAnalyticsAdWords.html

$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'keywords' => 'web analytics, seo', 'url' => 'wijs.be', 'depth' => '2', 'country' => 'belgium', 'lang' => 'nederlands'),
   '1'  => array('client' => 'Dries Bultynck', 'keywords' => 'web analytics, seo', 'url' => 'driesbultynck.be', 'depth' => '2', 'country' => 'belgium', 'lang' => 'nederlands')
);

//set day of week
// ! expand languages
$arrWDay = array('1' => 'maandag','2' => 'dinsdag','3' => 'woensdag','4' => 'donderdag','5' => 'vrijdag','6' => 'zaterdag','7' => 'zondag',);

//set ccTLD
$arrCCTLD = array('belgium'=>'be');

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

//herken url met matched url > zo ja > schrijf weg in array met keyword + ranking


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
$html = file_get_contents("http://www.google.com/search?q=used%20mercedes%20benz%20truck&hl=en&start=0");
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
//echo $html; //> opslaan in database en finito

/*
// alle links > betaald + organisch
foreach($x->query("//h3//a") as $node)
{
    //delay();
    //echo('i = '.$i);
    echo $node->getAttribute("href")."\n";
    //historische data bijhouden van de top 100?
    //hoe sitelinks uitfilteren? tel aantal H3's binnen div?
    //echo $node->nodeValue;
    $i++;
}
*/

//Loop om door pagina's te gaan
//decay ook nodig voor tussen pagina's per 10 url's > Controle voor beginnen met volgende sessie van 10 url's.
/*
for($i=1;$i<=$depth;$i++){
    echo $i;
}
*/

//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=uEkZUOrNOIi5hAeaiYHoDA&start=0&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=2EkZUIfKK9OZhQen6YDgAQ&start=10&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=AEoZULmTM5SYhQe6woHYDQ&start=20&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639

?>

