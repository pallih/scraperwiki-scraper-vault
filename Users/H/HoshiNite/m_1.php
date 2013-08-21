<?php

$curl = curl_init("http://www.4dresult.com.my/");
curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
$page = curl_exec($curl);
if(curl_errno($curl)) throw new Exception (curl_error($curl));
curl_close($curl);
 
$xpathExpr = '/html/body/form/table/tbody/tr[3]/td[1]/table/tr/td[2]/table[2]';


$dom = new DOMDocument;
if (!$dom->loadHTML($page)) throw new Exception (implode (",", libxml_get_errors()));
$xpath = new DOMXPath($dom);
$entries = $xpath->query($xpathExpr);
if (!$entries) throw new Exception ("XPath evaluation error");
foreach ($entries as $entry){
    $key = $entry->nodeValue;
}

$num = 1;
preg_match_all('/(\d{4})/', $key, $matches);
foreach ($matches[0] as $val){
    scraperwiki::save_var($num, $val);
    //print scraperwiki::get_var('last_page');
    $num++;   
}

$xpathExpr2 = '/html/body/form/table/tbody/tr[3]/td[1]/table/tr/td[2]/table[3]';
$entries2 = $xpath->query($xpathExpr2);
foreach ($entries2 as $entry2){
    $key2 = $entry2->nodeValue;
}
preg_match_all('/(\d{4})/', $key2, $matches2);
foreach ($matches2[0] as $val) {
    scraperwiki::save_var($num, $val);
    $num++;   
}


$xpathExpr3 = '/html/body/form/table/tbody/tr[3]/td[1]/table/tr/td[2]/table[1]';
$entries3 = $xpath->query($xpathExpr3);
foreach ($entries3 as $entry3){
    $key3 = $entry3->nodeValue;
}

$matches3 = explode(" ", $key3);
scraperwiki::save_var("day", $matches3[2]);

$match =  explode("\n", $matches3[1]);
scraperwiki::save_var("date", $match[2]);


//scraperwiki::save_var($num, $val);
//$num++;   




?>