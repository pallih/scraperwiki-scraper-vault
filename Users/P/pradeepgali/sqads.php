<?php
require 'scraperwiki/simple_html_dom.php';


$json_content= scraperWiki::scrape("http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2013/squads.js?_1363325436894=");
//print "JSON".$json_content;
 
if(strpos($json_content,"The page is not found") === FALSE){       
        //http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2012/23_careerStats.js
        $json_content=str_replace("onSquads(","",$json_content);
        $json_content=str_replace(");","",$json_content);
        $mySquadsData=json_decode($json_content,true); 
        //var_dump($myPlayerData);
        // PLAYER DATA
        $iplSeries=$mySquadsData["tournamentId"]["name"];
        $allSquads=$mySquadsData["squads"];
        
        foreach($allSquads as $sqad){
            $teamObject=$sqad["team"];
            $playersObject=$sqad["players"];
            foreach($playersObject as $player){
               $allrecord=array(
                'season'=> $iplSeries,
                'nationality'=> $player["nationality"],                
                'player_id'=> $player["id"],
                'player_dob'=>$player["dateOfBirth"],
                'player_fullName'=>$player["fullName"],
                'team_id'=>$teamObject["id"],
                'team_abbreviation'=>$teamObject["abbreviation"],
                'team_fullName'=>$teamObject["fullName"],
                'team_shortName'=>$teamObject["shortName"]
                );
             scraperwiki::save(array('player_id','season'), $allrecord); 
            }
        }      
               
        
}
else
{
    print "Empty JSON";
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';


$json_content= scraperWiki::scrape("http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2013/squads.js?_1363325436894=");
//print "JSON".$json_content;
 
if(strpos($json_content,"The page is not found") === FALSE){       
        //http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2012/23_careerStats.js
        $json_content=str_replace("onSquads(","",$json_content);
        $json_content=str_replace(");","",$json_content);
        $mySquadsData=json_decode($json_content,true); 
        //var_dump($myPlayerData);
        // PLAYER DATA
        $iplSeries=$mySquadsData["tournamentId"]["name"];
        $allSquads=$mySquadsData["squads"];
        
        foreach($allSquads as $sqad){
            $teamObject=$sqad["team"];
            $playersObject=$sqad["players"];
            foreach($playersObject as $player){
               $allrecord=array(
                'season'=> $iplSeries,
                'nationality'=> $player["nationality"],                
                'player_id'=> $player["id"],
                'player_dob'=>$player["dateOfBirth"],
                'player_fullName'=>$player["fullName"],
                'team_id'=>$teamObject["id"],
                'team_abbreviation'=>$teamObject["abbreviation"],
                'team_fullName'=>$teamObject["fullName"],
                'team_shortName'=>$teamObject["shortName"]
                );
             scraperwiki::save(array('player_id','season'), $allrecord); 
            }
        }      
               
        
}
else
{
    print "Empty JSON";
}

?>
