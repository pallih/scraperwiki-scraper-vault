<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';           

$sportday = new DateTime('2011-10-01');
for($i=0;$i<10;$i++){    
    $url = "http://www.scibet.com/betting-tips/".$sportday->format("Y-m-d")."/";
    $html = scraperWiki::scrape($url);        
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.canvas_body tr") as $data){
        $home="";
        $score="";
        $away="";
        $odds1 = "";
        $odds2 = "";
        $odds3 = "";
        $pred1="";
        $pred2="";
        $pred3="";
        $prediction="";
        $record = $data->find("td.home a");    
        if($record!=null){
            $home = $record[0]->innertext;            
        }
        $record = $data->find("td.score a");    
        if($record!=null){
            $score = $record[0]->innertext;            
        }
        $record = $data->find("td.away a");    
        if($record!=null){
            $away = $record[0]->innertext;            
        }    
        $record = $data->find("td.odds");    
        if($record!=null){
            $odds1 = $record[0]->innertext;    
            $odds2 = $record[1]->innertext;    
            $odds3 = $record[2]->innertext;            
        }
        $record = $data->find("td.prob table.prob");
        if($record!=null){
            $prediction = $record[0]->title;        
            $preds = preg_split("/[\s()]+/", $prediction);
            $pred1=$preds[1];
            $pred2=$preds[3];
            $pred3=$preds[5];
        }
        if($home!=""){
            $row = array(
                "date"=>$sportday,
                "home"=>$home,
                "away"=>$away,
                "score"=>$score,
                "hodds"=>$odds1,
                "dodds"=>$odds2,
                "aodds"=>$odds3,
                "hpred"=>$pred1,
                "dpred"=>$pred2,
                "spred"=>$pred3
            );            
            scraperwiki::save(array(), $row);
        }
    }
    $sportday->add(new DateInterval('P1D'));
}

?>
