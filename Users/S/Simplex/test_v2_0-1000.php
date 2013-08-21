<?php

require 'scraperwiki/simple_html_dom.php';
mb_internal_encoding('UTF-8');


//create table
//scraperwiki::sqliteexecute("drop table radical");
//scraperwiki::sqliteexecute("create table radical (ID smallint, nazov varchar,kategoria varchar, cena varchar,zlavnena_cena varchar,perc_zlava smallint, vyrobca varchar,vaha varchar,short_detail varchar, detail varchar,image_url varchar)");
//scraperwiki::sqlitecommit();

function traducirHTML($cad){
    $cad=htmlspecialchars_decode($cad);
    $esp=array('&nbsp;','&Aacute;','&Auml;','&Ccaron;','&Dcaron;','&Eacute;','&Lacute;','&Lcaron;','&Ncaron;','&Oacute;','&Ocirc;','&Racute;','&Scaron;','&Tcaron;','&Uacute;','&Yacute;','&Zcaron;','&aacute;','&auml;','&ccaron;','&dcaron;','&eacute;','&lacute;','&lcaron;','&ncaron;','&oacute;','&ocirc;','&racute;','&scaron;','&tcaron;','&uacute;','&yacute;','&zcaron;','&Iacute;','&iacute;');
    $sust=array(' ','Á','Ä','Č','Ď','É','Ĺ','Ľ','Ň','Ó','Ô','Ŕ','Š','Ť','Ú','Ý','Ž','á','ä','č','ď','é','ĺ','ľ','ň','ó','ô','ŕ','š','ť','ú','ý','ž','Í','í');
    return str_replace($esp,$sust,$cad);
}



for($i=2500;$i<2501;$i++){
$url="http://radicalfishing.sk/product.php?id_product=".$i;
$html_content = scraperwiki::scrape($url);
$html = str_get_html($html_content);

//nazov produktu
$nazov = $html->find("div#primary_block h2",0); //print $nazov . "\n";
if($nazov==""){}else{
$nazov = $nazov->plaintext;
$nazov = traducirHTML($nazov);

//kategoria a subkategoria


$xkategoria="";
foreach ($html->find("span.navigation_end a") as $kategoria)
{ $xkategoria.=$kategoria->plaintext;$xkategoria.=",";

}
$xkategoria = substr($xkategoria, 0, -1);
$xkategoria = traducirHTML($xkategoria);
//print $xkategoria;


//--------------------------------------DETAIL-----------------------------

$detail_all="";
$test4="";
foreach ($html->find("div#more_info_sheets p") as $detail2) { //print $detail->plaintext . "\n";
$test3 = $detail2;
$test3 = preg_replace('<<strong>>', '', $test3);
$test3 = preg_replace('<</strong>>', '', $test3);
$test3 = preg_replace('<<span style="font-size: small;">>', '', $test3);
$test3 = preg_replace('<<span style="color: #ff0000;">>', '', $test3);
$test3 = preg_replace('<<span style="color: #000000;">>', '', $test3);
$test3 = preg_replace('<</span>>', '', $test3);
$test3 = preg_replace("/'/", '&prime;', $test3);
$test3 = preg_replace('/background-color: #ff6600;/', 'border-collapse:collapse;', $test3);
//$test = $detail->plaintext;
$test3 = preg_replace('/\s+/', ' ', $test3);
//$testx = $test3->plaintext;
$test4 .= $test3;
//$detail_all = $test3;
}

$detail = $html->find("div#more_info_sheets ul",0);
$test = $detail;

$test = preg_replace('<<strong>>', '', $test);
$test = preg_replace('<</strong>>', '', $test);
$test = preg_replace("/'/", '&prime;', $test);
$test = preg_replace('<<span style="font-size: small;">>', '', $test);
$test = preg_replace('<<span style="color: #ff0000;">>', '', $test);
$test = preg_replace('<<span style="color: #000000;">>', '', $test);
$test = preg_replace('<</span>>', '', $test);

//$test = $detail->plaintext;
//$test = preg_replace('/\s+/', ' ', $test);
//$detail_all = $test;

//--------------------------------------DETAIL END-----------------------------
$detail_all= $test4.$test;

//--------------------------------------SHORT DETAIL-----------------------------

$short_detail="";
$test11="";
foreach ($html->find("div#short_description_content p") as $detail10) { //print $detail->plaintext . "\n";
$test10 = $detail10;
$test10 = preg_replace('<<strong>>', '', $test10);
$test10 = preg_replace('<</strong>>', '', $test10);
$test10 = preg_replace('<<span style="font-size: small;">>', '', $test10);
$test10 = preg_replace('<<span style="color: #ff0000;">>', '', $test10);
$test10 = preg_replace('<<span style="color: #000000;">>', '', $test10);
$test10 = preg_replace('<</span>>', '', $test10);
$test10 = preg_replace("/'/", '&prime;', $test10);
$test10 = preg_replace('/\s+/', ' ', $test10);
//$testx = $test3->plaintext;
$test11 .= $test10;
//$detail_all = $test3;
}

$detail9 = $html->find("div#short_description_content ul",0);
$test9 = $detail9;

$test9 = preg_replace('<<strong>>', '', $test9);
$test9 = preg_replace('<</strong>>', '', $test9);
$test9 = preg_replace("/'/", '&prime;', $test9);
$test9 = preg_replace('<<span style="font-size: small;">>', '', $test9);
$test9 = preg_replace('<<span style="color: #ff0000;">>', '', $test9);
$test9 = preg_replace('<<span style="color: #000000;">>', '', $test9);
$test9 = preg_replace('<</span>>', '', $test9);

//$test = $detail->plaintext;
//$test = preg_replace('/\s+/', ' ', $test);
//$detail_all = $test;

//--------------------------------------SHORT DETAIL END-----------------------------
$short_detail= $test11.$test9;




//percentualna zlava
$perc_zlava = $html->find("span#reduction_percent_display",0); //print $nazov . "\n";
$perc_zlava = $perc_zlava->plaintext;


// cena
if($perc_zlava==""){$cena_div="span#our_price_display";}else{$cena_div="span#old_price_display";}
foreach ($html->find($cena_div) as $cena) { /*print $cena->plaintext . "\n";*/
$test2x = $cena->plaintext;
$test2x = explode(" ", $test2x);
$cena = $test2x[0];
}


// zlavnena cena
if($perc_zlava==""){}else{
foreach ($html->find("span#our_price_display") as $zlavnena_cena) { /*print $cena->plaintext . "\n";*/
$test2 = $zlavnena_cena->plaintext;
$test2 = explode(" ", $test2);
$zlavnena_cena = $test2[0];
}
}//koniec if

//vyrobca
$vyrobca="";

$vyrobca=$html->find("span.navigation_end a",0); 
$vyrobca=$vyrobca->plaintext;
$vyrobca = traducirHTML($vyrobca);
//print $vyrobca. "\n";




//image url





$atribut='_';
foreach ($html->find("div#attributes label") as $atribut) {
$atribut = $atribut->plaintext;
$atribut = preg_replace("/:/", '', $atribut);
//echo $atribut;
}



$option_all='';
foreach ($html->find("div#attributes option") as $option) {
$option = $option->plaintext;
//$atribut = preg_replace("/:/", '', $atribut);
$option_all .= $option. "|";
}

$option_all = substr($option_all, 0, -1);
if($option_all==""){$option_all="_";}
//echo $option_all;


//----------------

$option_curent_all='';
foreach ($html->find("div#attributes option") as $option_curent) {
//$option_curent = $option->plaintext;
$pos = strrpos($option_curent, "selected");
if ($pos === false) {}else{$option_curent_all = $option_curent->plaintext;}
}
//echo $option_curent_all;


//----------------

/*
foreach ($html->find("div#image-block img") as $image) { 
$image = $image->src;
}
*/
$other_img_all='';
foreach ($html->find("ul#thumbs_list_frame a") as $other_img) {
$other_img = $other_img->href;
$other_img_all .= "http://radicalfishing.sk".$other_img. ",";   
}
//print $other_img;
$other_img_all = substr($other_img_all, 0, -1);
/*if($other_img==$image){$imagex="http://www.mikbaits.eu".$image;}else{$imagex="http://www.mikbaits.eu".$image . ",". $other_img_all;}
*/
$imagex=$other_img_all;
//print $imagex;



scraperwiki::sqliteexecute("insert into radical (ID, nazov,kategoria, cena,zlavnena_cena,perc_zlava,vyrobca,vaha,short_detail, detail, image_url) values ('$i', '$nazov','$xkategoria', '$cena','$zlavnena_cena','$perc_zlava','$vyrobca','','$short_detail','$detail_all','$imagex')");
scraperwiki::sqlitecommit();

$vyrobca="";
$cena="";
$zlavnena_cena="";
$perc_zlava="";
$imagex="";



//print_r(scraperwiki::sqliteexecute("select * from mikbaits"));
}//koniec if nazov
}

?>