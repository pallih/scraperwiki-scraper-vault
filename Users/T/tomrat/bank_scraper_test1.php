<?php
//print "Hello, coding in the cloud!";  

$top_url = "http://www.aaadir.com/";           

require 'scraperwiki/simple_html_dom.php';           
//$dom = new simple_html_dom();
//$dom->load($top_url);

$l1_urls = array (
    //"continent/continent.jsp?cont_id=8&la=1",
    "continent/continent.jsp?cont_id=3&la=1",
    //"continent/continent.jsp?cont_id=7&la=1",
    //"continent/continent.jsp?cont_id=1&la=1",
    //"continent/continent.jsp?cont_id=4&la=1",
    //"continent/continent.jsp?cont_id=11&la=1",
    //"continent/continent.jsp?cont_id=9&la=1",
    //"continent/continent.jsp?cont_id=6&la=1",
    //"continent/continent.jsp?cont_id=2&la=1",
);
 
foreach($l1_urls as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v); 

    foreach($html->find('a[class=para]') as $element) {
        $a[] = $element->href;
    }
    $html->clear();
}
 
$b = array_unique($a);
//pv($b);
 
/*
$b = array(
    "/banks/countries/all/main.jsp?cont_id=8&alfa=C&country_id=31&la=1",
    "/banks/countries/all/main.jsp?cont_id=8&alfa=M&country_id=114&la=1",
 
);
*/
echo "<br>";echo "<br>";
 
foreach($b as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v);
 
    foreach($html->find('a[class=title_name]') as $element) {
        //echo $element->href . '<br>';
        $c[] = $element->href;
    }
    $html->clear();
 
}
 
//pv($c);
 
/*
$c = array(
    "/banks/countries/all/detail.jsp?cont_id=8&banktype=group&type=1&country_id=31&bank_id=12336&la=1",
    "/banks/countries/all/detail.jsp?cont_id=8&banktype=group&type=1&country_id=31&bank_id=9234&la=1",
 
);
*/
foreach ($c as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v);
 
    $t = $html->find('table[class=detail]',0);
 
    $n =  trim($t->find('h1[class=h1_titles]',0)->plaintext);
    $u =  trim($t->find('a[class=detail_field]',0)->plaintext);
    $a1 = trim($t->find('td[class=detail_field]',0)->plaintext);
    $a2 = trim($t->find('td[class=detail_field]',1)->plaintext);
    $a3 = trim($t->find('td[class=detail_field]',2)->plaintext);
    $p  = trim($t->find('td[class=detail_field]',4)->plaintext);
    $br  = trim($t->find('td[class=detail_field]',6)->plaintext);
    $ib  = trim($t->find('td[class=detail_field]',10)->plaintext);
 
    echo $n.', '.$u.', '.$a1.', '.a2.', '.$a3.', '.$p.', '.$ib.  '<br />';
    $html->clear();
}
 
function pv($x) {
    echo "<pre>\n";
    print_r($x);
    echo "</pre>\n";
}

?><?php
//print "Hello, coding in the cloud!";  

$top_url = "http://www.aaadir.com/";           

require 'scraperwiki/simple_html_dom.php';           
//$dom = new simple_html_dom();
//$dom->load($top_url);

$l1_urls = array (
    //"continent/continent.jsp?cont_id=8&la=1",
    "continent/continent.jsp?cont_id=3&la=1",
    //"continent/continent.jsp?cont_id=7&la=1",
    //"continent/continent.jsp?cont_id=1&la=1",
    //"continent/continent.jsp?cont_id=4&la=1",
    //"continent/continent.jsp?cont_id=11&la=1",
    //"continent/continent.jsp?cont_id=9&la=1",
    //"continent/continent.jsp?cont_id=6&la=1",
    //"continent/continent.jsp?cont_id=2&la=1",
);
 
foreach($l1_urls as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v); 

    foreach($html->find('a[class=para]') as $element) {
        $a[] = $element->href;
    }
    $html->clear();
}
 
$b = array_unique($a);
//pv($b);
 
/*
$b = array(
    "/banks/countries/all/main.jsp?cont_id=8&alfa=C&country_id=31&la=1",
    "/banks/countries/all/main.jsp?cont_id=8&alfa=M&country_id=114&la=1",
 
);
*/
echo "<br>";echo "<br>";
 
foreach($b as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v);
 
    foreach($html->find('a[class=title_name]') as $element) {
        //echo $element->href . '<br>';
        $c[] = $element->href;
    }
    $html->clear();
 
}
 
//pv($c);
 
/*
$c = array(
    "/banks/countries/all/detail.jsp?cont_id=8&banktype=group&type=1&country_id=31&bank_id=12336&la=1",
    "/banks/countries/all/detail.jsp?cont_id=8&banktype=group&type=1&country_id=31&bank_id=9234&la=1",
 
);
*/
foreach ($c as $k=>$v) {
    //$html = file_get_html($top_url.$v);
    $html = scraperWiki::scrape($top_url.$v);
 
    $t = $html->find('table[class=detail]',0);
 
    $n =  trim($t->find('h1[class=h1_titles]',0)->plaintext);
    $u =  trim($t->find('a[class=detail_field]',0)->plaintext);
    $a1 = trim($t->find('td[class=detail_field]',0)->plaintext);
    $a2 = trim($t->find('td[class=detail_field]',1)->plaintext);
    $a3 = trim($t->find('td[class=detail_field]',2)->plaintext);
    $p  = trim($t->find('td[class=detail_field]',4)->plaintext);
    $br  = trim($t->find('td[class=detail_field]',6)->plaintext);
    $ib  = trim($t->find('td[class=detail_field]',10)->plaintext);
 
    echo $n.', '.$u.', '.$a1.', '.a2.', '.$a3.', '.$p.', '.$ib.  '<br />';
    $html->clear();
}
 
function pv($x) {
    echo "<pre>\n";
    print_r($x);
    echo "</pre>\n";
}

?>