<?php
######################################
# Basic PHP scraper
######################################



$html = scraperwiki::scrape("http://www.schoolwebindex.com/countries/england.php?religion=J");
$html = oneline($html);

    preg_match_all('|<tr.*?><td>(.*?)</td><td><a href=".*?">(.*?)</a></td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>|',$html,$arr);



    foreach ($arr[1] as $key=>$val) {
    scraperwiki::save(array('count'), array('count' => "".clean($arr[1][$key]),'school' => clean($arr[2][$key]),
                                             'location' => clean($arr[3][$key]),'county' => clean($arr[4][$key]),
                                            'type' => clean($arr[5][$key]),
                                            'religion' => clean($arr[6][$key]), 
                                            'classification' => clean($arr[7][$key]),
                                            'lea' => clean($arr[8][$key])));    
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

?><?php
######################################
# Basic PHP scraper
######################################



$html = scraperwiki::scrape("http://www.schoolwebindex.com/countries/england.php?religion=J");
$html = oneline($html);

    preg_match_all('|<tr.*?><td>(.*?)</td><td><a href=".*?">(.*?)</a></td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>|',$html,$arr);



    foreach ($arr[1] as $key=>$val) {
    scraperwiki::save(array('count'), array('count' => "".clean($arr[1][$key]),'school' => clean($arr[2][$key]),
                                             'location' => clean($arr[3][$key]),'county' => clean($arr[4][$key]),
                                            'type' => clean($arr[5][$key]),
                                            'religion' => clean($arr[6][$key]), 
                                            'classification' => clean($arr[7][$key]),
                                            'lea' => clean($arr[8][$key])));    
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