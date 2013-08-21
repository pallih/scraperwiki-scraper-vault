<?php

//scrape bing? Yahoo?
//http://code.google.com/apis/analytics/docs/articles/gdataAnalyticsAdWords.html


//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'keywords' => 'web analytics, seo', 'url' => 'wijs.be', 'country' => 'belgium', 'lang' => 'nederlands'),
   '1'  => array('client' => 'Dries Bultynck', 'keywords' => 'web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs, web analytics, seo, car, test, wijs', 'url' => 'driesbultynck.be', 'country' => 'netherlands', 'lang' => 'nederlands')
);

//set day of week
// ! expand languages
$arrWDay = array('1' => 'maandag','2' => 'dinsdag','3' => 'woensdag','4' => 'donderdag','5' => 'vrijdag','6' => 'zaterdag','7' => 'zondag',);

//set ccTLD
$arrCCTLD = array('belgium'=>'be', 'netherlands'=>'nl');

//set lang
$arrLang = array('nederlands'=>'nl');

//function to get client id
function searchForId($client, $array) {
   foreach ($array as $key => $val) {
       if ($val['client'] === $client) {
           return $key;
       }
   }
   return null;
}

//get details data by client
$selectedClient = searchForId('Wijs', $arrData);
$keywords = $arrData[$selectedClient]['keywords'];
$url = $arrData[$selectedClient]['url'];
$country = $arrData[$selectedClient]['country'];
$CCTLD = $arrCCTLD[$country];
$language = $arrData[$selectedClient]['lang'];
$lng = $arrLang[$language];
$arrKeywords = explode(',',$keywords);

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

// ! Stats to compare by date of year, weekday of month, weekday of month per year, per hour per month, per hour per weekday , ...

//scrape top 10 google op keyword
// ! check keywords per keywords per site
// ! check land per land > ook taal per taal?

foreach($arrKeywords as $keyword){
    //delay();
    $queryUrl= "http://www.google.".$CCTLD."/search?q=".urlencode($keyword)."&hl=".$lng."&start=0&pws=0";
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
echo $html."\n"; //> opslaan in database en finito
}

//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=uEkZUOrNOIi5hAeaiYHoDA&start=0&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=2EkZUIfKK9OZhQen6YDgAQ&start=10&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=AEoZULmTM5SYhQe6woHYDQ&start=20&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639

?>

