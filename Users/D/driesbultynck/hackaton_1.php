<?php
/*********************************************************** to do ********************************************************/
//html pagina voor filtering per klant & date
//html pagina voor add klant scraping
//voorzie keuze veld (braaf zijn = delay functie)
//niveau's instellen? > niet te diep of blijft eeuwige loop

//http://www.planckendael.be/ > at en dot

//data
$arrData = array(
   '0'  => array('klant' => 'Wijs', 'thema' => 'online marketing', 'keywords' => 'seo, sea, web analytics', 'sites' => 'proximedia.be, reference.be, the-aim.be')
);

//klant opzoeken op basis van naam
function searchForId($client, $array) {
   foreach ($array as $key => $val) {
       if ($val['klant'] === $client) {
           return $key;
       }
   }
   return null;
}
$selectedClient = searchForId('Wijs', $arrData);
$thema = $arrData[$selectedClient]['thema'];
$keywords = $arrData[$selectedClient]['keywords'];
$sites = $arrData[$selectedClient]['sites'];
$arrKeywords = explode(',',$keywords);
$arrSites = explode(',',$sites);


/*********************************************************** to do ********************************************************/
//delay function toevoegen?
//settings
$minDelay='5'; //sec
$maxDelay='10'; //sec

function delay(){
    global $minDelay, $maxDelay;    
    $delay = rand($minDelay,$maxDelay);
    sleep($delay);
    //controle voor seconden vertraging
    //$newNow = getdate();
    //echo $newNow['hours'].':'.$newNow['minutes'].':'.$newNow['seconds'];
}

/*********************************************************** to do ********************************************************/
//alternatief > indexed pages vanuit google scrapen met site:
//loop door sites om de scraping te doen
/*
$depth= count($arrSites);
$j=0;
while($j<$depth){
    $homepage = $arrSites[$j];
    scrapeHomepage($homepage);
    $j++;
}

of 

//http://php.net/manual/en/control-structures.while.php
/*
$finished = false;                       
while (! $finished ):                  
  // do stuff
  if (voorwaarde){
    $finished = true;                   
  }
endwhile;
*/


/*
    //header checker bij redirect
    $headers = get_headers('http://www.'.$homepage);
    print_r($headers);
switch (substr($headers[0], 9, 3)) {
    case 302:
        $tempHomepage = $headers[5];
        break;
    case 301:
        $tempHomepage = $headers[5];
        break;
    case 404:
        exit("De homepage geeft een 404 header terug. Probeer eens een andere start url.");
        break;
    }
// wat met redirects naar zonder basehref urls?
echo $tempHomepage;

*/

$homepage = $arrSites[0];
scrapeHomepage($homepage);

function scrapeHomepage($homepage){
    //geen https ondersteuning > xpath uitzoeken > Regex is nogal complex
    //set_time_limit(10);
    //goedkope oplossing domain > header check nog doen
    $newHomepage = 'http://www.'.$homepage;
    $html = file_get_contents($newHomepage);
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    //lege velden nog uit filteren
    //foreach($x->query("//a[((contains(@href,'".$homepage."') or not(contains(@href, 'http://'))) and not(contains(@href, 'https://'))) and not(contains(@href, 'mailto:')) and not(contains(@href, '#'))]/@href") as $node){
    foreach($x->query("//a[contains(@href,'".$homepage."') and not(contains(@href, 'mailto:')) and not(contains(@href, '#'))]/@href") as $node){
        if (!empty($node)) {
            $arrBaseUrls[] = $node->nodeValue;
            //echo $node->nodeValue.', ';
        }else{
            echo 'leeg';
        }
    } 
    echo count($arrBaseUrls) .' pagina\'s gevonden op niveau 1<br/>';
    //print_r($arrBaseUrls);
    scrape($arrBaseUrls, $homepage);
}

function scrape($arrBaseUrls, $homepage){
    //scrapeUrl($arrBaseUrls[0],$homepage);
    $depth= count($arrBaseUrls);
    for($i=0;$i<$depth;$i++){
        //echo $i.' - '.$arrBaseUrls[$i].', ';
        scrapeUrl($arrBaseUrls[$i],$homepage);
    }
}

function scrapeUrl($url, $homepage){ 
    //check of url basehref bevat
    /*
    $match = 'http://www.'.$homepage;
    $pos = strpos($url, $match);
    if($pos===true){
        $url = $url;
    }else{

        //if(preg_match('/^([^.]+)\.{0,4}$/',$url)){     
            //$url = 'http://www.'.$homepage.$url;}
       
        if(preg_match('/^([^.]+)\./',$url)){     
            $url = $url;
        }elseif(substr($url,0,1)=='/'){
            $url = 'http://www.'.$homepage.$url;
        }else{
            $url = 'http://www.'.$homepage.'/'.$url;   
        }
    }
*/
    $html = file_get_contents($url);
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    //foreach($x->query("//a[((contains(@href,'".$homepage."') or not(contains(@href, 'http://'))) and not(contains(@href, 'https://'))) and not(contains(@href, 'mailto:')) and not(contains(@href, '#'))]/@href") as $node){
    foreach($x->query("//a[contains(@href,'".$homepage."') and not(contains(@href, 'mailto:')) and not(contains(@href, '#'))]/@href") as $node){
        if (!empty($node)) {
            global $arrAllUrls;
            $arrAllUrls[] = $node->nodeValue;
            //echo $node->nodeValue;
            //cleanAllUrls($arrAllUrls);
            foreach(array_unique($arrAllUrls) as $v){
        if($v){
            $arrClean[] = $v;
        }else{
            array_pop($arrAllUrls);
        }
    }
        }else{
            echo 'leeg';
        }
    } 
    print_r($arrAllUrls);
    //echo count($arrAllUrls) .' pagina\'s gevonden op niveau 2 (niet ontdubbeld)<br/>';
    //echo count($arrClean) .' pagina\'s resterend op niveau 2 (ontdubbeld)<br/>';
}

function cleanAllUrls(&$arrAllUrls){
    global $arrClean;
    //$last_key = end(array_keys($arrAllUrls));
    foreach(array_unique($arrAllUrls) as $v){
        if($v){
            $arrClean[] = $v;
        }else{
            array_pop($arrAllUrls);
        }
    }
    //print_r($arrAllUrls);
}

//scrapeEmails($arrClean);

function scrapeEmails(&$arrClean){
    //scrapeUrl($arrClean[0]);
    $depth= count($arrClean);
    for($i=0;$i<$depth;$i++){
        //echo $i.' - '.$arrClean[$i].', ';
        scrapeUrlForEmails($arrClean[$i]);
    }
}

function scrapeUrlForEmails($url){
    $html = file_get_contents($url);
    $dom = new DOMDocument();
    @$dom->loadHTML($html);
    $x = new DOMXPath($dom);
    foreach($x->query("//*[starts-with(@href, 'mailto:') or (contains(text(),'@') and not(contains(text(), '@import')) and not(contains(@href, 'css')))]") as $node){
        //delay();
        if (!empty($node)) {
            //echo $node->nodeValue;
            global $arrAllEmails;
            $arrAllEmails[]=$node->nodeValue;
        }else{
            echo 'leeg';
        }
    }
}

//cleanAllEmails($arrAllEmails);

function cleanAllEmails(&$arrAllEmails){
    global $arrCleanEmails;
    foreach(array_unique($arrAllEmails) as $v){
        if($v){
            $arrCleanEmails[] = $v;
        }
    }
    //print_r($arrCleanEmails);
    echo implode(", ", $arrCleanEmails);
}


/*********************************************************** to do ********************************************************/
//save list by date & thema
//dag om te saven van de lijst
//$now = getdate();
//print_r($now);
//$saveDate = $now;


/*********************************************************** Gevezer ********************************************************/
//raw html scraping
//http://stackoverflow.com/questions/3470332/scrape-email-addresses
/*
$newlines = array("\t","\n","\r","\x20\x20","\0","\x0B");
$content = str_replace($newlines, "", html_entity_decode($html));
$start = strpos($content, '<body>');
$end = strpos($content, '</body>');
$data = substr($content, $start, $end-$start);
$pattern = '#a[^>]+href="mailto:([^"]+)"[^>]*?>#is';
preg_match_all($pattern, $data, $matches);
foreach ($matches[1] as $key => $email) {
    $emails[] = $email;
}
echo implode(', ', $emails );
*/

//http://stackoverflow.com/questions/10102642/parse-text-email-addresses-using-xpath-not-astartswithhref-mailto
//http://www.crccheck.com/blog/xpath-to-find-email-address-links/
//http://stackoverflow.com/questions/7654414/xpath-regex-combined-with-preg-match > Oplossing voor php:functionString('preg_match', '/selected/', @class

//nog selectie nodig voor at dot adressen of combinatie at . adressen > gebruik url van site?
//link naar contact pagina + contact gegevens per persoon

/*
$nodes = $x->query(sprintf("//*[starts-with(@href, 'mailto:') or contains(text(),'@')]"));
if ($nodes) {
    printf('niet leeg');
} else {
    printf('leeg');
}
*/

/*
$arrDuplicate = array ('http://www.proximedia.be','http://www.proximedia.be','http://www.proximedia.be/',1,3,"",5);
print_r($arrDuplicate);
 foreach(array_unique($arrDuplicate) as $v){
  if($v){$arrRemoved[] = $v;  }}
print_r($arrRemoved);
*/


/*
traverse($home,0);
function traverse($url,$depth)
{
if($depth>1)return;
$html = file_get_contents($url);
foreach($html->find('a') as $element)
{
    $nurl = $element->href;
    echo $nurl."<br>";
    traverse($nurl,$depth+1);
}
}
*/

//lijst de unieke emailadressen op voor de totale website
        //http://www.blog.highub.com/php/php-core/php-traversing-arrays/
        //http://www.coursesweb.net/php-mysql/multidimensional-array-functions
        //http://stackoverflow.com/questions/3630348/php-code-to-traverse-through-a-html-file-to-find-all-the-images-in-there
        //https://www.google.be/webhp?sourceid=chrome-instant&ie=UTF-8&ion=1#hl=nl&safe=off&output=search&sclient=psy-ab&q=php%20traverse%20example&oq=&gs_l=&pbx=1&fp=ebcb5a1a42fb26ac&ion=1&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&biw=1275&bih=639&pws=0 

?>

