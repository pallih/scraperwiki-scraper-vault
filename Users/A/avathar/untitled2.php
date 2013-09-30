
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = oneline(scraperwiki::scrape("http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm"));

    preg_match_all('|<tr.*?>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?</tr>|',$html,$arr);
$last = '';
$z = false;
foreach($arr[1] as $key=>$val) {

    if (strtolower(substr(clean($arr[1][$key]),0,1))=='z') {
        $z=true;
    }
    if ($z==true && strtolower(substr(clean($arr[1][$key]),0,1))!='z') {
        exit;
    }
   scraperwiki::save(array('country'), array('country' => clean($arr[1][$key]),'currency' => clean($arr[2][$key]),
                                             'alpha_code' => clean($arr[3][$key]),'num_code' => clean($arr[4][$key])));


}

    function clean($val) {
        $val = str_replace('&nbsp;','',$val);
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



<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = oneline(scraperwiki::scrape("http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm"));

    preg_match_all('|<tr.*?>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?<td valign="top">(.*?)</td>.*?</tr>|',$html,$arr);
$last = '';
$z = false;
foreach($arr[1] as $key=>$val) {

    if (strtolower(substr(clean($arr[1][$key]),0,1))=='z') {
        $z=true;
    }
    if ($z==true && strtolower(substr(clean($arr[1][$key]),0,1))!='z') {
        exit;
    }
   scraperwiki::save(array('country'), array('country' => clean($arr[1][$key]),'currency' => clean($arr[2][$key]),
                                             'alpha_code' => clean($arr[3][$key]),'num_code' => clean($arr[4][$key])));


}

    function clean($val) {
        $val = str_replace('&nbsp;','',$val);
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


