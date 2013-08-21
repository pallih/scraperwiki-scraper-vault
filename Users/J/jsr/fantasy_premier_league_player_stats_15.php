<?php
require 'scraperwiki/simple_html_dom.php'; 

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

//should create automatic method to find range of pages
#$lastplayer=

//set range of players to look through - currently there are 675
$players=range(1,534);
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
//var_dump($obj);

//get the fixture history for the player


$i = 0;

foreach($obj as $rows)
 {
 
//create results table
$results = array(
    'pl_num' => strval($player),
    'first_name' => strval($obj->first_name),
    'last_name' => strval($obj->web_name),
    'position' => strval($obj->type_name),
    'team_name' => strval($obj->team_name),
    'selected_cur'=>strval($obj->selected),
    'selected_by_cur'=>strval($obj->selected_by),
    'Pl_code'=>strval($obj->code),
    'Status'=>strval($obj->status),
    'News'=>strval($obj->news),
    'PIC'=>strval($obj->photo_mobile_url),
    'tot_pts'=>strval($obj->total_points),
    'form'=>strval($obj->form),
    'cur_cost'=>strval($obj->now_cost),
    'Ppg'=>strval($obj->points_per_game),
    'gwpts'=>strval($obj->event_points),

);

//check results
#print_r($results);

//save
scraperwiki::save(array('pl_num'),$results);


 if (++$i == 1) {
        break;
    }
}

}
?>
