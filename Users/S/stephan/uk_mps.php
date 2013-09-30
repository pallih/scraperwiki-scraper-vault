<?php
######################################
# Basic PHP scraper
######################################



$html = scraperwiki::scrape("http://www.parliament.uk/mps-lords-and-offices/mps/");
$html = oneline($html);

  preg_match_all('|href="(/biographies/.*?)"|',$html,$r);

foreach ($r[1] as $key=>$val) {
    $html = scraperwiki::scrape("http://www.parliament.uk".$val);
    $html = oneline($html);

    preg_match_all('|<title>(.*?)</title>|',$html,$name);
    preg_match_all('|<h3 class="first">Constituency</h3>.*?<p>(.*?)</p>|',$html,$con);
    preg_match_all('|<h3>Party</h3>.*?<p>(.*?)</p>|',$html,$party);
    preg_match_all('|Tel:(.*?)<br />|',$html,$phone);
    preg_match_all('|Fax:(.*?)<br />|',$html,$fax);
    preg_match_all('|href="mailto:(.*?)">|',$html,$email);
    
    if (!isset($fax[1][0]))   { $fax[1][0] = '';}
    if (!isset($email[1][0])) { $email[1][0] = '';}
    if (!isset($phone[1][0])) { $phone[1][0] = '';}
    if (!isset($con[1][0]))   { $con[1][0] = '';}
    if (!isset($party[1][0])) { $party[1][0] = '';}

scraperwiki::save(array('id'), array('id' => "".$key,'name' => clean($name[1][0]),'constituency' => clean($con[1][0]),'party' => clean($party[1][0]), 'phone' => clean($phone[1][0]),    'fax' => clean($fax[1][0]),   'email' => clean($email[1][0])));
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



$html = scraperwiki::scrape("http://www.parliament.uk/mps-lords-and-offices/mps/");
$html = oneline($html);

  preg_match_all('|href="(/biographies/.*?)"|',$html,$r);

foreach ($r[1] as $key=>$val) {
    $html = scraperwiki::scrape("http://www.parliament.uk".$val);
    $html = oneline($html);

    preg_match_all('|<title>(.*?)</title>|',$html,$name);
    preg_match_all('|<h3 class="first">Constituency</h3>.*?<p>(.*?)</p>|',$html,$con);
    preg_match_all('|<h3>Party</h3>.*?<p>(.*?)</p>|',$html,$party);
    preg_match_all('|Tel:(.*?)<br />|',$html,$phone);
    preg_match_all('|Fax:(.*?)<br />|',$html,$fax);
    preg_match_all('|href="mailto:(.*?)">|',$html,$email);
    
    if (!isset($fax[1][0]))   { $fax[1][0] = '';}
    if (!isset($email[1][0])) { $email[1][0] = '';}
    if (!isset($phone[1][0])) { $phone[1][0] = '';}
    if (!isset($con[1][0]))   { $con[1][0] = '';}
    if (!isset($party[1][0])) { $party[1][0] = '';}

scraperwiki::save(array('id'), array('id' => "".$key,'name' => clean($name[1][0]),'constituency' => clean($con[1][0]),'party' => clean($party[1][0]), 'phone' => clean($phone[1][0]),    'fax' => clean($fax[1][0]),   'email' => clean($email[1][0])));
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