<?php

# Blank PHP
$iplSeries="2012";
$homeGrounds=array("Deccan Chargers"=>"Hyderabad","Chennai Super Kings"=>"Chennai","Rajasthan Royals"=>"Jaipur","Kolkata Knight Riders"=>"Kolkata","Pune Warriors"=>"Gahunje","Kings XI Punjab"=>"Mohali","Delhi Daredevils"=>"Delhi","Mumbai Indians"=>"Mumbai","Royal Challengers Bangalore"=>"Bangalore");
$venueType=-1;

//$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league/".$iplSeries."/");           
$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league");           
require 'scraperwiki/simple_html_dom.php';

$dom = str_get_html($html_content);
$i=0;
 foreach ($dom->find("table tr a") as $el) {           
    $toScrape= "http://www.thatscricket.com".$el->href;
    $scorecard_html=scraperWiki::scrape($toScrape);
    $scorecard_dom=str_get_html($scorecard_html);
    $summaryItems=$scorecard_dom->find("div.cricket-matchSummaryLeft div");
    $summaryTitle=$scorecard_dom->find("div.cricket-matchSummaryLeft1 h3");
    $matchResultDOM=$scorecard_dom->find("div.cricket-matchResultBlock h3");
    $InningsDOM=$scorecard_dom->find("h3.cricket-accorHeader");

    $tossWinner=$summaryItems[3]->plaintext;    
    $matchDate=$summaryItems[2]->plaintext;
    $matchResult=$matchResultDOM[0]->plaintext;     


    $venue=$summaryItems[1]->plaintext;
     $teams=explode("Vs",trim($summaryTitle[0]->plaintext));
    if(count($teams)===2){
    $teamA=trim($teams[0]);
    $teamB=trim($teams[1]);
    }
    else{
     print "problem". $el->href;
    }
    //FOR DC
    if(strpos($venue,"Visakhapatnam")!==FALSE){
            print $venue;
            $venue="Hyderabad";

        }
    if(strpos($venue,"Cuttack")!==FALSE){
            print $venue;        
            $venue="Hyderabad";
        }
    if(strpos($venue, $homeGrounds[$teamA]) !== FALSE){
            $venueType=1;
    }
    if(strpos($venue, $homeGrounds[$teamB]) !== FALSE){
            $venueType=0;
    }
    if($venueType===-1){
        $venueType=2;
    }
    $tossWinnerFlag=-1;
    if(strpos($tossWinner,$teamA) !== FALSE){
            $tossWinnerFlag=1;
    }
    if(strpos($tossWinner,$teamB) !== FALSE){
            $tossWinnerFlag=0;
    }
    $tossDecision=-1;    
    if(strpos($tossWinner,"bat") !== FALSE){
            $tossDecision=1;
    }
    if(strpos($tossWinner,"bowl") !== FALSE){
            $tossDecision=0;
    }    
    $matchResultFlag=-1;
    if(strpos($matchResult,$teamA) !== FALSE){
            $matchResultFlag=1;
    }
    if(strpos($matchResult,$teamB) !== FALSE){
            $matchResultFlag=0;
    }

    $fInningsSummary=$InningsDOM[0]->plaintext;
    $sInningsSummary=$InningsDOM[1]->plaintext;  
  
    $record = array(
            'IPL'=>$iplSeries,
            'match_url' =>  $el->href, 
            'Date' =>  $matchDate,
            'Team A'=>$teamA,
            'Team B'=>$teamB,          
            'Toss Winner'=>$tossWinner,
            'Toss Winner Flag'=>$tossWinnerFlag,
            'Toss Decision'=> $tossDecision,
            'Venue Type'=>$venueType,
            'Result Flag'=> $matchResultFlag,
            'Result'=> $matchResult,
            'First Inn. Summ.'=>$fInningsSummary,
            'Second Inn. Summ.'=>$sInningsSummary,
            'Venue'=>$venue          
        );
    scraperwiki::save(array('match_url'), $record);
    $scorecard_dom->__destruct();
   // $i++;
   // if($i===4) break;
} 

/* foreach($dom->find("table tr") as $data){

    $tds = $data->find("td");
    if(count($tds)==2){
        $record = array(
            'match_description' => $tds[0]->plaintext, 
            'date' => $tds[1]->plaintext
        );
        //scraperwiki::save(array('date'), $record);
    }
} */

?>
