<?php
######################################
# Basic PHP scraper
######################################

$html = scraperwiki::scrape("http://www.apple.com/euro/itunes/charts/top10rocksongs.html");
$html = oneline($html);

preg_match_all('|<div class="boxcap captop"></div>(.*?)</ol>|',$html,$arr);
$counter = 0;
foreach ($arr[1] as $key=>$val) {
    preg_match_all('|<h2>(.*?)</h2>|',$val,$c);
    preg_match_all('|<li><a href="(.*?)"><strong>(.*?)</strong></a><br /><a href=".*?"><span>(.*?)</span></a>.*?</li>|',$val,$a);
    $position=0;
    foreach ($a[1] as $key=>$val) {
        scraperwiki::save(array('id'), array('id' => "".$counter,'country' => $c[1][0],'position' => "".++$position,'artist' => clean($a[3][$key]),'song' => clean($a[2][$key]),'link' => $a[1][$key]));
$counter++;
    }


}



    function clean($val) {
        $val = str_replace('&nbsp;','',$val);
        $val = str_replace('&amp;','&',$val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }
    
    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        return $code;
    }

?>