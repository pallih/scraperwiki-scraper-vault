<?php
######################################
# Basic PHP scraper
######################################


$max = 10032586;
$counter = scraperwiki::get_metadata('counter');          

    for ($i=0; $i< 10; $i++) 

    {
        $counter++;
        if ($counter == $max) 
    {
            scraperwiki::save_metadata('counter',10000000); 
            $i= 1001;
    }
$html = oneline(scraperwiki::scrape("http://www.ukrlp.co.uk/ukrlp/ukrlp_provider.page_pls_provDetails?x=&pn_p_id=".$counter."&pv_status=VERIFIED&pv_vis_code=L"));

preg_match_all('|<div class="pod_main_body">(.*?<div )class="searchleft">|',$html,$arr);
   if (isset($arr[1][0])) { $code = $arr[1][0];} else { $code='';}
        if ($code!='') {

preg_match_all('|<div class="provhead">UKPRN: ([0-9]*?)</div>|',$code,$num);
 if (isset($num [1][0])) { $num  = trim($num [1][0]);} else { $num ='';}

preg_match_all('|</div>.*?<div class="provhead">(.*?)<|',$code,$name);
if (isset($name [1][0])) { $name = trim($name [1][0]);} else { $name ='';}

preg_match_all('|<div class="tradingname">Trading Name: <span>(.*?)</span></div>|',$code,$trading);
if (isset($trading[1][0])) { $trading = trim($trading[1][0]);} else { $trading='';}

preg_match_all('|<div class="assoc">Legal address</div>(.*?)<div|',$code,$legal);
if (isset($legal [1][0])) { $legal = trim($legal [1][0]);} else { $legal ='';}


preg_match_all('|<div class="assoc">Primary contact address</div>(.*?)<div|',$code,$primary);
if (isset($primary[1][0])) { $primary= trim($primary[1][0]);} else { $primary='';}

$primary = parseAddress($primary);
$legal= parseAddress($legal);
       
        if (trim($name)!='') 

{

$record=array('name' => clean($name),'trading' => clean($trading),'legal_address' => clean($legal['address']),'legal_phone' => clean($legal['phone']),'legal_fax' => clean($legal['fax']),'legal_email' => clean($legal['email']),'legal_web' => clean($legal['web']), 'primary_address' => clean($primary['address']),'primary_phone' => clean($primary['phone']), 'primary_fax' => clean($primary['fax']),'primary_email' => clean($primary['email']),'primary_web' => clean($primary['web']), 'primary_courses' => clean($primary['courses'])); 
 
scraperwiki::save(array('num'),$record); 
}
   
    scraperwiki::save_metadata('counter',$counter);  
    }
    }

    

function parseAddress($val) {

        preg_match_all('|<strong>Telephone: </strong>(.*?)<br />|',$val,$phone);
        if (isset($phone[1][0])) { $dat['phone'] = trim($phone[1][0]);} else { $dat['phone']='';}
        preg_match_all('|<strong>E-mail: </strong><a href="mailto:(.*?)">.*?</a><br />|',$val,$email);
        if (isset($email[1][0])) { $dat['email'] = trim($email[1][0]);} else { $dat['email']='';}
        preg_match_all('|<strong>Website: </strong><a target="_blank" href="(.*?)">.*?</a><br />|',$val,$web);
        if (isset($web[1][0])) { $dat['web'] = trim($web[1][0]);} else { $dat['web']='';}
        preg_match_all('|<strong>Fax: </strong>(.*?)<br />|',$val,$fax);
        if (isset($fax[1][0])) { $dat['fax'] = trim($fax[1][0]);} else { $dat['fax']='';}
        if (isset($courses[1][0])) { $dat ['courses'] = trim($courses[1][0]);} else { $dat['courses']='';}
        preg_match_all('|<strong>Courses: </strong>(.*?)<br />|',$val,$courses);
        $p = explode('<strong>',$val);
       
        $p = explode('<br />',$p[0]);
        
        $dat['address'] = '';
        foreach ($p as $a) {
            $a = trim($a);
            if ($a !='') {
                if ($dat['address']!='') { $dat['address'] .=', '; }
                $dat['address'] .= $a;
            }
        }
        if ($dat['address'] == 'Not specified. Please use the above.') {
        $dat['address'] = '';
        }

        return $dat;

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
