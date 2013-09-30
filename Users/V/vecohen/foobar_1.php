<?php
/**
* retrieve OG data
* @param (string) html
* @author Vincent Cohen
*/

function getFacebookLikes($strUrl) {
 
    $strJson = file_get_contents('http://graph.facebook.com/?ids=' . $strUrl);
    $objJson = json_decode($strJson, true);
     
    foreach($objJson as $key =>$val){
  
        if(isset($objJson[$key]["shares"])){
            return intval( $objJson[$key]['shares'] );
        }
    }
}

//    get twitter shares
function getTwitterShares($strUrl){
    
    $strJson = file_get_contents("http://urls.api.twitter.com/1/urls/count.json?url=" . $strUrl);
    $objJson = json_decode($strJson);

    return $objJson->count;
}

function parseOpenGraph($HTML) {
    $old_libxml_error = libxml_use_internal_errors(true);

    $doc = new DOMDocument();
    $doc->loadHTML($HTML);

    $values = array();
    
    libxml_use_internal_errors($old_libxml_error);

    $tags = $doc->getElementsByTagName('meta');
    if (!$tags || $tags->length === 0) {
        return false;
    }

    $nonOgDescription = null;
    
    foreach ($tags as $tag) {
        if ($tag->hasAttribute('property') &&
            strpos($tag->getAttribute('property'), 'og:') === 0) {
            $key = strtr(substr($tag->getAttribute('property'), 3), '-', '_');
            $values[$key] = $tag->getAttribute('content');
        }
        
        //Added this if loop to retrieve description values from sites like the New York Times who have malformed it. 
        if ($tag ->hasAttribute('value') && $tag->hasAttribute('property') &&
            strpos($tag->getAttribute('property'), 'og:') === 0) {
            $key = strtr(substr($tag->getAttribute('property'), 3), '-', '_');
            $values[$key] = $tag->getAttribute('value');
        }
        //Based on modifications at https://github.com/bashofmann/opengraph/blob/master/src/OpenGraph/OpenGraph.php
        if ($tag->hasAttribute('name') && $tag->getAttribute('name') === 'description') {
            $nonOgDescription = $tag->getAttribute('content');
        }   
    }

    //Based on modifications at https://github.com/bashofmann/opengraph/blob/master/src/OpenGraph/OpenGraph.php
    if (!isset($page->_values['title'])) {
        $titles = $doc->getElementsByTagName('title');
        if ($titles->length > 0) {
            $values['title'] = $titles->item(0)->textContent;
        }
    }

    if (!isset($values['description']) && $nonOgDescription) {
        $values['description'] = $nonOgDescription;
    }

    if (empty($values)) { return false; }
    
    return $values;
}


//$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");    
//$html = scraperWiki::scrape("http://arstechnica.com/gadgets/2013/04/diy-cardboard-rifle-can-fire-paper-pellets-up-to-25-yeards/");
$arrItems = array();

// whip
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=327125ea480c7e77ab99c241ae6e5b82&_render=json"));

//digg
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=783479af591eb07fa41e4faa017baa75&_render=json")); 

//reddit
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=95b162812752550b18d5f96a959b0787&_render=json"));
$arrUrlsToParse = array();


// remove items from yesterday

// delete older items..?
foreach($arrItems as $objFeedItem){
   
    foreach($objFeedItem->value->items as $item){
        
        if(isset($item->link) && strpos($item->link,'reddit')){

            if(isset($item->href) && count($item->href) == 1){
                $arrUrlsToParse[] = $item->href->href;
            }else{
               if(isset($item->href) && isset($item->href[0]->href)){
                   $arrUrlsToParse[] = $item->href[0]->href;
               }
            }
       
        }else{

            if(isset($item->href)){
                $arrUrlsToParse[] = (string) $item->href;
            }
     
            if(isset($item->link)){
                $arrUrlsToParse[] = (string) $item->link;
            }

        }
    }
}

foreach($arrUrlsToParse as $strUrl){
    
    if($strUrl == "" || is_null($strUrl)){
        continue;
    }

    $tmp = array();
    $tmp["link"] = $strUrl;
    $html = scraperWiki::scrape($strUrl);
    
    if($html != ""){
        $objGraph = parseOpenGraph($html);
        $tmp["graph"] = $objGraph;
        $arrayGraphResults[] = $tmp;
        
        $twt = getTwitterShares($strUrl);
        $fb  = getFacebookLikes($strUrl);
        $popularity = $twt + $fb;

        $record = array(
            'cron_time' => $time,
            'url' => $strUrl, 
            'title' => $objGraph['title'],
            'description' => $objGraph['description'],
            'image' => $objGraph['image'],
            'twitter_count' => $twt,
            'facebook_count' => $fb,
            'popularity' => $popularity,
            'is_used' => 0
        );
        
        scraperwiki::save(array('url'), $record);
    }
}

// delete older items
$hour = 12;

$today = strtotime("$hour:00:00");
$yesterday = strtotime('-1 day', $today);
$theDayBefore = strtotime('-1 day', $yesterday) ;

$time = time();
$arrayGraphResults = array();           

scraperwiki::sqliteexecute("delete from`swdata` where cron_time < " . $theDayBefore);
scraperwiki::sqlitecommit();
<?php
/**
* retrieve OG data
* @param (string) html
* @author Vincent Cohen
*/

function getFacebookLikes($strUrl) {
 
    $strJson = file_get_contents('http://graph.facebook.com/?ids=' . $strUrl);
    $objJson = json_decode($strJson, true);
     
    foreach($objJson as $key =>$val){
  
        if(isset($objJson[$key]["shares"])){
            return intval( $objJson[$key]['shares'] );
        }
    }
}

//    get twitter shares
function getTwitterShares($strUrl){
    
    $strJson = file_get_contents("http://urls.api.twitter.com/1/urls/count.json?url=" . $strUrl);
    $objJson = json_decode($strJson);

    return $objJson->count;
}

function parseOpenGraph($HTML) {
    $old_libxml_error = libxml_use_internal_errors(true);

    $doc = new DOMDocument();
    $doc->loadHTML($HTML);

    $values = array();
    
    libxml_use_internal_errors($old_libxml_error);

    $tags = $doc->getElementsByTagName('meta');
    if (!$tags || $tags->length === 0) {
        return false;
    }

    $nonOgDescription = null;
    
    foreach ($tags as $tag) {
        if ($tag->hasAttribute('property') &&
            strpos($tag->getAttribute('property'), 'og:') === 0) {
            $key = strtr(substr($tag->getAttribute('property'), 3), '-', '_');
            $values[$key] = $tag->getAttribute('content');
        }
        
        //Added this if loop to retrieve description values from sites like the New York Times who have malformed it. 
        if ($tag ->hasAttribute('value') && $tag->hasAttribute('property') &&
            strpos($tag->getAttribute('property'), 'og:') === 0) {
            $key = strtr(substr($tag->getAttribute('property'), 3), '-', '_');
            $values[$key] = $tag->getAttribute('value');
        }
        //Based on modifications at https://github.com/bashofmann/opengraph/blob/master/src/OpenGraph/OpenGraph.php
        if ($tag->hasAttribute('name') && $tag->getAttribute('name') === 'description') {
            $nonOgDescription = $tag->getAttribute('content');
        }   
    }

    //Based on modifications at https://github.com/bashofmann/opengraph/blob/master/src/OpenGraph/OpenGraph.php
    if (!isset($page->_values['title'])) {
        $titles = $doc->getElementsByTagName('title');
        if ($titles->length > 0) {
            $values['title'] = $titles->item(0)->textContent;
        }
    }

    if (!isset($values['description']) && $nonOgDescription) {
        $values['description'] = $nonOgDescription;
    }

    if (empty($values)) { return false; }
    
    return $values;
}


//$html = scraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm");    
//$html = scraperWiki::scrape("http://arstechnica.com/gadgets/2013/04/diy-cardboard-rifle-can-fire-paper-pellets-up-to-25-yeards/");
$arrItems = array();

// whip
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=327125ea480c7e77ab99c241ae6e5b82&_render=json"));

//digg
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=783479af591eb07fa41e4faa017baa75&_render=json")); 

//reddit
$arrItems[] = json_decode(scraperWiki::scrape("http://pipes.yahoo.com/pipes/pipe.run?_id=95b162812752550b18d5f96a959b0787&_render=json"));
$arrUrlsToParse = array();


// remove items from yesterday

// delete older items..?
foreach($arrItems as $objFeedItem){
   
    foreach($objFeedItem->value->items as $item){
        
        if(isset($item->link) && strpos($item->link,'reddit')){

            if(isset($item->href) && count($item->href) == 1){
                $arrUrlsToParse[] = $item->href->href;
            }else{
               if(isset($item->href) && isset($item->href[0]->href)){
                   $arrUrlsToParse[] = $item->href[0]->href;
               }
            }
       
        }else{

            if(isset($item->href)){
                $arrUrlsToParse[] = (string) $item->href;
            }
     
            if(isset($item->link)){
                $arrUrlsToParse[] = (string) $item->link;
            }

        }
    }
}

foreach($arrUrlsToParse as $strUrl){
    
    if($strUrl == "" || is_null($strUrl)){
        continue;
    }

    $tmp = array();
    $tmp["link"] = $strUrl;
    $html = scraperWiki::scrape($strUrl);
    
    if($html != ""){
        $objGraph = parseOpenGraph($html);
        $tmp["graph"] = $objGraph;
        $arrayGraphResults[] = $tmp;
        
        $twt = getTwitterShares($strUrl);
        $fb  = getFacebookLikes($strUrl);
        $popularity = $twt + $fb;

        $record = array(
            'cron_time' => $time,
            'url' => $strUrl, 
            'title' => $objGraph['title'],
            'description' => $objGraph['description'],
            'image' => $objGraph['image'],
            'twitter_count' => $twt,
            'facebook_count' => $fb,
            'popularity' => $popularity,
            'is_used' => 0
        );
        
        scraperwiki::save(array('url'), $record);
    }
}

// delete older items
$hour = 12;

$today = strtotime("$hour:00:00");
$yesterday = strtotime('-1 day', $today);
$theDayBefore = strtotime('-1 day', $yesterday) ;

$time = time();
$arrayGraphResults = array();           

scraperwiki::sqliteexecute("delete from`swdata` where cron_time < " . $theDayBefore);
scraperwiki::sqlitecommit();
