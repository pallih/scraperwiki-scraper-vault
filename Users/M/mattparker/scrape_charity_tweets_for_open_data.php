<?php

/**
 * Look for tweets @VCSOpen #ourdata, try and parse it for a number 
 */


// Get the page: %20%23ourdata
/*
$jsonString = scraperWiki::scrape("http://search.twitter.com/search.json?q=@VCSOpen&result_type=recent&rpp=1&page=1");

$json = json_decode($jsonString);

$max_id = $json->max_id;
*/


// Parses text of tweet looking for numbers
function parseTweetText($str) {
    $str = trim(strtolower($str));
    $ret = str_replace(
        array(
            '@vcsopen',
            '#ourdata'
        ), 
        '',
        $str
    );
    $str = preg_replace('/[^0-9 ]/', '', $str);
    preg_match('/\w([0-9])+\w/', $str, $match);
    if ($match && count($match) > 0) {
        return $match[0];
    }
    return '';      

};


// For testing:
$json = new stdClass();
$json->results = array();
$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata 6789';
$json->results[] = $res1;

$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata we worked with 4,837 people';
$json->results[] = $res1;

$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata we worked with 123 people and 456 organisations';
$json->results[] = $res1;

foreach($json->results as $result) {

    $thisTweet = array(
        'user' => $result->from_user,
        'user_id' => $result->from_user_id,
        'numBeneficiaries' => parseTweetText($result->text)
    );
    var_dump($thisTweet);
    
}
   // scraperwiki::save(array('date'), $data);

    //$saved = scraperwiki::select("* from swdata where `date` = '" . date('Y-m-d') . "'");
    //var_dump($saved);




?>
<?php

/**
 * Look for tweets @VCSOpen #ourdata, try and parse it for a number 
 */


// Get the page: %20%23ourdata
/*
$jsonString = scraperWiki::scrape("http://search.twitter.com/search.json?q=@VCSOpen&result_type=recent&rpp=1&page=1");

$json = json_decode($jsonString);

$max_id = $json->max_id;
*/


// Parses text of tweet looking for numbers
function parseTweetText($str) {
    $str = trim(strtolower($str));
    $ret = str_replace(
        array(
            '@vcsopen',
            '#ourdata'
        ), 
        '',
        $str
    );
    $str = preg_replace('/[^0-9 ]/', '', $str);
    preg_match('/\w([0-9])+\w/', $str, $match);
    if ($match && count($match) > 0) {
        return $match[0];
    }
    return '';      

};


// For testing:
$json = new stdClass();
$json->results = array();
$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata 6789';
$json->results[] = $res1;

$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata we worked with 4,837 people';
$json->results[] = $res1;

$res1 = new stdClass();
$res1->from_user = 'test1';
$res1->from_user_id = '12345';
$res1->text = '@VCSOpen #ourdata we worked with 123 people and 456 organisations';
$json->results[] = $res1;

foreach($json->results as $result) {

    $thisTweet = array(
        'user' => $result->from_user,
        'user_id' => $result->from_user_id,
        'numBeneficiaries' => parseTweetText($result->text)
    );
    var_dump($thisTweet);
    
}
   // scraperwiki::save(array('date'), $data);

    //$saved = scraperwiki::select("* from swdata where `date` = '" . date('Y-m-d') . "'");
    //var_dump($saved);




?>
