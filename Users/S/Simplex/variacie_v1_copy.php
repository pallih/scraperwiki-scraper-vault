<?php

require 'scraperwiki/simple_html_dom.php';

//create table
//scraperwiki::sqliteexecute("drop table radical_more");
//scraperwiki::sqliteexecute("create table radical_more (ID smallint, moznosti varchar, cena varchar, vaha varchar, predvolene smallint,image_url varchar)");
//scraperwiki::sqlitecommit();

function traducirHTML($cad){
    $cad=htmlspecialchars_decode($cad);
    $esp=array('&nbsp;','&Aacute;','&Auml;','&Ccaron;','&Dcaron;','&Eacute;','&Lacute;','&Lcaron;','&Ncaron;','&Oacute;','&Ocirc;','&Racute;','&Scaron;','&Tcaron;','&Uacute;','&Yacute;','&Zcaron;','&aacute;','&auml;','&ccaron;','&dcaron;','&eacute;','&lacute;','&lcaron;','&ncaron;','&oacute;','&ocirc;','&racute;','&scaron;','&tcaron;','&uacute;','&yacute;','&zcaron;','&Iacute;','&iacute;');
    $sust=array(' ','Á','Ä','Č','Ď','É','Ĺ','Ľ','Ň','Ó','Ô','Ŕ','Š','Ť','Ú','Ý','Ž','á','ä','č','ď','é','ĺ','ľ','ň','ó','ô','ŕ','š','ť','ú','ý','ž','Í','í');
    return str_replace($esp,$sust,$cad);
}

function get_between($input, $start, $end) 
{ 
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1)); 
  return $substr; 
} 


function get_between2($input2, $start2, $end2) 
{ 
  $substr2 = substr($input2, strlen($start2)+strpos($input2, $start2),strlen($input2));
  $substr3 = substr($substr2,0,(strlen($substr2) - strpos($substr2, $end2))*(-1));
  return $substr3; 
} 


$vaha="";

for($i=4070;$i<4100;$i++){
$url="http://radicalfishing.sk/product.php?id_product=" . $i;
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);


//

//percentualna zlava
$perc_zlava = $html->find("span#reduction_percent_display",0); //print $nazov . "\n";
$perc_zlava = $perc_zlava->plaintext;


//////////////////////////////////////////////////////////////////////////////////////

// cena_zaklad
if($perc_zlava==""){$cena_div="span#our_price_display";}else{$cena_div="span#old_price_display";}
foreach ($html->find($cena_div) as $cena_zaklad) { /*print $cena->plaintext . "\n";*/
$test2x = $cena_zaklad->plaintext;
$test2x = explode(" ", $test2x);
$cena_zaklad = $test2x[0];
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////




$other_img_all='';
$other_img = $html->find("ul#thumbs_list_frame a",0);
$other_img = $other_img->href;
$other_img_all .= "http://www.radicalfishing.sk".$other_img;   
$imagex=$other_img_all;
//print $imagex;


$f=0;
foreach ($html->find("div#attributes p") as $postual) { //postual begin

foreach ($postual->find("label") as $atribut) {
$atribut = $atribut->plaintext;
$atribut = substr($atribut, 0, -2);
//print $atribut;

for($xxx=0;($postual->find("option",$xxx))!="";$xxx++){

$option_curent= $postual->find("option",$xxx);
$option_number= $postual->find("option",$xxx);
$pos = strrpos($option_curent, "selected");
if ($pos === false) {$dodatok = 0;}else{$dodatok = 1;}
$option_curent = $option_curent->plaintext;
$option_number = $option_number->value;



$moznosti[$xxx] = $option_number . "|" . $atribut . ": " . $option_curent ."|". $dodatok;
$moznosti[$xxx] =traducirHTML($moznosti[$xxx]);
$moznostix=explode("|",$moznosti[$xxx]);
//print $moznostix[2] . "\n";
$ulozm[$f]=$moznosti[$xxx];
$f++;

}

}

} //postual end

$a = "// Combinations"; 
$b = "// Colors";
$go=get_between($html, $a, $b);
$gox=explode(";",$go);
$nr = count(explode(";",$go));
for($gox_pom=0;$gox_pom<$nr-1;$gox_pom++){
$medzikus=get_between($gox[$gox_pom],"('","')") . "|".get_between2($gox[$gox_pom],"'), 1, ",",");
$medzikus=str_replace("'","",$medzikus);
//print $nr ."\n";
$medzikus=explode("|",$medzikus);
$cena_zaklad=str_replace(",",".",$cena_zaklad);
$cena=$cena_zaklad + $medzikus[1];$cena = number_format($cena, 2, ',', '');

//zaciatok if
for($d=0;$d<$f;$d++){
$moznostix=explode("|",$ulozm[$d]);
$medzifinal=explode(",",$medzikus[0]);

if($medzifinal[0]==$moznostix[0]){$prvy= str_replace($moznostix[0],$moznostix[1],$medzifinal[0]);$zhoda1=$moznostix[2];}
if($medzifinal[1]==$moznostix[0]){$druhy= str_replace($moznostix[0],$moznostix[1],$medzifinal[1]);$zhoda2=$moznostix[2];}

//print $medzikus[0] ." Y\n";
//print $medzifinal[1] ." X\n";


 }

//print $zhoda1 ." Y\n";
//print $zhoda2 ." X\n";

if($druhy==""){$finalb=$prvy;if($zhoda1==1){$predvolene=1;}else{$predvolene=0;}}else{$finalb=$prvy.",".$druhy;if($zhoda1==1 && $zhoda2==1){$predvolene=1;}else{$predvolene=0;}}


scraperwiki::sqliteexecute("insert into radical_more (ID, moznosti, cena, vaha, predvolene,image_url) values ('$i','$finalb','$cena', '$vaha','$predvolene','$imagex')");
scraperwiki::sqlitecommit();

}







$prvy="";
$druhy="";
$cena="";
$perc_zlava="";
$imagex="";
$xxx="";


//print_r(scraperwiki::sqliteexecute("select * from mikbaits"));

}




?><?php

require 'scraperwiki/simple_html_dom.php';

//create table
//scraperwiki::sqliteexecute("drop table radical_more");
//scraperwiki::sqliteexecute("create table radical_more (ID smallint, moznosti varchar, cena varchar, vaha varchar, predvolene smallint,image_url varchar)");
//scraperwiki::sqlitecommit();

function traducirHTML($cad){
    $cad=htmlspecialchars_decode($cad);
    $esp=array('&nbsp;','&Aacute;','&Auml;','&Ccaron;','&Dcaron;','&Eacute;','&Lacute;','&Lcaron;','&Ncaron;','&Oacute;','&Ocirc;','&Racute;','&Scaron;','&Tcaron;','&Uacute;','&Yacute;','&Zcaron;','&aacute;','&auml;','&ccaron;','&dcaron;','&eacute;','&lacute;','&lcaron;','&ncaron;','&oacute;','&ocirc;','&racute;','&scaron;','&tcaron;','&uacute;','&yacute;','&zcaron;','&Iacute;','&iacute;');
    $sust=array(' ','Á','Ä','Č','Ď','É','Ĺ','Ľ','Ň','Ó','Ô','Ŕ','Š','Ť','Ú','Ý','Ž','á','ä','č','ď','é','ĺ','ľ','ň','ó','ô','ŕ','š','ť','ú','ý','ž','Í','í');
    return str_replace($esp,$sust,$cad);
}

function get_between($input, $start, $end) 
{ 
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1)); 
  return $substr; 
} 


function get_between2($input2, $start2, $end2) 
{ 
  $substr2 = substr($input2, strlen($start2)+strpos($input2, $start2),strlen($input2));
  $substr3 = substr($substr2,0,(strlen($substr2) - strpos($substr2, $end2))*(-1));
  return $substr3; 
} 


$vaha="";

for($i=4070;$i<4100;$i++){
$url="http://radicalfishing.sk/product.php?id_product=" . $i;
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);


//

//percentualna zlava
$perc_zlava = $html->find("span#reduction_percent_display",0); //print $nazov . "\n";
$perc_zlava = $perc_zlava->plaintext;


//////////////////////////////////////////////////////////////////////////////////////

// cena_zaklad
if($perc_zlava==""){$cena_div="span#our_price_display";}else{$cena_div="span#old_price_display";}
foreach ($html->find($cena_div) as $cena_zaklad) { /*print $cena->plaintext . "\n";*/
$test2x = $cena_zaklad->plaintext;
$test2x = explode(" ", $test2x);
$cena_zaklad = $test2x[0];
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////




$other_img_all='';
$other_img = $html->find("ul#thumbs_list_frame a",0);
$other_img = $other_img->href;
$other_img_all .= "http://www.radicalfishing.sk".$other_img;   
$imagex=$other_img_all;
//print $imagex;


$f=0;
foreach ($html->find("div#attributes p") as $postual) { //postual begin

foreach ($postual->find("label") as $atribut) {
$atribut = $atribut->plaintext;
$atribut = substr($atribut, 0, -2);
//print $atribut;

for($xxx=0;($postual->find("option",$xxx))!="";$xxx++){

$option_curent= $postual->find("option",$xxx);
$option_number= $postual->find("option",$xxx);
$pos = strrpos($option_curent, "selected");
if ($pos === false) {$dodatok = 0;}else{$dodatok = 1;}
$option_curent = $option_curent->plaintext;
$option_number = $option_number->value;



$moznosti[$xxx] = $option_number . "|" . $atribut . ": " . $option_curent ."|". $dodatok;
$moznosti[$xxx] =traducirHTML($moznosti[$xxx]);
$moznostix=explode("|",$moznosti[$xxx]);
//print $moznostix[2] . "\n";
$ulozm[$f]=$moznosti[$xxx];
$f++;

}

}

} //postual end

$a = "// Combinations"; 
$b = "// Colors";
$go=get_between($html, $a, $b);
$gox=explode(";",$go);
$nr = count(explode(";",$go));
for($gox_pom=0;$gox_pom<$nr-1;$gox_pom++){
$medzikus=get_between($gox[$gox_pom],"('","')") . "|".get_between2($gox[$gox_pom],"'), 1, ",",");
$medzikus=str_replace("'","",$medzikus);
//print $nr ."\n";
$medzikus=explode("|",$medzikus);
$cena_zaklad=str_replace(",",".",$cena_zaklad);
$cena=$cena_zaklad + $medzikus[1];$cena = number_format($cena, 2, ',', '');

//zaciatok if
for($d=0;$d<$f;$d++){
$moznostix=explode("|",$ulozm[$d]);
$medzifinal=explode(",",$medzikus[0]);

if($medzifinal[0]==$moznostix[0]){$prvy= str_replace($moznostix[0],$moznostix[1],$medzifinal[0]);$zhoda1=$moznostix[2];}
if($medzifinal[1]==$moznostix[0]){$druhy= str_replace($moznostix[0],$moznostix[1],$medzifinal[1]);$zhoda2=$moznostix[2];}

//print $medzikus[0] ." Y\n";
//print $medzifinal[1] ." X\n";


 }

//print $zhoda1 ." Y\n";
//print $zhoda2 ." X\n";

if($druhy==""){$finalb=$prvy;if($zhoda1==1){$predvolene=1;}else{$predvolene=0;}}else{$finalb=$prvy.",".$druhy;if($zhoda1==1 && $zhoda2==1){$predvolene=1;}else{$predvolene=0;}}


scraperwiki::sqliteexecute("insert into radical_more (ID, moznosti, cena, vaha, predvolene,image_url) values ('$i','$finalb','$cena', '$vaha','$predvolene','$imagex')");
scraperwiki::sqlitecommit();

}







$prvy="";
$druhy="";
$cena="";
$perc_zlava="";
$imagex="";
$xxx="";


//print_r(scraperwiki::sqliteexecute("select * from mikbaits"));

}




?>