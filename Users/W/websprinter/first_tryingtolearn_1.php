<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.writersservices.com/reference/b-personal-management-ltd");
$html = str_get_html($html_content);

//foreach ($html->find("div[id=logo] a") as $el) {
//foreach ($html->find("div.field-item", 0) as $el) {


$el=$html->find("div.pane-content", 0); //Company Name
$coname = $el->plaintext;
//print $el . "\n";
print $coname;

$el=$html->find("div.field-item", 0); //address
$address = $el->plaintext;
print $address . "\n";;


$el=$html->find("div.pane-content", 4); //description text
$codesc = $el->plaintext;
//print $el . "\n";
print $codesc . "\n";


$el=$html->find("div.pane-content", 5); // Company telephone
$cotel = $el->plaintext;
//print $el . "\n";
print $cotel . "\n";

$el=$html->find("div.pane-content", 7); //Company email
$coemail = $el->plaintext;
//print $el . "\n";
print $coemail . "\n";

$el=$html->find("div.pane-content", 8)->find("div.field-item a",0); //Company site
$cosite = $el->href;
//print $el . "\n";
print $cosite;

//}

?>

