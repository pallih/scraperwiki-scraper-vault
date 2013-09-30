<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
//https://scraperwiki.com/scrapers/new/php?template=php-tutorial-2#
//https://scraperwiki.com/scrapers/new/python?template=advanced-scraping-pdfs
require 'scraperwiki/simple_html_dom.php';
/*
$html_content = scraperwiki::scrape("http://cpxip.com/coronado.html");
$html = str_get_html($html_content);
$el = $html->find("div#divFrameInfo",0);

echo $el->plaintext . "\n";
*/


/*
$html = scraperwiki::scrape("http://cpxip.com/coronado.html");

$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
foreach ($dom->find("div#divFrameInfo p") as $p)
    array_push($arr, $p->plaintext);

print_r($arr);
*/






$html = scraperwiki::scrape("http://cpxip.com/coronado.html");
$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
$arr1 = array();
$arrDesc = array();


foreach ($dom->find("div#divFrameInfo p") as $p){
    array_push($arrDesc, $p->plaintext);
}
$arrDesc[7] = $arrDesc[7] . $arrDesc[8];
$arrDesc[10] = $arrDesc[10] . $arrDesc[11];

//print_r($arrDesc);


foreach ($dom->find("ul#ulModels") as $ul){

    foreach ($ul->find("li") as $li){
    array_push($arr, $li->innertext);
    array_push($arr1, $li->plaintext);
    } //end foreach li
} //end foreach ul#ulModels

$arrName = array();
foreach ($dom->find("#MainContent_ucFrameViewer_lblStyleName") as $sn){
    array_push($arrName, $sn->plaintext);
    } //end foreach sn

//print_r($arrName);

$arrBrand = array();
foreach ($dom->find("#MainContent_ucFrameViewer_imgLogo span") as $bn){
    array_push($arrBrand, $bn->plaintext);
    } //end foreach sn
$arrBrand = str_replace("-", "", $arrBrand);
//print_r($arrBrand);


$temparr = array();
$temparr1 = array();
$temparr2 = array();
$temparr3 = array();
$arrofarr = array();
for ($i=0; $i<count($arr); $i++){
     $temparr = explode("this,", $arr[$i]);
     $temparr1 = explode(")", $temparr[1]);
     //array_push($temparr2, explode(",", $temparr1[0]));
     $temparr2 = explode(",", $temparr1[0]);
     //stripslashes($temparr2[0]);
     $temparr2[0] = str_replace("'", "",$temparr2[0]);
     $temparr2[1] = str_replace("'", "",$temparr2[1]);
     $temparr2[2] = str_replace("'", "",$temparr2[2]);
     //$temparr2[0] = trim($temparr2[0], "'");
     $temparr2[3] = $arr1[$i];
     array_push($arrofarr, $temparr2);
   // print_r($temparr2);
} //end for count($arr)

//print_r($arrofarr);
//print_r($arrofarr[2][2]);
//print_r($temparr2);

$arrDescStr = "<p>" . $arrDesc[0] . "</p><p>" . $arrDesc[1] . "</p><p>" .  $arrDesc[2] . "</p><p>" .  $arrDesc[3] . "</p><p>" .  $arrDesc[4] . "</p><p>".  $arrDesc[5] . "</p><p>".  $arrDesc[6] . "</p><p>".  $arrDesc[7] . "</p><p>".  $arrDesc[9] . "</p><p>".  $arrDesc[10] . "</p><p>";


$str = $arrofarr[0][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[0][1] . "; " . $arrofarr[0][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[0][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[0][0] . ";" . ";;;";

echo $str ;
echo "****************************" ;


$str1 = $arrofarr[1][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[1][1] . "; " . $arrofarr[1][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[1][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[1][0] . ";" . ";;;";

echo $str1;
echo "****************************" ;

$str2 = $arrofarr[2][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[2][1] . "; " . $arrofarr[2][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[2][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[2][0] . ";" . ";;;";

echo $str2;
//print_r($arr);
scraperwiki::save_var('fomt', $str2); 
?>
<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
//https://scraperwiki.com/scrapers/new/php?template=php-tutorial-2#
//https://scraperwiki.com/scrapers/new/python?template=advanced-scraping-pdfs
require 'scraperwiki/simple_html_dom.php';
/*
$html_content = scraperwiki::scrape("http://cpxip.com/coronado.html");
$html = str_get_html($html_content);
$el = $html->find("div#divFrameInfo",0);

echo $el->plaintext . "\n";
*/


/*
$html = scraperwiki::scrape("http://cpxip.com/coronado.html");

$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
foreach ($dom->find("div#divFrameInfo p") as $p)
    array_push($arr, $p->plaintext);

print_r($arr);
*/






$html = scraperwiki::scrape("http://cpxip.com/coronado.html");
$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
$arr1 = array();
$arrDesc = array();


foreach ($dom->find("div#divFrameInfo p") as $p){
    array_push($arrDesc, $p->plaintext);
}
$arrDesc[7] = $arrDesc[7] . $arrDesc[8];
$arrDesc[10] = $arrDesc[10] . $arrDesc[11];

//print_r($arrDesc);


foreach ($dom->find("ul#ulModels") as $ul){

    foreach ($ul->find("li") as $li){
    array_push($arr, $li->innertext);
    array_push($arr1, $li->plaintext);
    } //end foreach li
} //end foreach ul#ulModels

$arrName = array();
foreach ($dom->find("#MainContent_ucFrameViewer_lblStyleName") as $sn){
    array_push($arrName, $sn->plaintext);
    } //end foreach sn

//print_r($arrName);

$arrBrand = array();
foreach ($dom->find("#MainContent_ucFrameViewer_imgLogo span") as $bn){
    array_push($arrBrand, $bn->plaintext);
    } //end foreach sn
$arrBrand = str_replace("-", "", $arrBrand);
//print_r($arrBrand);


$temparr = array();
$temparr1 = array();
$temparr2 = array();
$temparr3 = array();
$arrofarr = array();
for ($i=0; $i<count($arr); $i++){
     $temparr = explode("this,", $arr[$i]);
     $temparr1 = explode(")", $temparr[1]);
     //array_push($temparr2, explode(",", $temparr1[0]));
     $temparr2 = explode(",", $temparr1[0]);
     //stripslashes($temparr2[0]);
     $temparr2[0] = str_replace("'", "",$temparr2[0]);
     $temparr2[1] = str_replace("'", "",$temparr2[1]);
     $temparr2[2] = str_replace("'", "",$temparr2[2]);
     //$temparr2[0] = trim($temparr2[0], "'");
     $temparr2[3] = $arr1[$i];
     array_push($arrofarr, $temparr2);
   // print_r($temparr2);
} //end for count($arr)

//print_r($arrofarr);
//print_r($arrofarr[2][2]);
//print_r($temparr2);

$arrDescStr = "<p>" . $arrDesc[0] . "</p><p>" . $arrDesc[1] . "</p><p>" .  $arrDesc[2] . "</p><p>" .  $arrDesc[3] . "</p><p>" .  $arrDesc[4] . "</p><p>".  $arrDesc[5] . "</p><p>".  $arrDesc[6] . "</p><p>".  $arrDesc[7] . "</p><p>".  $arrDesc[9] . "</p><p>".  $arrDesc[10] . "</p><p>";


$str = $arrofarr[0][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[0][1] . "; " . $arrofarr[0][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[0][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[0][0] . ";" . ";;;";

echo $str ;
echo "****************************" ;


$str1 = $arrofarr[1][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[1][1] . "; " . $arrofarr[1][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[1][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[1][0] . ";" . ";;;";

echo $str1;
echo "****************************" ;

$str2 = $arrofarr[2][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[2][1] . "; " . $arrofarr[2][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[2][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[2][0] . ";" . ";;;";

echo $str2;
//print_r($arr);
scraperwiki::save_var('fomt', $str2); 
?>
