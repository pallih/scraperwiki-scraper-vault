<?php
require 'scraperwiki/simple_html_dom.php';

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//set range of players to look through - currently there are 553
$players=range(1,581);

//scrape page for each player
foreach($players as $player)
{
    $html = scraperwiki::scrape($url.$player);

    // load html into dom
    $dom = new simple_html_dom();
    $dom->load($html);
    $json = $dom;
    $obj = json_decode($json);

    ##if(!( strval($obj->type_name) == 'Forward')) {
        ##continue;
    ##}

    $mins_played = 0;
    $goals_scored = 0;

    foreach($obj->fixture_history->all as $rows)
    {
        $mins_played += intval($rows[3]);
        $goals_scored += intval($rows[4]);
    };

    //create results table
    $results = array(
        'index' => strval($obj->id),
        'Selected' => intval($obj->selected),
        'Selected%' => floatval($obj->selected_by),    
        'position' => strval($obj->type_name),
        'team_name' => strval($obj->team_name),    
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'Total_Points' => intval($obj->total_points),
    'Pts_per_game' => intval($obj->points_per_game),
    'Form' => strval($obj->form),    
    'Orig_cost' => intval($obj->original_cost),
    'Value' => intval($obj->now_cost),
    'Transfers_in' => intval($obj->transfers_in),
    'Transfers_in_eve' => intval($obj->transfers_in_event),    
    'Transfers_in_out' => intval($obj->transfers_out_event),
    'Next_fixture' => strval($obj->next_fixture),
    'Current_Fixture' => strval($obj->current_fixture),
    'News' => strval($obj->news),
    'Mins Played' => $mins_played,
    'goals_scored' => $goals_scored,
    );

    //save
    scraperwiki::save(array('index'),$results);
}
?>
