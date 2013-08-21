<?php
require 'scraperwiki/simple_html_dom.php';

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//should create automatic method to find range of pages
#$lastplayer=

//set range of players to look through - currently there are 675
$players=range(1,700);
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
//print_r($obj);

//get the fixture history for the player


//create results table
$results = array(
    'index' => strval($player),
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'position' => strval($obj->type_name),
    'team_name' => strval($obj->team_name),
    'transfers_out' => strval($obj->transfers_out),
    'code' => strval($obj->code),
    'event_total' => strval($obj->event_total),
    'last_season_points' => strval($obj->last_season_points),
    'squad_number' => strval($obj->squad_number),
    'transfers_balance' => strval($obj->transfers_balance),
    'news_updated' => strval($obj->news_updated),
    'event_cost' => strval($obj->event_cost),
    'news_added' => strval($obj->news_added),
    'in_dreamteam' => strval($obj->in_dreamteam),
    'team_code' => strval($obj->team_code),
    'id' => strval($obj->id),
    'transfers_out_event' => strval($obj->transfers_out_event),
    'element_type_id' => strval($obj->element_type_id),
    'max_cost' => strval($obj->max_cost),
    'selected' => strval($obj->selected),
    'min_cost' => strval($obj->min_cost),
    'total_points' => strval($obj->total_points),
    'type_name' => strval($obj->type_name),
    'team_name' => strval($obj->team_name),
    'status' => strval($obj->status),
    'added' => strval($obj->added),
    'form' => strval($obj->form),
    'current_fixture' => strval($obj->current_fixture),
    'now_cost' => strval($obj->now_cost),
    'points_per_game' => strval($obj->points_per_game),
    'transfers_in' => strval($obj->transfers_in),
    'news' => strval($obj->news),
    'original_cost' => strval($obj->original_cost),
    'event_points' => strval($obj->event_points),
    'news_return' => strval($obj->news_return),
    'next_fixture' => strval($obj->next_fixture),
    'transfers_in_event' => strval($obj->transfers_in_event),
    'selected_by' => strval($obj->selected_by),
    'team_id' => strval($obj->team_id),
    'second_name' => strval($obj->second_name)
);

//check results
#print_r($results);

//save
scraperwiki::save(array('index'),$results);

}
?>
