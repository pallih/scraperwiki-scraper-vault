<?php
   
$html = scraperWiki::scrape("http://walkabout.eu.com/sport/");                 
// print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// for each line of html find td
foreach($dom->find("div[class=sportsrow]") as $data){

    //  print $data;

    // get the team(s) playing
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $date = $data->find("div[class=start_time]");

    $comp = $data->find("div[class=competition_name] strong");

    $time = $data->find("div[class=start_time] strong");
    $sport = $data->find("div[class=sportrow]");

    // which channel is it on?
   // $chan = $data->find("div[class=channel_name]");
    //$tvchan = $chan[0]->innertext;
   // echo basename($tvchan);
   // preg_match_all('!https?://[\S]+!', $tvchan, $matches);
   // $all_urls = $matches[0];
    //echo $matches[1];

    if($team1){

   // $record is a new array to store the values found
        $record = array(
            //'team1' => $team1[0]->innertext, 
            //'team2' => $team2->innertext, 
            'fixture' => $team1[0]->innertext . ' vs ' . $team2->innertext,
            //'sport' => $sport->innertext, 
            'comp' => $comp[0]->innertext, 
            'time' => $time[0]->innertext, 
            //'chan' => $chan[0]->innertext, 
            //'date' => $date[0],//->last_child(1)->innnertext, 
        
           // 'team2' => intval($tds1[0]->plaintext)
        );

        // output json 
        print json_encode($record) . "\n";
        scraperwiki::save(array('fixture', 'comp', 'time'), $record);   
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

    // get the team(s) playing
    $team1 = $data->find("div[class=sport_teams] strong");
    $team2 = $data->find("div[class=sport_teams] strong", 1);
    $date = $data->find("div[class=start_time]");

    $comp = $data->find("div[class=competition_name] strong");

    $time = $data->find("div[class=start_time] strong");
    $sport = $data->find("div[class=sportrow]");

    // which channel is it on?
   // $chan = $data->find("div[class=channel_name]");
    //$tvchan = $chan[0]->innertext;
   // echo basename($tvchan);
   // preg_match_all('!https?://[\S]+!', $tvchan, $matches);
   // $all_urls = $matches[0];
    //echo $matches[1];

    if($team1){

   // $record is a new array to store the values found
        $record = array(
            //'team1' => $team1[0]->innertext, 
            //'team2' => $team2->innertext, 
            'fixture' => $team1[0]->innertext . ' vs ' . $team2->innertext,
            //'sport' => $sport->innertext, 
            'comp' => $comp[0]->innertext, 
            'time' => $time[0]->innertext, 
            //'chan' => $chan[0]->innertext, 
            //'date' => $date[0],//->last_child(1)->innnertext, 
        
           // 'team2' => intval($tds1[0]->plaintext)
        );

        // output json 
        print json_encode($record) . "\n";
        scraperwiki::save(array('fixture', 'comp', 'time'), $record);   
    }
}



?>
