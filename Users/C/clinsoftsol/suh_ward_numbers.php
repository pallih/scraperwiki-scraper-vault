<?php
require 'scraperwiki/simple_html_dom.php';

$url = "http://www.uhs.nhs.uk/ContactUs/Wardtelephonenumbers.aspx";

$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 
foreach ($dom->find('tr') as $tr) {
    $wardname = trim($tr->children(0)->plaintext);
    $wardname = str_replace("&nbsp;","",$wardname);
    $exts = trim($tr->children(1)->plaintext);
    $exts = str_replace("&nbsp;","",$exts);
    array_push($arr, "{ 'name': '".$wardname."', 'ext': '".$exts."' }");

    // Save in data store. First array says which columns are unique
    scraperwiki::save(array("WardName"),array("WardName"=>$wardname, "Exts"=>$exts));
    }
print json_encode($arr) . "\n";
?>
