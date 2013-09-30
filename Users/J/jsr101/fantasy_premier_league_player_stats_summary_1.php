<?php
require 'scraperwiki/simple_html_dom.php'; 

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//should create automatic method to find range of pages
#$lastplayer=

//set range of players to look through - currently there are 675
$players=range(1,675);
#$players=range(1,$lastplayer);

//need to add specific numbers such as Jan transfers to array

//scrape page for each player
foreach($players as $player)
{
$html = scraperwiki::scrape($url.$player);

// load html into dom
$dom = new simple_html_dom();
    $dom->load($html);

//turn dom into a string
$json = $dom;

//make the json string an array which i confusingly call an object
$obj = json_decode($json);

//Test:
#print_r($obj);

$rows = '';

//create results table
$results = array(
    'index' => strval($player.$rows),
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'position' => strval($obj->type_name),
    'team_name' => strval($obj->team_name), 
    'total_points' => strval($obj->total_points),     
    'now_cost' => strval($obj->now_cost),
    'points_per_game' => strval($obj->points_per_game),
    'next_fixture' => strval($obj->next_fixture),
    'shirt_mobile_image_url' => strval($obj->shirt_mobile_image_url),
    'status' => strval($obj->status),
   
);

//check results
#print_r($results);

//save
scraperwiki::save(array('index'),$results);
}


?>
<?php
require 'scraperwiki/simple_html_dom.php'; 

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//should create automatic method to find range of pages
#$lastplayer=

//set range of players to look through - currently there are 675
$players=range(1,675);
#$players=range(1,$lastplayer);

//need to add specific numbers such as Jan transfers to array

//scrape page for each player
foreach($players as $player)
{
$html = scraperwiki::scrape($url.$player);

// load html into dom
$dom = new simple_html_dom();
    $dom->load($html);

//turn dom into a string
$json = $dom;

//make the json string an array which i confusingly call an object
$obj = json_decode($json);

//Test:
#print_r($obj);

$rows = '';

//create results table
$results = array(
    'index' => strval($player.$rows),
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'position' => strval($obj->type_name),
    'team_name' => strval($obj->team_name), 
    'total_points' => strval($obj->total_points),     
    'now_cost' => strval($obj->now_cost),
    'points_per_game' => strval($obj->points_per_game),
    'next_fixture' => strval($obj->next_fixture),
    'shirt_mobile_image_url' => strval($obj->shirt_mobile_image_url),
    'status' => strval($obj->status),
   
);

//check results
#print_r($results);

//save
scraperwiki::save(array('index'),$results);
}


?>
