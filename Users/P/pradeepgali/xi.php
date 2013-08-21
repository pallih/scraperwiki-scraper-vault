<?php
require 'scraperwiki/simple_html_dom.php';
$iplSeries="2013";
//$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league/".$iplSeries."/");
ScraperWiki::attach("sqads", "src");
//$playerIds=scraperwiki::select("distinct player_id from src.swdata desc");
$matchNId=1;
while($matchNId<=59){

//Carrer Stats http://dynamic.pulselive.com/test/data/core/cricket/careerStats/1_careerStats.js?_1363343668516=
//http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2012/ipl2012-70/scoring.js?_1364576135590=
$json_content= scraperWiki::scrape("http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl".$iplSeries."/ipl".$iplSeries."-".sprintf("%02s",$matchNId)."/scoring.js?_1364576135590=");
//print "JSON".$json_content;
 
if(strpos($json_content,"The page is not found") === FALSE){       
        //http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2012/23_careerStats.js
        $json_content=str_replace("onScoring(","",$json_content);
            $json_content=str_replace(");","",$json_content);
        $myMatchData=null;
        $myMatchData=json_decode($json_content,true); 
        //var_dump($myPlayerData);
        // PLAYER DATA
        $matchId=$myMatchData["matchId"]["name"];
        print $matchId."\n";
        $matchInfo=$myMatchData["matchInfo"];
        $venue=$matchInfo["venue"];
        $venuefullName=$venue["fullName"];
        $venueCity=$venue["city"];
        $teamToBat=-1;
        $battingOrder=$matchInfo["battingOrder"];
        if($battingOrder["0"]==0)
        {
            $teamToBat=0;
        }
        elseif($battingOrder["0"]==1){
            $teamToBat=1;
        }
        $teamA=null;
        $teamAPlayers=null;
        $teamB=null;
        $teamBPlayers=null;

        $teamA=$matchInfo["teams"]["0"];
        $teamB=$matchInfo["teams"]["1"];
    
        $teamAPlayers=$teamA["players"];
        $teamBPlayers=$teamB["players"];
        $tossWinner=-1;
        $result=$matchInfo["matchStatus"]["outcome"];
        $tossWinner=$matchInfo["additionalInfo"]["toss.winner"];
        $tossWin=-1;
        if($tossWinner==$teamA["team"]["fullName"])
        {
             $tossWin=0;
        }
        elseif($tossWinner==$teamB["team"]["fullName"])
        {
            $tossWin=1;
        }
        //print "Id".$player_id;
        //OVERALL Batting Status
       // print $player_fullName.$player_id."\n";

        
        
        // Prepare Overall Record
        
        $allrecord=array(
                'matchId'=> $matchId,
                'venuefullName'=> $venuefullName,
                'venueCity'=> $venueCity,
                'season'=> "ipl".$iplSeries,
                'tossWin'=>$tossWin,
                'result'=>$result,
                'teamA'=>$teamA["team"]["shortName"],
                'teamB'=>$teamB["team"]["shortName"],
                'teamToBat'=>$teamToBat
                    
                );
        
        scraperwiki::save(array('matchId','season'), $allrecord); 
        

}
else
{
    print "Empty JSON FOR".$matchId."\n";
}

$matchNId++;


}

?>

