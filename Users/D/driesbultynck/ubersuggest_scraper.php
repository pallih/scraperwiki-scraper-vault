<?php
//https://github.com/ariya/phantomjs/blob/master/examples/waitfor.js
//http://stackoverflow.com/questions/11275772/php-crawler-check-if-object-exists
//http://stackoverflow.com/questions/12071213/how-to-check-if-a-simplehtmldom-element-does-not-exist

//echo 'One moment pls :)'."\n";
//echo 'This could take a few seconds...'."\n";

/* SETTINGS */

require 'scraperwiki/simple_html_dom.php'; 
$minDelay='0'; //sec
$maxDelay='5'; //sec
$i=0;
$depth = 1;
$stack = array();
$end = false;
$source="ubersuggest";
$word='atco'; //geef zoekwoord op dat domein moet bevatten

//visualiseren van data 
//pay options? > data verzamelen!!! country based, ip, dates, months insights, ...
//domain watcher service?

//headerChecker("http://www.driesbultynck.be");
scrape($source);

/* STANDARD FUNCTIONS */

function save(){
    //iedere link met 404 code saven in database
    //vanuit zelf ingegeven link
    //vanuit zelf zoekmachine + keyword
    //check voor update > indien geen 404 meer, zet als fixed en delete uit lijst
}

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

function searchForWord($stack){
    global $word;
    $matches = preg_grep('/'.$word.'/', $stack);
    return $matches;   
}

function headerChecker($url){
    file_get_contents($url);
    list($version,$status_code,$msg) = explode(' ',$http_response_header[0], 3);
/*
    switch($status_code) {
        case 200:
                $error_status="200: Success";
                break;
        case 401:
                $error_status="401: Login failure. Try logging out and back in. Password are ONLY used when posting.";
                break;
        case 400:
                $error_status="400: Invalid request. You may have exceeded your rate limit.";
                break;
        case 404:
                $error_status="404: Not found. This shouldn't happen. Please let me know what happened using the feedback link above.";
                break;
        case 500:
                $error_status="500: Servers replied with an error. Hopefully they'll be OK soon!";
                break;
        case 502:
                $error_status="502: Servers may be down or being upgraded. Hopefully they'll be OK soon!";
                break;
        case 503:
                $error_status="503: Service unavailable. Hopefully they'll be OK soon!";
                break;
        default:
                $error_status="Wow... not sure what to do actually with this code: " . $status_code;
                break;
    }
*/
    return $status_code;
}

function loop($source){

//voorrang geven aan gesavede content!

    global $end, $depth, $source;
        switch($source){
        case "ubersuggest":
            //while (!$end && $depth<1000){
            //$runDepth = $depth;
                $link = scraperwiki::scrape("http://ubersuggest.org/?query=fietsroutes&format=html&language=Dutch&source=web");
                        $html = str_get_html($link);
                        if(!is_object($html->find("body a", 0))){
                            break;
                        }
                        
                        $urls = getLinks($html);
                    /* 
                    $depth++;
                        if($depth==9999){
                            $end = true;
                        }
                    }
                    */
                    if(sizeof($urls) > 0){
                        foreach($urls as $key=>$value){
                            echo $value."\n";
                        }
                    }else{
                        echo "No match found";
                    }
                break;
        case "google":
            // wat met landen / taal versies?
            echo "to do";
            break;
        case "bing":
                    // wat met landen / taal versies?
                    echo "to do";
                    break;
        case "yahoo":
                    // wat met landen / taal versies?
                    echo "to do";
                    break;
       default:
                echo "Choose an option";
                break;
}
}

/* SCRAPING NOT FOUND DOT ORG */

//algemene functie voor scraping: select source > daaruit volgt de rest
//google
//bing
//yahoo?
//site

function scrape($source){
    //while ook in aparte functie gieten voor hergebruik google of bing of specifieke site
    loop($source);
}

function getLinks($html){
    global $i, $stack;
    //check andere bron?
    //if(preg_match('/notfound.org/',$html)){
        foreach($html->find("a",0) as $tag){
            $stack[$i] = $tag->getAttribute('href');
            //$stack[$i] = $tag->innerText;
            $i++;
        //}
        //return searchForWord($stack);
        return $stack;
    }
}

?>
