<?php
   
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");                 
// print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// for each line of html find td
foreach($dom->find("div[class=sportsrow]") as $data){

      //  print $data;
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $comp = $data->find("div[class=competition_name] strong");
    $sport = $data->find("div[class=sportrow]");
    $chan = $data->find("div[class=channel_name]");
    if($team1){

// $record is a new array to store the values found
        $record = array(
            'team1' => $team1[0]->innertext, 
            'team2' => $team2->innertext, 
            //'sport' => $sport->innertext, 
            'comp' => $comp[0]->innertext, 
            'time' => $time[0]->innertext, 
            'chan' => $chan[0]->innertext, 
            'date' => $date[0]->last_child(1)->innnertext, 
//
           // 'team2' => intval($tds1[0]->plaintext)
        );
// output json 
        print csv_encode($record) . "\n";
        scraperwiki::save(array('team1', 'team2', 'comp', 'time', 'chan', 'date'), $record);   
    }
}



?>
<?php
   
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");                 
// print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// for each line of html find td
foreach($dom->find("div[class=sportsrow]") as $data){

      //  print $data;
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $date = $data->find("div[class=start_time]");
    $time = $data->find("div[class=start_time] strong");
    $comp = $data->find("div[class=competition_name] strong");
    $sport = $data->find("div[class=sportrow]");
    $chan = $data->find("div[class=channel_name]");
    if($team1){

// $record is a new array to store the values found
        $record = array(
            'team1' => $team1[0]->innertext, 
            'team2' => $team2->innertext, 
            //'sport' => $sport->innertext, 
            'comp' => $comp[0]->innertext, 
            'time' => $time[0]->innertext, 
            'chan' => $chan[0]->innertext, 
            'date' => $date[0]->last_child(1)->innnertext, 
//
           // 'team2' => intval($tds1[0]->plaintext)
        );
// output json 
        print csv_encode($record) . "\n";
        scraperwiki::save(array('team1', 'team2', 'comp', 'time', 'chan', 'date'), $record);   
    }
}



?>
