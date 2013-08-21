<?php
//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec
$runDepth="";
$i=0;
$j=1;
//data
$arrData = array(
   '0'  => array('client' => 'Kardex', 'keywords' => 'pallet racking', 'url' => 'kardex-stow.com', 'country' => 'uk', 'lang' => 'engels', 'depth' => '3'),
   '1'  => array('client' => 'Dries', 'keywords' => 'Dries, seo', 'url' => 'driesbultynck.be', 'country' => 'belgium', 'lang' => 'nederlands', 'depth' => '10'),
'2'  => array('client' => 'Braem', 'keywords' => 'site:openminds.be', 'url' => 'braem.com', 'country' => 'belgium', 'lang' => 'nederlands', 'depth' => '11')
);

//set day of week
// ! expand languages
$arrWDay = array('1' => 'maandag','2' => 'dinsdag','3' => 'woensdag','4' => 'donderdag','5' => 'vrijdag','6' => 'zaterdag','7' => 'zondag',);

//set ccTLD
$arrCCTLD = array('belgium'=>'be', 'netherlands'=>'nl', 'uk'=>'co.uk');

//set lang
$arrLang = array('nederlands'=>'nl', 'engels'=>'en');

//set depth
$arrDepth = array('1' => '0','2' => '10','3' => '20','4' => '30','5' => '40','6' => '50','7' => '60','8' => '70','9' => '80','10' => '90','11' => '690');

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
$selectedClient = searchForId('Braem', $arrData);
$keywords = $arrData[$selectedClient]['keywords'];
$url = $arrData[$selectedClient]['url'];
$country = $arrData[$selectedClient]['country'];
$CCTLD = $arrCCTLD[$country];
$language = $arrData[$selectedClient]['lang'];
$lng = $arrLang[$language];
//$arrKeywords = explode(',',$keywords);
$arrKeywords = preg_split('/[,]+/', $keywords);
//print_r($arrKeywords);

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

loopThroughKeywords();

function loopThroughKeywords(){
global $arrKeywords;
foreach ($arrKeywords as $key => $keyword) {
    //print "$key = $keyword\n";
    loop($keyword);
}
}

function loop($keyword){
global $endDepth, $CCTLD, $lng, $url, $i;
if($endDepth=='0'){
    $runDepth=$endDepth;
}
else{
    for($i=0;$i<$endDepth+1;$i += 10){
        $runDepth = $i;
        x($runDepth,$keyword);
/*
        $queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode($keyword).'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
        $html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
    delay();
    echo($keyword.' > i = '.$i."\n");
    echo $node->getAttribute('href');
    
    if(preg_match('/'.$url.'/',$node->getAttribute('href'))){
        echo($keyword.' > i = '.$i. ' -> found on '.$i."\n");     
        //break;
    }
    else{
        echo($keyword.' > i = '.$i."\n");
        echo 'not found on '.$runDepth+$i."\n";
    }
     
       $i++;
    }
    }
    }
*/
}
}}

/*
while(!$end && $depth<$endDepth+1){
            $runDepth = $depth;
                $link = scraperwiki::scrape("http://www.notfound.org/participants?page=".$runDepth);
                       $html = str_get_html($link);
                        $urls = getLinks($html);
                         $depth+=10;
                        if($endDepth=='0'){
                            $runDepth = $endDepth;
                            $end = true;
                        }
                    }
                    if(sizeof($urls) > 0){
                        foreach($urls as $key=>$value){
                            echo $value."\n";
                        }
                    }else{
                        echo "No match found";
                    }
*/

function x($runDepth,$keyword){
global $CCTLD, $lng, $url,$j;
$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode($keyword).'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
        $html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;

foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
    //delay();
    //echo($keyword.' > i = '.$i."\n");
    //echo $node->getAttribute('href');
    
    if(preg_match('/'.$url.'/',$node->getAttribute('href'))){
        // nood aan 2e teller die nummer onthoud van ranking (volgens pagina)
        echo($keyword.' > i = '.$i. ' -> found on '.$j."\n");
        //$j=1;   
        //break;
    }
    else{
        //echo($keyword.' > i = '.$i."\n");
        echo($keyword.' not found on - j = '.$j."\n");
    }
     
       $i++;
       $j++;
    }
    }

//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=uEkZUOrNOIi5hAeaiYHoDA&start=0&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=2EkZUIfKK9OZhQen6YDgAQ&start=10&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639
//https://www.google.be/#q=wijs/&hl=nl&safe=off&pws=0&prmd=imvns&ei=AEoZULmTM5SYhQe6woHYDQ&start=20&sa=N&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&fp=c29742016ea24ed5&biw=1278&bih=639

//historische data bijhouden van de top 100?
    //hoe sitelinks uitfilteren? tel aantal H3s binnen div?

?>

