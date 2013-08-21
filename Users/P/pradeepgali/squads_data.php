<?php
require 'scraperwiki/simple_html_dom.php';
$iplSeries="2012";
//$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league/".$iplSeries."/");
ScraperWiki::attach("sqads", "src");
$playerIds=scraperwiki::select("distinct player_id from src.swdata desc");
foreach($playerIds as $playerid){

//Carrer Stats http://dynamic.pulselive.com/test/data/core/cricket/careerStats/1_careerStats.js?_1363343668516=
$json_content= scraperWiki::scrape("http://dynamic.pulselive.com/dynamic/data/core/cricket/careerStats/".$playerid["player_id"]."_careerStats.js?_1363343668516=");
//print "JSON".$json_content;
 
if(strpos($json_content,"The page is not found") === FALSE){       
        //http://dynamic.pulselive.com/dynamic/data/core/cricket/2012/ipl2012/23_careerStats.js
        $json_content=str_replace("onPlayerCareerStats(","",$json_content);
        $json_content=str_replace(");","",$json_content);
        $myPlayerData=null;
        $myPlayerData=json_decode($json_content,true); 
        //var_dump($myPlayerData);
        // PLAYER DATA
        $player_full=$myPlayerData["player"];
        $player_fullName=$player_full["fullName"];
        $player_Nationality=$player_full["nationality"];
        $player_DOB=$player_full["dateOfBirth"];
        $player_id=$player_full["id"];
        //print "Id".$player_id;
        //OVERALL Batting Status
        print $player_fullName.$player_id."\n";
        $overAllRecords=null;
        if(array_key_exists("stats",$myPlayerData)){
        foreach($myPlayerData["stats"] as $stsType)
        {
            if($stsType["matchType"]=="IPLT20"){
                $overAllRecords=$stsType;
             }
        }
        if(!empty($overAllRecords))
        {
        $overAllBatting=null;
        $overAllBowling=null;
        $overAllFielding=null;
        $overAllBatting=$overAllRecords["battingStats"];
        $overAllBowling=$overAllRecords["bowlingStats"];
        $overAllFielding=$overAllRecords["fieldingStats"];
        
        // Prepare Overall Record
        
        $allrecord=array(
                'fullname'=> $player_fullName,
                'nationality'=> $player_Nationality,
                'dateOfBirth'=> $player_DOB,
                'player_id'=> $player_id,
                'season'=>'All',
                'BAT_Mat'=>$overAllBatting ? $overAllBatting["m"] : "-",
                'BAT_Inns'=>$overAllBatting ? $overAllBatting["inns"] : "-",
                'BAT_NO'=>$overAllBatting ? $overAllBatting["no"] : "-", 
                'BAT_Runs'=>$overAllBatting ? $overAllBatting["r"] : "-", 
                'BAT_HS'=>$overAllBatting ? $overAllBatting["hs"] : "-", 
                'BAT_Ave'=>$overAllBatting ? $overAllBatting["a"] : "-",
                'BAT_BF'=>$overAllBatting ? $overAllBatting["b"] : "-",
                'BAT_SR'=>$overAllBatting ? $overAllBatting["sr"] : "-",
                'BAT_100'=>$overAllBatting ? $overAllBatting["100s"] : "-",
                'BAT_50'=>$overAllBatting ? $overAllBatting["50s"] : "-", 
                'BAT_4s'=>$overAllBatting ? $overAllBatting["4s"] : "-", 
                'BAT_6s'=>$overAllBatting ? $overAllBatting["6s"] : "-",
                'BAT_Ct'=>$overAllFielding ? $overAllFielding["c"] : "-", 
                'BAT_St'=> $overAllFielding ? $overAllFielding["s"] : "-",
                'BOWL_Mat'=>$overAllBowling ? $overAllBowling["m"] : "-",
                'BOWL_Inns'=>$overAllBowling ? $overAllBowling["inns"] : "-",
                'BOWL_Balls'=> $overAllBowling ? $overAllBowling["b"] : "-",
                'BOWL_Runs'=>$overAllBowling ? $overAllBowling["r"] : "-", 
                'BOWL_Dots'=>$overAllBowling ? $overAllBowling["d"] : "-", 
                'BOWL_Wkts'=>$overAllBowling ? $overAllBowling["w"] : "-", 
                'BOWL_BBM'=>$overAllBowling && $overAllBowling["bbmr"] !== "-" && $overAllBowling["bbmw"] !== "-" ? $overAllBowling["bbmw"] + "-" + $overAllBowling["bbmr"] : "-",
                'BOWL_Ave'=>$overAllBowling ? $overAllBowling["a"] : "-",
                'BOWL_Econ'=> $overAllBowling ? $overAllBowling["e"] : "-",
                'BOWL_SR'=>$overAllBowling ? $overAllBowling["sr"] : "-", 
                'BOWL_4w'=>$overAllBowling ? $overAllBowling["4w"] : "-", 
                'BOWL_5w'=>$overAllBowling ? $overAllBowling["5w"] : "-");
        
        scraperwiki::save(array('player_id','season'), $allrecord); 
        
        // Prepare Seasonal Data
        
        foreach ($overAllRecords["breakdown"] as $seasonData){
            //print $seasonData["seasonId"]."\n";
            $overAllBatting=$seasonData["battingStats"];
        $overAllBowling=$seasonData["bowlingStats"];
        $overAllFielding=$seasonData["fieldingStats"];
        
        // Prepare Overall Record
        
        $allrecord=array(
                'fullname'=> $player_fullName,
                'nationality'=> $player_Nationality,
                'dateOfBirth'=> $player_DOB,
                'player_id'=> $player_id,
                'season'=>$seasonData["tournamentId"]["name"],
                'BAT_Mat'=>$overAllBatting ? $overAllBatting["m"] : "-",
                'BAT_Inns'=>$overAllBatting ? $overAllBatting["inns"] : "-",
                'BAT_NO'=>$overAllBatting ? $overAllBatting["no"] : "-", 
                'BAT_Runs'=>$overAllBatting ? $overAllBatting["r"] : "-", 
                'BAT_HS'=>$overAllBatting ? $overAllBatting["hs"] : "-", 
                'BAT_Ave'=>$overAllBatting ? $overAllBatting["a"] : "-",
                'BAT_BF'=>$overAllBatting ? $overAllBatting["b"] : "-",
                'BAT_SR'=>$overAllBatting ? $overAllBatting["sr"] : "-",
                'BAT_100'=>$overAllBatting ? $overAllBatting["100s"] : "-",
                'BAT_50'=>$overAllBatting ? $overAllBatting["50s"] : "-", 
                'BAT_4s'=>$overAllBatting ? $overAllBatting["4s"] : "-", 
                'BAT_6s'=>$overAllBatting ? $overAllBatting["6s"] : "-",
                'BAT_Ct'=>$overAllFielding ? $overAllFielding["c"] : "-", 
                'BAT_St'=> $overAllFielding ? $overAllFielding["s"] : "-",
                'BOWL_Mat'=>$overAllBowling ? $overAllBowling["m"] : "-",
                'BOWL_Inns'=>$overAllBowling ? $overAllBowling["inns"] : "-",
                'BOWL_Balls'=> $overAllBowling ? $overAllBowling["b"] : "-",
                'BOWL_Runs'=>$overAllBowling ? $overAllBowling["r"] : "-", 
                'BOWL_Dots'=>$overAllBowling ? $overAllBowling["d"] : "-", 
                'BOWL_Wkts'=>$overAllBowling ? $overAllBowling["w"] : "-", 
                'BOWL_BBM'=>$overAllBowling && $overAllBowling["bbmr"] !== "-" && $overAllBowling["bbmw"] !== "-" ? $overAllBowling["bbmw"] + "-" + $overAllBowling["bbmr"] : "-",
                'BOWL_Ave'=>$overAllBowling ? $overAllBowling["a"] : "-",
                'BOWL_Econ'=> $overAllBowling ? $overAllBowling["e"] : "-",
                'BOWL_SR'=>$overAllBowling ? $overAllBowling["sr"] : "-", 
                'BOWL_4w'=>$overAllBowling ? $overAllBowling["4w"] : "-", 
                'BOWL_5w'=>$overAllBowling ? $overAllBowling["5w"] : "-");
        
        scraperwiki::save(array('player_id','season'), $allrecord); 
        
        }
    }
    }
    else{
        print "Empty STATS";
    }
}
else
{
    print "Empty JSON FOR".$playerid["player_id"]."\n";
}
}

?>
