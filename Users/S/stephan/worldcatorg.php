<?php
$run = true;
$i=1;
$start = 1;
do {
    $html = scraperwiki::scrape('http://www.worldcat.org/search?q=African+Americans&dblist=638'.
                                     '&fq=(((x0%3Avideo+x4%3Avhs)OR(x0%3Avideo+x4%3Advd)OR(x0%3Avideo+x4%3Afilm)'.
                                     'OR(x0%3Avideo+x4%3Adigital)))&start='.$start.
                                     '&se=&sd=&qt=facet_fm_pagelink&refinesearch=true&refreshFormat=undefined');

    $html = oneline($html);
    preg_match_all('|td class=&quot;coverart&quot;&gt;&lt;a href=&quot;(/title/.*?&amp;referer=brief_results)&quot;&gt;|',$html,$m);
   
    if (count($m[1])==0) { $run = false;}
    else {
       
        foreach ($m[1] as $key=>$val) {
         
            scraperwiki::save(array('id'), array('id' => $i,'link' => clean(addslashes($m[1][$key]))));
            $i++;
        }

    }
    $start = $start+10;

} while ($run==true);



function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
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
