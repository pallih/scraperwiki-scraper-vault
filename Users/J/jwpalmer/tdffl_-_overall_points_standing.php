<?php
$tourStartDate = '2013-06-29';
$start = new DateTime($tourStartDate);
$today = new DateTime();
$interval = $start->diff($today);
$stage = $interval->format('%a')+1;
if ($stage < 24){

    $offset = 0;
    $restDay = false;
    //rest days after stage 9 (day 10) and after stage 15 (day 17)
    if ($stage == 10){ $restDay = true; }
    if ($stage > 10){ $offset++; }
    if ($stage == 17){ $restDay = true; }
    if ($stage > 17){ $offset++; }
    
    if ($offset > 0){ $stage = ($stage-$offset); }
    
    //$stage = 7;
    //stage 4 was a team time trial, results are completely different!
    //  http://www.letour.fr/le-tour/2013/us/400/classement/bloc-classement-page/ETE.html
    //echo "stage: ".$stage."\n";
    
    $url = "http://www.letour.fr/le-tour/2013/us/".$stage."00/classement/bloc-classement-page/ITE.html";
    //echo "path: ".$url."\n";
    
    
    if (!$restDay){
    
        $html = scraperWiki::scrape($url);
        require 'scraperwiki/simple_html_dom.php';           
        $dom = new simple_html_dom();
        $dom->load($html);
        $ptr = 0;
        foreach($dom->find("tbody tr") as $data){
            $tds = $data->find("td");
            if(count($tds)==6 && $ptr>1){
                $time = $tds[4]->plaintext;
                $hours = substr($time,0,2);
                $minutes = substr($time,4,2);
                $seconds = substr($time,8,2);
                $cmptime = ($hours*3600)+($minutes*60)+$seconds;
        
                $record = array(
                    'stage' => $stage,
                    'rank' => intval(str_replace(".","",$tds[0]->plaintext)),
                    'rider' => substr($tds[1]->plaintext,3),
                    'number' => $tds[2]->plaintext,
                    'team' => $tds[3]->plaintext,
                    'time' => $time,
                    'h' => $hours,
                    'm' => $minutes,
                    's' => $seconds,
                    'cmptime' => $cmptime,
                    'gap' => $tds[5]->plaintext
                );
                scraperwiki::save(array('rank','rider'),$record);
            }
            $ptr++;
        }

    
    }//end check for it being a rest day

}//end check for tour being over
?><?php
$tourStartDate = '2013-06-29';
$start = new DateTime($tourStartDate);
$today = new DateTime();
$interval = $start->diff($today);
$stage = $interval->format('%a')+1;
if ($stage < 24){

    $offset = 0;
    $restDay = false;
    //rest days after stage 9 (day 10) and after stage 15 (day 17)
    if ($stage == 10){ $restDay = true; }
    if ($stage > 10){ $offset++; }
    if ($stage == 17){ $restDay = true; }
    if ($stage > 17){ $offset++; }
    
    if ($offset > 0){ $stage = ($stage-$offset); }
    
    //$stage = 7;
    //stage 4 was a team time trial, results are completely different!
    //  http://www.letour.fr/le-tour/2013/us/400/classement/bloc-classement-page/ETE.html
    //echo "stage: ".$stage."\n";
    
    $url = "http://www.letour.fr/le-tour/2013/us/".$stage."00/classement/bloc-classement-page/ITE.html";
    //echo "path: ".$url."\n";
    
    
    if (!$restDay){
    
        $html = scraperWiki::scrape($url);
        require 'scraperwiki/simple_html_dom.php';           
        $dom = new simple_html_dom();
        $dom->load($html);
        $ptr = 0;
        foreach($dom->find("tbody tr") as $data){
            $tds = $data->find("td");
            if(count($tds)==6 && $ptr>1){
                $time = $tds[4]->plaintext;
                $hours = substr($time,0,2);
                $minutes = substr($time,4,2);
                $seconds = substr($time,8,2);
                $cmptime = ($hours*3600)+($minutes*60)+$seconds;
        
                $record = array(
                    'stage' => $stage,
                    'rank' => intval(str_replace(".","",$tds[0]->plaintext)),
                    'rider' => substr($tds[1]->plaintext,3),
                    'number' => $tds[2]->plaintext,
                    'team' => $tds[3]->plaintext,
                    'time' => $time,
                    'h' => $hours,
                    'm' => $minutes,
                    's' => $seconds,
                    'cmptime' => $cmptime,
                    'gap' => $tds[5]->plaintext
                );
                scraperwiki::save(array('rank','rider'),$record);
            }
            $ptr++;
        }

    
    }//end check for it being a rest day

}//end check for tour being over
?>