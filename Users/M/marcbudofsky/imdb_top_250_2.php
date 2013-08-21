<?php
######################################
# Basic PHP scraper
######################################



$html = scraperwiki::scrape("http://www.imdb.com/chart/top");
$html = oneline($html);

    preg_match_all('|<tr bgcolor="#.*?" valign="top"><td align="right"><font face="Arial, Helvetica, sans-serif" size="-1"><b>(.*?)\.</b></font></td><td align="center"><font face="Arial, Helvetica, sans-serif" size="-1">(.*?)</font></td><td><font face="Arial, Helvetica, sans-serif" size="-1"><a href="(.*?)">(.*?)</a> \((.*?)\)</font></td><td align="right"><font face="Arial, Helvetica, sans-serif" size="-1">.*?</font></td></tr>|',$html,$arr);
    
    foreach ($arr[1] as $key=>$val) {
    scraperwiki::save(array('rank'), array('rank' => "".clean($arr[1][$key]),'rating' => clean($arr[2][$key]),
                                             'name' => clean($arr[4][$key]),'year' => clean($arr[5][$key]),
                                            'link' => clean('http://www.imdb.com'.$arr[3][$key])));    
    }


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