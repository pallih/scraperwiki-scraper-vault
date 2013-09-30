<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("delete from swdata");            


$urlList[0] = "http://www.scibet.com/betting-tips/soccer/england/";
$urlList[1] = "http://www.scibet.com/betting-tips/soccer/argentina/";
$urlList[2] = "http://www.scibet.com/betting-tips/soccer/brazil/";
$urlList[3] = "http://www.scibet.com/betting-tips/soccer/chile/";
$urlList[4] = "http://www.scibet.com/betting-tips/soccer/fifa/";
$urlList[5] = "http://www.scibet.com/betting-tips/soccer/france/";
$urlList[6] = "http://www.scibet.com/betting-tips/soccer/germany/";
$urlList[7] = "http://www.scibet.com/betting-tips/soccer/greece/";
$urlList[8] = "http://www.scibet.com/betting-tips/soccer/italy/";
$urlList[9] = "http://www.scibet.com/betting-tips/soccer/mexico/";
$urlList[10] = "http://www.scibet.com/betting-tips/soccer/poland/";
$urlList[11] = "http://www.scibet.com/betting-tips/soccer/spain/";
$urlList[12] = "http://www.scibet.com/betting-tips/soccer/turkey/";
$urlList[13] = "http://www.scibet.com/betting-tips/soccer/uefa/";


for($i=0;$i<14;$i++){    
    $url = $urlList[$i];    
    $html = scraperWiki::scrape($url);
            
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.canvas_body tr") as $data){
        $date="";
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
        $record = $data->find("td.date");
        if($record!=null){
            $date = $record[0]->innertext;           
        }
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
                "date"=>$date,
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
    sleep(20);
    //$sportday->add(new DateInterval('P1D'));
}

?>

<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("delete from swdata");            


$urlList[0] = "http://www.scibet.com/betting-tips/soccer/england/";
$urlList[1] = "http://www.scibet.com/betting-tips/soccer/argentina/";
$urlList[2] = "http://www.scibet.com/betting-tips/soccer/brazil/";
$urlList[3] = "http://www.scibet.com/betting-tips/soccer/chile/";
$urlList[4] = "http://www.scibet.com/betting-tips/soccer/fifa/";
$urlList[5] = "http://www.scibet.com/betting-tips/soccer/france/";
$urlList[6] = "http://www.scibet.com/betting-tips/soccer/germany/";
$urlList[7] = "http://www.scibet.com/betting-tips/soccer/greece/";
$urlList[8] = "http://www.scibet.com/betting-tips/soccer/italy/";
$urlList[9] = "http://www.scibet.com/betting-tips/soccer/mexico/";
$urlList[10] = "http://www.scibet.com/betting-tips/soccer/poland/";
$urlList[11] = "http://www.scibet.com/betting-tips/soccer/spain/";
$urlList[12] = "http://www.scibet.com/betting-tips/soccer/turkey/";
$urlList[13] = "http://www.scibet.com/betting-tips/soccer/uefa/";


for($i=0;$i<14;$i++){    
    $url = $urlList[$i];    
    $html = scraperWiki::scrape($url);
            
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.canvas_body tr") as $data){
        $date="";
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
        $record = $data->find("td.date");
        if($record!=null){
            $date = $record[0]->innertext;           
        }
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
                "date"=>$date,
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
    sleep(20);
    //$sportday->add(new DateInterval('P1D'));
}

?>

