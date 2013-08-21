<?php
//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec
$statusKeyword = '0';

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'keywords' => 'responsive web design, seo', 'url' => 'wijs.be', 'country' => 'belgium', 'lang' => 'nederlands', 'depth' => '10'),
   '1'  => array('client' => 'Dries Bultynck', 'keywords' => 'web analytics, seo', 'url' => 'driesbultynck.be', 'country' => 'netherlands', 'lang' => 'nederlands', 'depth' => '2')
);

//set day of week
// ! expand languages
$arrWDay = array('1' => 'maandag','2' => 'dinsdag','3' => 'woensdag','4' => 'donderdag','5' => 'vrijdag','6' => 'zaterdag','7' => 'zondag',);

//set ccTLD
$arrCCTLD = array('belgium'=>'be', 'netherlands'=>'nl');

//set lang
$arrLang = array('nederlands'=>'nl');

//set depth
$arrDepth = array('1' => '0','2' => '10','3' => '20','4' => '30','5' => '40','6' => '50','7' => '60','8' => '70','9' => '80','10' => '90');

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

// export als Json om, om te zetten naar html preview, excel export of samenvoegen met GA data?
// ! Stats to compare by date of year, weekday of month, weekday of month per year, per hour per month, per hour per weekday , ...


//scrape top 10 google op keyword
// ! check keywords per keywords per site
// ! check land per land > ook taal per taal?

$depth = $arrData[$selectedClient]['depth'];
echo 'depth uit arrData: '.$depth."\n";
$endDepth = $arrDepth[$depth];
echo 'depth uit arrDepth: '.$endDepth."\n";
if($endDepth=='0'){
    $runDepth=$endDepth;
}
else{
    for($i=0;$i<$endDepth+1;$i += 10){
        $runDepth = $i;
        loopThroughPages($runDepth);
    }
}

function loopThroughPages($runDepth){
    global $arrKeywords,$CCTLD,$keyword,$lng,$url,$statusKeyword;
    foreach($arrKeywords as $keyword){
        //echo 'status keyword: '.$statusKeyword;
        print_r($arrKeywords);
        
        if($statusKeyword=='0'){
            x($CCTLD,$keyword,$lng,$url,$runDepth);
        }else{
            $arrKeywords = array_shift($arrKeywords);
           break;
        }
    }
}

function x($CCTLD,$keyword,$lng,$url,$runDepth){
global $statusKeyword;
echo 'resultaten keyword '. $keyword.' :';
$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode($keyword).'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
    //delay();
    //echo('i = '.$i. ' -> ');
    if(preg_match('/'.$url.'/',$node->getAttribute('href'))){
        //echo 'ja';
        // gevonden in top 10
        echo $keyword. ' found on '.$i."\n";
        // of gevonden later > + depth erbij tellen
        //echo $keyword. ' found on '.$runDepth.$i."\n";

        $statusKeyword == '1';
        //echo 'Status: '.$statusKeyword."\n";
        //als gevonden break, anders niet
        break;
        //continue;
    }
    else{
        echo 'not found op '.$runDepth+$i."\n";
    }
    
        //status found of niet > echo $keyword. ' op '.$i;
    
    //historische data bijhouden van de top 100?
    //hoe sitelinks uitfilteren? tel aantal H3s binnen div?
    //echo $node->nodeValue;
     
       $i++;
    }
}

//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=uEkZUOrNOIi5hAeaiYHoDA&start=0&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=2EkZUIfKK9OZhQen6YDgAQ&start=10&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=AEoZULmTM5SYhQe6woHYDQ&start=20&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639

?>

