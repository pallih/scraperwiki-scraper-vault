<?php

//http://www.bing.com/search?q=site%3Alinkedin.com+%22belgium%22+wijs+-dir+%22know+in+common%22&go=&qs=n&form=QBRE&pq=site%3Alinkedin.com+%22belgium%22+wijs+-dir+%22know+in+common%22&sc=0-0&sp=-1&sk=
//http://www.booleanblackbelt.com/2011/06/update-your-linkedin-x-ray-searches-for-location-names/
//http://www.booleanblackbelt.com/2009/03/x-ray-searching-facebook-for-sourcing/
//http://www.booleanblackbelt.com/2009/02/free-linkedin-search-internal-vs-x-ray/

//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'urls' => 'wijs.be', 'depth' => '0'),
   '1'  => array('client' => 'Catena', 'urls' => 'cyclingnews.com', 'depth' => '2')
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
$selectedClient = searchForId('Catena', $arrData);
$url = $arrData[$selectedClient]['urls'];
$arrUrls = explode(',',$url);

function delay(){
    global $minDelay, $maxDelay;    
    $delay = rand($minDelay,$maxDelay);
    sleep($delay);
    //controle voor seconden vertraging
    //$newNow = getdate();
    //echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
}

//scrape top 10 bing voor linked urls
//run door top 100
//run door set met links 
/*
foreach($arrUrls as $urls){

}
*/

$html = file_get_contents("http://www.bing.com/search?q=linkfromdomain%3A".$url."+-".$url."&first=1");
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@class='sb_tlst']//h3//a") as $node)
{
    //delay();
    echo $i.'. ' . $node->getAttribute("href")."\n";
    //echo $node->nodeValue;
    $i++;
}

?>

<?php

//http://www.bing.com/search?q=site%3Alinkedin.com+%22belgium%22+wijs+-dir+%22know+in+common%22&go=&qs=n&form=QBRE&pq=site%3Alinkedin.com+%22belgium%22+wijs+-dir+%22know+in+common%22&sc=0-0&sp=-1&sk=
//http://www.booleanblackbelt.com/2011/06/update-your-linkedin-x-ray-searches-for-location-names/
//http://www.booleanblackbelt.com/2009/03/x-ray-searching-facebook-for-sourcing/
//http://www.booleanblackbelt.com/2009/02/free-linkedin-search-internal-vs-x-ray/

//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec

//data
$arrData = array(
   '0'  => array('client' => 'Wijs', 'urls' => 'wijs.be', 'depth' => '0'),
   '1'  => array('client' => 'Catena', 'urls' => 'cyclingnews.com', 'depth' => '2')
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
$selectedClient = searchForId('Catena', $arrData);
$url = $arrData[$selectedClient]['urls'];
$arrUrls = explode(',',$url);

function delay(){
    global $minDelay, $maxDelay;    
    $delay = rand($minDelay,$maxDelay);
    sleep($delay);
    //controle voor seconden vertraging
    //$newNow = getdate();
    //echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
}

//scrape top 10 bing voor linked urls
//run door top 100
//run door set met links 
/*
foreach($arrUrls as $urls){

}
*/

$html = file_get_contents("http://www.bing.com/search?q=linkfromdomain%3A".$url."+-".$url."&first=1");
$dom = new DOMDocument();
@$dom->loadHTML($html);
$x = new DOMXPath($dom);
$i=1;
foreach($x->query("//div[@class='sb_tlst']//h3//a") as $node)
{
    //delay();
    echo $i.'. ' . $node->getAttribute("href")."\n";
    //echo $node->nodeValue;
    $i++;
}

?>

