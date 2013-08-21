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

//get the fixture history for the player
foreach($obj->fixture_history->all as $rows)
{

//create results table
$results = array(
    'index' => strval($player.$rows[1]),
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'position' => strval($obj->type_name),
    'team_name' => strval($obj->team_name),
    'date' => strval($rows[0]),
    'week' => strval($rows[1]),
    'result' => strval($rows[2]),
    'minutes_played' => strval($rows[3]),
    'goals_scored'=>strval($rows[4]),
    'assists'=>strval($rows[5]),
    'clean_sheets'=>strval($rows[6]),
    'goals_conceded'=>strval($rows[7]),
    'own_goals'=>strval($rows[8]),
    'penalties_saved'=>strval($rows[9]),
    'penalties missed'=>strval($rows[10]),
    'yellow_cards'=>strval($rows[11]),
    'red_cards'=>strval($rows[12]),
    'saves'=>strval($rows[13]),
    'bonus'=>strval($rows[14]),
    'EA_Spots_PPI'=>strval($rows[15]),
    'net_transfers'=>strval($rows[16]),
    'value'=>strval($rows[17]),
    'points'=>strval($rows[18]),

);

//check results
#print_r($results);

//save
scraperwiki::save(array('index'),$results);
}

}
?>
