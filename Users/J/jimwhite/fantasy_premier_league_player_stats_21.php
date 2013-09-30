<?php
require 'scraperwiki/simple_html_dom.php'; 

# Work In Progress!

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

// should create automatic method to find range of pages
#$lastplayer=

// set range of players to look through - currently there are 675
$players=range(1,10);
#$players=range(1,$lastplayer);

// scrape page for each player
foreach($players as $player)
{
    $html = scraperwiki::scrape($url.$player.'/');
    #print_r($html);

    // load html into dom
    $dom = new simple_html_dom();
        $dom->load($html);
    
    // turn dom into a string
    $json = $dom;

    // make the json string an array which i confusingly call an object
    $obj = json_decode($json);
    
    //Test:
    #print_r($obj);
    #break;
    
    if (is_null($obj->id))
        print("null");
    if (empty($obj->id))
        print("empty");
    
    #$points = $obj->total_points;
    #$cost_now = $obj->now_cost;
    #$ranking = ($points * 10) - $cost_now;
    
    $res = array
    (
        'id' => strval($obj->id),
        'first_name' => strval($obj->first_name),
        'last_name' => strval($obj->web_name),
        'position' => strval($obj->type_name),
        'team_name' => strval($obj->team_name),
        'status' => strval($obj->status),
        'points' => strval($obj->total_points),
        'cost_now' => strval($obj->now_cost),
        'form' => strval($obj->form),
        'sel_by' => strval($obj->selected_by),
        'opponents' => strval($obj->fixtures->all['1']),
       # 'fitness' => strval($ranking)
    );
    
    // Output the scraped details in res
    #print_r($res);

    // Save back to ScraperWiki
    scraperwiki::save(array('id'),$res);

}
?>
<?php
require 'scraperwiki/simple_html_dom.php'; 

# Work In Progress!

// get base url
$url = 'http://fantasy.premierleague.com/web/api/elements/';

// should create automatic method to find range of pages
#$lastplayer=

// set range of players to look through - currently there are 675
$players=range(1,10);
#$players=range(1,$lastplayer);

// scrape page for each player
foreach($players as $player)
{
    $html = scraperwiki::scrape($url.$player.'/');
    #print_r($html);

    // load html into dom
    $dom = new simple_html_dom();
        $dom->load($html);
    
    // turn dom into a string
    $json = $dom;

    // make the json string an array which i confusingly call an object
    $obj = json_decode($json);
    
    //Test:
    #print_r($obj);
    #break;
    
    if (is_null($obj->id))
        print("null");
    if (empty($obj->id))
        print("empty");
    
    #$points = $obj->total_points;
    #$cost_now = $obj->now_cost;
    #$ranking = ($points * 10) - $cost_now;
    
    $res = array
    (
        'id' => strval($obj->id),
        'first_name' => strval($obj->first_name),
        'last_name' => strval($obj->web_name),
        'position' => strval($obj->type_name),
        'team_name' => strval($obj->team_name),
        'status' => strval($obj->status),
        'points' => strval($obj->total_points),
        'cost_now' => strval($obj->now_cost),
        'form' => strval($obj->form),
        'sel_by' => strval($obj->selected_by),
        'opponents' => strval($obj->fixtures->all['1']),
       # 'fitness' => strval($ranking)
    );
    
    // Output the scraped details in res
    #print_r($res);

    // Save back to ScraperWiki
    scraperwiki::save(array('id'),$res);

}
?>
