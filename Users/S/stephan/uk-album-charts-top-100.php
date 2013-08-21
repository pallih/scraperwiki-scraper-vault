<?php
######################################
# Basic PHP scraper
######################################
date_default_timezone_set('Europe/London');

$html = scraperwiki::scrape("http://www.theofficialcharts.com/albums-chart/");

preg_match_all('|<span class="date"> - (.*?)</span>|',$html,$date);
$date = date('Y-m-d',strtotime($date[1][0]));
preg_match_all('|<td class="currentposition">(.*?)</td>|',$html,$arr);
$current = $arr[1];

preg_match_all('|<td class="lastposition">(.*?)</td>|',$html,$arr);
$last= $arr[1];

preg_match_all('|<td class="weeks">(.*?)</td>|',$html,$arr);
$weeks = $arr[1];

$html_oneline = str_replace("\r", "", $html);
$html_oneline= str_replace("\n", "", $html_oneline);

preg_match_all('|<div id="wide"><div class="infoHolder">   <img class="coverimage" src="(.*?)" />   <h4>(.*?)</h4>(.*?)<br />   <span class="label">\((.*?)\)</span>  </div>|i',$html_oneline,$arr);


$cover= $arr[1];
$song= $arr[2];
$artist= $arr[3];
$label= $arr[4];



    
foreach($song as $key=>$val) {
    scraperwiki::save(array('current','date'), array('date'=>$date,'current' => cleanText($current[$key]),'last' => cleanText($last[$key]),'weeks' => cleanText($weeks[$key]),'song' => cleanText($song[$key]),'artist' => cleanText($artist[$key]),'cover' => trim($cover[$key]),'label' => cleanText($label[$key]) ));
 
}
 

    function cleanText($str) {
        $str = html_entity_decode($str);
        
        $str = str_replace('&#039;',"'",$str);

        $str = trim($str);
        return($str);
    }
   
?>