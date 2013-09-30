<?php
print "Starting!  Waiting for scrape...\n";

// Get a dummy response, we just care about the session ID it will return that says we want to use the english language
// Do this first, but you only need to use it once.
$dummyresponse = get_url("https://rakendused.vm.ee/akta/index.php?language=eng");
$SESSION_ID = $dummyresponse['cookie'];

// Now use the dummy response (most important, the session ID from the response) to issue an additional query.
// As long as we don't time out, we can still use this same $SESSION_ID as the session ID.
$realresponse = get_url("https://rakendused.vm.ee/akta/andmed_vaata.php?id=2063", $SESSION_ID);
// Set the variable html as the HTML response from the issued query
$html = $realresponse['content'];


// Now, continue as normal
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$temprecord=array();
$innertabledata=$dom->find("div#sisuAla");
$allrecords=getTableElements($innertabledata[0]);

// print_r will print an array in a fairly readible format
print_r($allrecords);
// If you need to print as JSON, you can use this
print json_encode($allrecords) . "\n";


function getTableElements($dom){
    //print $dom[0]."this is dom \n";
    $record = array();
    $numtoskip=0;
    foreach($dom->find("tr") as $data){
        if($numtoskip>0) {
            $numtoskip--;
            continue;
        }
        $tds = $data->find("td");
        //print "||1||".$tds[0]->plaintext."|| ||2||".$tds[1]->plaintext."||\n";
        $counter=0;
        // Special Case
        if(count($tds) > 1 and count($tds[1]->find("td"))>1){
            $newrecord=getTableElements($tds[1]);
            $numtoskip=count($newrecord);
            print "made it here!".count($newrecord). "\n";
            foreach($newrecord as $key=> $value){
                $record[$tds[0]->plaintext . "_".$key] = $value;
                print "adding ".$tds[0]->plaintext . "_".$key." with value ". $value. "\n";
            }
        }
        
        else {
            if(count($tds) > 1) {
                $record[$tds[0]->plaintext] = $tds[1]->plaintext;
            }
        }
        
    }
    print "the size of the record is " . count($record);
    return $record;
}

print "\n\nFinished.  Moving on...\n";

// Function to get the url with a cookie as the header.  For the Estonian data, we need
// to get a session ID, then use it as further calls to get_url.  $cookies can be emtpy,
// in which case it won't set any session ID
function get_url($url, $cookies="") {
    $res = array();
    $options = array(
        CURLOPT_RETURNTRANSFER => true,     // return web page
        CURLOPT_HEADER         => true,     // return headers
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects
        CURLOPT_USERAGENT      => "spider", // who am i
        CURLOPT_COOKIESESSION  => true,
        CURLOPT_COOKIE         => $cookies, // set the cookies
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect
        CURLOPT_SSL_VERIFYPEER => false,    // required for https urls
        CURLOPT_CONNECTTIMEOUT => 120,      // timeout on connect
        CURLOPT_TIMEOUT        => 120,      // timeout on response
        CURLOPT_MAXREDIRS      => 10,       // stop after 10 redirects
    );
    $ch      = curl_init( $url );
    curl_setopt_array( $ch, $options );
    $content = curl_exec( $ch );
    $err     = curl_errno( $ch );
    $errmsg  = curl_error( $ch );
    $response = curl_getinfo( $ch );
    $headers = get_headers($response['url']);
    $cookie = "";
    if(preg_match('/^Set-Cookie: (.*?);/m', $content, $m)) {
        $cookie = $m[1];
    }
    
    //print "Cookie is: [$cookie]\n";
    curl_close( $ch );

    $res['content'] = $content;
    $res['cookie'] = $cookie;
    return $res;
}


?><?php
print "Starting!  Waiting for scrape...\n";

// Get a dummy response, we just care about the session ID it will return that says we want to use the english language
// Do this first, but you only need to use it once.
$dummyresponse = get_url("https://rakendused.vm.ee/akta/index.php?language=eng");
$SESSION_ID = $dummyresponse['cookie'];

// Now use the dummy response (most important, the session ID from the response) to issue an additional query.
// As long as we don't time out, we can still use this same $SESSION_ID as the session ID.
$realresponse = get_url("https://rakendused.vm.ee/akta/andmed_vaata.php?id=2063", $SESSION_ID);
// Set the variable html as the HTML response from the issued query
$html = $realresponse['content'];


// Now, continue as normal
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$temprecord=array();
$innertabledata=$dom->find("div#sisuAla");
$allrecords=getTableElements($innertabledata[0]);

// print_r will print an array in a fairly readible format
print_r($allrecords);
// If you need to print as JSON, you can use this
print json_encode($allrecords) . "\n";


function getTableElements($dom){
    //print $dom[0]."this is dom \n";
    $record = array();
    $numtoskip=0;
    foreach($dom->find("tr") as $data){
        if($numtoskip>0) {
            $numtoskip--;
            continue;
        }
        $tds = $data->find("td");
        //print "||1||".$tds[0]->plaintext."|| ||2||".$tds[1]->plaintext."||\n";
        $counter=0;
        // Special Case
        if(count($tds) > 1 and count($tds[1]->find("td"))>1){
            $newrecord=getTableElements($tds[1]);
            $numtoskip=count($newrecord);
            print "made it here!".count($newrecord). "\n";
            foreach($newrecord as $key=> $value){
                $record[$tds[0]->plaintext . "_".$key] = $value;
                print "adding ".$tds[0]->plaintext . "_".$key." with value ". $value. "\n";
            }
        }
        
        else {
            if(count($tds) > 1) {
                $record[$tds[0]->plaintext] = $tds[1]->plaintext;
            }
        }
        
    }
    print "the size of the record is " . count($record);
    return $record;
}

print "\n\nFinished.  Moving on...\n";

// Function to get the url with a cookie as the header.  For the Estonian data, we need
// to get a session ID, then use it as further calls to get_url.  $cookies can be emtpy,
// in which case it won't set any session ID
function get_url($url, $cookies="") {
    $res = array();
    $options = array(
        CURLOPT_RETURNTRANSFER => true,     // return web page
        CURLOPT_HEADER         => true,     // return headers
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects
        CURLOPT_USERAGENT      => "spider", // who am i
        CURLOPT_COOKIESESSION  => true,
        CURLOPT_COOKIE         => $cookies, // set the cookies
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect
        CURLOPT_SSL_VERIFYPEER => false,    // required for https urls
        CURLOPT_CONNECTTIMEOUT => 120,      // timeout on connect
        CURLOPT_TIMEOUT        => 120,      // timeout on response
        CURLOPT_MAXREDIRS      => 10,       // stop after 10 redirects
    );
    $ch      = curl_init( $url );
    curl_setopt_array( $ch, $options );
    $content = curl_exec( $ch );
    $err     = curl_errno( $ch );
    $errmsg  = curl_error( $ch );
    $response = curl_getinfo( $ch );
    $headers = get_headers($response['url']);
    $cookie = "";
    if(preg_match('/^Set-Cookie: (.*?);/m', $content, $m)) {
        $cookie = $m[1];
    }
    
    //print "Cookie is: [$cookie]\n";
    curl_close( $ch );

    $res['content'] = $content;
    $res['cookie'] = $cookie;
    return $res;
}


?>