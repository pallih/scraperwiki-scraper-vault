<?php

//http://www.lambris.com/index.asp

// !!!!!!!
// chrome extensie in JS gieten > mouse over voor snelle weergave site?
// !!!!!!!

//use only selected operators 
//add/delete your operators + resetbutton > add the list with standard operators (excl. duplicates) > doorloop de lijst met operators en lijst resultaten op in 1 keer
//standard list operators
//set delay > if delay is 0 > wait random (10 sec) between assignment
// ajax output mogelijk?

/*
http://www.html-form-guide.com/php-form/php-form-select.html
//http://stackoverflow.com/questions/5249825/auto-populate-a-select-box-using-an-array-in-php
http://www.html-form-guide.com/php-form/php-form-checkbox.html
*/

$arrOwnOperatorsEN=array();
$arrOwnOperatorsNL=array();
$arrOwnOperatorsFR=array();
$arrOwnOperatorsDE=array();

$reset='1';
$exclDuplicateUrls = '1';
$exclDuplicateDomains = '0';
$markDuplicateUrls = '0';
$markDuplicateDomains = '0';

$arrOperatorsEN = array(
    '0' => '',
    '1' => 'submit site',
    '2' => 'submit url',
    '3' => 'intitle:directory',
    '4' => 'intitle:resources',
    '5' => 'directory list',
    '6' => 'intitle:list',
    '7' => 'inurl:list',
    '8' => 'inurl:directory',
    '9' => 'inurl:resources',
    '10' => 'add url',
    '11' => 'submit url',
    '12' => 'suggest url',
    '13' => 'submit a site',
    '14' => 'submit your site',
    '15' => 'add a url',
    '16' => 'add a site',
    '17' => 'add listing',
    '18' => 'add your listing',
    '19' => 'submit a listing',
    '20' => 'submit your website',
    '21' => 'press release',
    '22' => 'news release',
    '23' => 'prweb',
    '24' => 'reuters',
    '25' => 'associated press',
    '26' => 'for immediate release',
    '27' => 'directory'
);

//press + local cities
//inurl:forum music new releases

$arrOperatorsNL = array(
    '0' => '',
    '1' => 'site toevoegen',
    '2' => 'website toevoegen',
    '3' => 'intitle:directory',
    '4' => 'intitle:resources',
    '5' => 'directory lijst',
    '6' => 'directory lijst',
    '7' => 'intitle:lijst',
    '8' => 'inurl:lijst',
    '9' => 'inurl:directory',
    '10' => 'inurl:resources',
    '11' => 'url toevoegen',
    '12' => 'submit url'
);

$arrCCTLD = array('wereldwijd'=>'com','belgie'=>'be', 'nederland'=>'nl', 'nederland'=>'nl', 'frankrijk'=>'fr','uk'=>'co.uk', 'duitsland'=>'de');
$arrLang = array('engels'=>'en','nederlands'=>'nl','frans'=>'fr','duits'=>'de');
$arrDepth = array('1' => '0','2' => '10','3' => '20','4' => '30','5' => '40','6' => '50','7' => '60','8' => '70','9' => '80','10' => '90','11' => '280');

//settings
$minDelay='3'; //sec
$maxDelay='8'; //sec
//$keyword = 'site:http://www.deceuninck.be';
$keyword = 'inurl:forum volvo';
$operator = $arrOperatorsNL['0'];
$depth = 5;
$country = 'belgie';
$CCTLD = $arrCCTLD[$country];
$language = 'nederlands';
$lng = $arrLang[$language];
//$arrKeywords = explode(',',$keywords);
$stack=array();

function delay(){
    global $minDelay, $maxDelay, $delay;
    if($minDelay=='0'){
        //echo "werkt";
        //wait();
    }else{ 
        $delay = rand($minDelay,$maxDelay);
    }
    sleep($delay);
}

function wait(){
    sleep(rand(10,15));
    //controle voor seconden vertraging
    $newNow = getdate();
    echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
    //break;
}

$endDepth = $arrDepth[$depth];
if($endDepth=='0'){
    $runDepth=$endDepth;
}
else{
    global $keyword, $operator;
    for($i=0;$i<$endDepth+1;$i += 10){
        $runDepth = $i;
        x($CCTLD,$lng,$runDepth,$keyword,$operator);
    }
}

function x($CCTLD,$lng,$runDepth,$keyword,$operator){
global $message, $pattern, $stack;
$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode(''.$keyword.' "'.$operator.'"').'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
//$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode($keyword).'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
//echo $queryUrl."\n";
echo 'Query: '.$keyword.' "'.$operator.'" - Start '.$runDepth."\n";
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
    delay();
    $url = $node->getAttribute('href');
    $url = trim($url, "/url?q=");
    $url = current(explode('&sa', $url));
    array_push($stack, $url);
    //echo $url."\n";
    $i++;
    }
}

checkSettings($exclDuplicateUrls,$stack);

function checkSettings($exclDuplicateUrls,$stack){
//mark duplicates or delete duplicates > full url or domain option 
global $exclDuplicateUrls, $stack;
    if($exclDuplicateUrls == '1'){
       print_r(array_unique($stack));
    }else{
       print_r($stack);  
    }      
}

?>
<?php

//http://www.lambris.com/index.asp

// !!!!!!!
// chrome extensie in JS gieten > mouse over voor snelle weergave site?
// !!!!!!!

//use only selected operators 
//add/delete your operators + resetbutton > add the list with standard operators (excl. duplicates) > doorloop de lijst met operators en lijst resultaten op in 1 keer
//standard list operators
//set delay > if delay is 0 > wait random (10 sec) between assignment
// ajax output mogelijk?

/*
http://www.html-form-guide.com/php-form/php-form-select.html
//http://stackoverflow.com/questions/5249825/auto-populate-a-select-box-using-an-array-in-php
http://www.html-form-guide.com/php-form/php-form-checkbox.html
*/

$arrOwnOperatorsEN=array();
$arrOwnOperatorsNL=array();
$arrOwnOperatorsFR=array();
$arrOwnOperatorsDE=array();

$reset='1';
$exclDuplicateUrls = '1';
$exclDuplicateDomains = '0';
$markDuplicateUrls = '0';
$markDuplicateDomains = '0';

$arrOperatorsEN = array(
    '0' => '',
    '1' => 'submit site',
    '2' => 'submit url',
    '3' => 'intitle:directory',
    '4' => 'intitle:resources',
    '5' => 'directory list',
    '6' => 'intitle:list',
    '7' => 'inurl:list',
    '8' => 'inurl:directory',
    '9' => 'inurl:resources',
    '10' => 'add url',
    '11' => 'submit url',
    '12' => 'suggest url',
    '13' => 'submit a site',
    '14' => 'submit your site',
    '15' => 'add a url',
    '16' => 'add a site',
    '17' => 'add listing',
    '18' => 'add your listing',
    '19' => 'submit a listing',
    '20' => 'submit your website',
    '21' => 'press release',
    '22' => 'news release',
    '23' => 'prweb',
    '24' => 'reuters',
    '25' => 'associated press',
    '26' => 'for immediate release',
    '27' => 'directory'
);

//press + local cities
//inurl:forum music new releases

$arrOperatorsNL = array(
    '0' => '',
    '1' => 'site toevoegen',
    '2' => 'website toevoegen',
    '3' => 'intitle:directory',
    '4' => 'intitle:resources',
    '5' => 'directory lijst',
    '6' => 'directory lijst',
    '7' => 'intitle:lijst',
    '8' => 'inurl:lijst',
    '9' => 'inurl:directory',
    '10' => 'inurl:resources',
    '11' => 'url toevoegen',
    '12' => 'submit url'
);

$arrCCTLD = array('wereldwijd'=>'com','belgie'=>'be', 'nederland'=>'nl', 'nederland'=>'nl', 'frankrijk'=>'fr','uk'=>'co.uk', 'duitsland'=>'de');
$arrLang = array('engels'=>'en','nederlands'=>'nl','frans'=>'fr','duits'=>'de');
$arrDepth = array('1' => '0','2' => '10','3' => '20','4' => '30','5' => '40','6' => '50','7' => '60','8' => '70','9' => '80','10' => '90','11' => '280');

//settings
$minDelay='3'; //sec
$maxDelay='8'; //sec
//$keyword = 'site:http://www.deceuninck.be';
$keyword = 'site:zwembadstore.be';
$operator = $arrOperatorsNL['0'];
$depth = 10;
$country = 'belgie';
$CCTLD = $arrCCTLD[$country];
$language = 'nederlands';
$lng = $arrLang[$language];
//$arrKeywords = explode(',',$keywords);
$stack=array();

function delay(){
    global $minDelay, $maxDelay, $delay;
    if($minDelay=='0'){
        //echo "werkt";
        //wait();
    }else{ 
        $delay = rand($minDelay,$maxDelay);
    }
    sleep($delay);
}

function wait(){
    sleep(rand(10,15));
    //controle voor seconden vertraging
    $newNow = getdate();
    echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
    //break;
}

$endDepth = $arrDepth[$depth];
if($endDepth=='0'){
    $runDepth=$endDepth;
}
else{
    global $keyword, $operator;
    for($i=0;$i<$endDepth+1;$i += 10){
        $runDepth = $i;
        x($CCTLD,$lng,$runDepth,$keyword,$operator);
    }
}

function x($CCTLD,$lng,$runDepth,$keyword,$operator){
global $message, $pattern, $stack;
$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode(''.$keyword.' "'.$operator.'"').'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
//$queryUrl= 'http://www.google.'.$CCTLD.'/search?q='.urlencode($keyword).'&hl='.$lng.'&start='.$runDepth.'&pws=0'.'\n';
//echo $queryUrl."\n";
echo 'Query: '.$keyword.' "'.$operator.'" - Start '.$runDepth."\n";
$html = file_get_contents($queryUrl);
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@id='ires']//h3//a") as $node)
    {
    delay();
    $url = $node->getAttribute('href');
    $url = trim($url, "/url?q=");
    $url = current(explode('&sa', $url));
    array_push($stack, $url);
    //echo $url."\n";
    $i++;
    }
}

checkSettings($exclDuplicateUrls,$stack);

function checkSettings($exclDuplicateUrls,$stack){
//mark duplicates or delete duplicates > full url or domain option 
global $exclDuplicateUrls, $stack;
    if($exclDuplicateUrls == '1'){
       print_r(array_unique($stack));
    }else{
       print_r($stack);  
    }      
}

?>
