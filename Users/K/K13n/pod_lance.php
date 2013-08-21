<?php
require 'scraperwiki/simple_html_dom.php';

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//set range of players to look through - currently there are 601
$players=range(1,548);

//scrape page for each player
foreach($players as $player)
{
    $html = scraperwiki::scrape($url.$player);

    // load html into dom
    $dom = new simple_html_dom();
    $dom->load($html);
    $json = $dom;
    $obj = json_decode($json);

    #if(!( strval($obj->type_name) == 'Forward')) {
        #continue;
    #}

    $mins_played = 0;
    $goals_scored = 0;
    $assists = 0;
    $clean_sheets = 0;
    $goals_con = 0;
    $own_goals = 0;
    $pen_save = 0;
    $pen_miss = 0;
    $yel_cards = 0;
    $red_cards = 0;
    $saves = 0;    
    $bonus_pts = 0;
    $eas_pts = 0;

    foreach($obj->fixture_history->all as $rows)
    {
        $mins_played += intval($rows[3]);
        $goals_scored += intval($rows[4]);
    $assists += intval($rows[5]);
    $clean_sheets += intval($rows[6]);
    $goals_con += intval($rows[7]);    
    $own_goals += intval($rows[8]);
    $pen_save += intval($rows[9]);
    $pen_miss += intval($rows[10]);
    $yel_cards += intval($rows[11]);
    $red_cards += intval($rows[12]);
    $saves += intval($rows[13]);    
    $bonus_pts += intval($rows[14]);    
    $eas_pts += intval($rows[15]);    
    
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
        'All_Star' => strval($obj->in_dreamteam),
        'Mins Played' => $mins_played,
        'Goals_scored' => $goals_scored,
        'Assists' => $assists,
        'clean_sheets' => $clean_sheets,
        'goals_con' => $goals_con,
        'own_goals' => $own_goals,
        'pen_save'  => $pen_save,
        'pen_miss'  => $pen_miss,
        'Yel_cards' => $yel_cards,
        'red_cards' => $red_cards,
        'saves' => $saves,    
        'bonus_pts' => $bonus_pts,
        'eas_pts' => $eas_pts
       
    
    );

    //save
    scraperwiki::save(array('index'),$results);
}
?>
