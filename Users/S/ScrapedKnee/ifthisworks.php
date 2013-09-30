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


$arrPages = array();

//JohnVarvatos
$arrPages[0]= "v740.html";
$arrPages[1]= "v748.html";
$arrPages[2]= "v749.html";
$arrPages[3]= "v750.html";
$arrPages[4]= "v751.html";
$arrPages[5]= "v752-af.html";
$arrPages[6]= "v752.html";
$arrPages[7]= "v753-af.html";
$arrPages[8]= "v753.html";
$arrPages[9]= "v754.html";
$arrPages[10]= "v755.html";
$arrPages[11]= "v756-af.html";
$arrPages[12]= "v756.html";
$arrPages[13]= "v757.html";
$arrPages[14]= "v758.html";
$arrPages[15]= "v759.html";
$arrPages[16]= "v760.html";
$arrPages[17]= "v761.html";
$arrPages[18]= "v762.html";
$arrPages[19]= "v763.html";
$arrPages[20]= "v764.html";
$arrPages[21]= "v765-af.html";
$arrPages[22]= "v765.html";
$arrPages[23]= "v766-af.html";
$arrPages[24]= "v766.html";
$arrPages[25]= "v767-af.html";
$arrPages[26]= "v767.html";
$arrPages[27]= "v768-af.html";
$arrPages[28]= "v768.html";
$arrPages[29]= "v769-af.html";
$arrPages[30]= "v769.html";
$arrPages[31]= "v770-af.html";
$arrPages[32]= "v770.html";
$arrPages[33]= "v771.html";
$arrPages[34]= "v772.html";
$arrPages[35]= "v773-af.html";
$arrPages[36]= "v773.html";
$arrPages[37]= "v774-af.html";
$arrPages[38]= "v774.html";
$arrPages[39]= "v775.html";
$arrPages[40]= "v776.html";
$arrPages[41]= "v777-af.html";
$arrPages[42]= "v777.html";
$arrPages[43]= "v779-af.html";
$arrPages[44]= "v779.html";
$arrPages[45]= "v780-af.html";
$arrPages[46]= "v780.html";
$arrPages[47]= "v905.html";
$arrPages[48]= "v906.html";
$arrPages[49]= "v907.html";

//Converse Backstage
$arrPages[50]= "chart-topper.html";
$arrPages[51]= "chorus.html";
$arrPages[52]= "front-man.html";
$arrPages[53]= "half-stack.html";
$arrPages[54]= "in-studio.html";
$arrPages[55]= "lineup.html";
$arrPages[56]= "merch.html";
$arrPages[57]= "on-tour.html";
$arrPages[58]= "opening-band.html";
$arrPages[59]= "plugged-in.html";
$arrPages[60]= "record-deal.html";
$arrPages[61]= "reel.html";
$arrPages[62]= "roadie.html";
$arrPages[63]= "set-list.html";
$arrPages[64]= "the-close-talker.html";
$arrPages[65]= "the-entertainer.html";
$arrPages[66]= "the-showstopper.html";
$arrPages[67]= "the-sure-thing.html";
$arrPages[68]= "the-tall-tale-teller.html";
$arrPages[69]= "the-traveler.html";
$arrPages[70]= "ticket-holder.html";
$arrPages[71]= "venue.html";
$arrPages[72]= "wavelength.html";
$arrPages[73]= "will-call.html";
$arrPages[74]= "with-the-band.html";

//Converse Black Canvas Sun
$arrPages[75]= "american-dream.html";
$arrPages[76]= "birdie.html";
$arrPages[77]= "breakdown-lane.html";
$arrPages[78]= "converseations.html";
$arrPages[79]= "daring.html";
$arrPages[80]= "endorser.html";
$arrPages[81]= "forum.html";
$arrPages[82]= "foxing.html";
$arrPages[83]= "hall-of-fame.html";
$arrPages[84]= "independence.html";
$arrPages[85]= "maximum-traction.html";
$arrPages[86]= "play-on.html";
$arrPages[87]= "reinvented.html";
$arrPages[88]= "tournament.html";
$arrPages[89]= "triple-treads.html";
$arrPages[90]= "truer-bounce.html";
$arrPages[91]= "well-played.html";
$arrPages[92]= "what-s-new.html";
$arrPages[93]= "who-knows.html";
$arrPages[94]= "world-champion.html";

//Converse Star Chevron
$arrPages[95]= "buzzer-beater.html";
$arrPages[96]= "in-the-mix.html";
$arrPages[97]= "offense.html";
$arrPages[98]= "on-deck.html";
$arrPages[99]= "overtime.html";
$arrPages[100]= "turnover.html";

//Luck Brand
$arrPages[101]= "aurora.html";
$arrPages[102]= "beach-bum.html";
$arrPages[103]= "bootcut.html";
$arrPages[104]= "boyfriend.html";
$arrPages[105]= "capitola.html";
$arrPages[106]= "day-break.html";
$arrPages[107]= "flare.html";
$arrPages[108]= "highlander.html";
$arrPages[109]= "hyannis.html";
$arrPages[110]= "indigo.html";
$arrPages[111]= "interlude.html";
$arrPages[112]= "kennedy.html";
$arrPages[113]= "local.html";
$arrPages[114]= "midnight.html";
$arrPages[115]= "moon-beam.html";
$arrPages[116]= "night.html";
$arrPages[117]= "nocturnal.html";
$arrPages[118]= "oceana.html";
$arrPages[119]= "recruiter.html";
$arrPages[120]= "refrain.html";
$arrPages[121]= "resort.html";
$arrPages[122]= "sun-kiss.html";
$arrPages[123]= "super-skinny.html";
$arrPages[124]= "sync.html";

//Tumi Sun
$arrPages[125]= "bixby-af.html";
$arrPages[126]= "bixby.html";
$arrPages[127]= "brooklyn.html";
$arrPages[128]= "capilano.html";
$arrPages[129]= "coronado-af.html";
$arrPages[130]= "coronado.html";
$arrPages[131]= "kawazu.html";
$arrPages[132]= "malone-af.html";
$arrPages[133]= "malone.html";
$arrPages[134]= "newport.html";
$arrPages[135]= "severn-af.html";
$arrPages[136]= "severn.html";
$arrPages[137]= "stari-af.html";
$arrPages[138]= "stari.html";
$arrPages[139]= "tacoma-af.html";
$arrPages[140]= "tacoma.html";
$arrPages[141]= "tobin.html";
$arrPages[142]= "vasco.html";





$intPrice = 0.00;
$strCat = "";
$intTaxRule = 30;
$intRetail = 0.00;
$strBrah = "";


//for ($k=0; $k<143; $k++){


for ($k=99; $k<143; $k++){
$strPage = "http://cpxip.com/" . $arrPages[$k];
$html = scraperwiki::scrape($strPage);
//$html = scraperwiki::scrape("http://cpxip.com/coronado.html");
$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
$arr1 = array();
$arrDesc = array();


//John Varvatos Book
if (($k ==0) ||($k==49)){ $intPrice = 160;}
if ($k == 1){ $intPrice = 115;}
if (($k >= 2 && $k<=19) || ($k==22) || ($k==39) || ($k==40)){$intPrice = 100;}
if (($k==20) || ($k==23) || ($k==24) || ($k >= 27 && $k<=30)|| ($k==35) || ($k==36) || ($k==43) || ($k==44)){$intPrice = 110;}
if (($k==25) || ($k==26) || ($k >= 31 && $k<=34)|| ($k==37) || ($k==38) || ($k==41) || ($k==42)){$intPrice = 120;}
if (($k ==45) ||($k==46)){ $intPrice = 130;}
if (($k ==47) ||($k==48)){ $intPrice = 180;}

//Converse Backstage
if ($k >49 && $k<75){$intPrice = 29;}


//Converse Black Canvas
if ($k>74 && $k<95){$intPrice = 64;}

//Converse Star Chevron
if ($k>94 && $k<101){$intPrice = 34.50;}

//Lucky Brand
if ($k>100 && $k<125){$intPrice = 34.50;}
if (($k ==102) ||($k==105) || ($k ==113) ||($k==118) || ($k ==121) ||($k==122)){ $intPrice = 24.50;}

//Tumi

if (($k ==125) ||($k==126) || ($k ==134) ||($k==139) || ($k ==140) ){ $intPrice = 132.50;}
if (($k ==127) ||($k==131) || ($k ==137) ||($k==138) ){ $intPrice = 137.50;}
if (($k ==128) ||($k==141)  ){ $intPrice = 112.50;}
if (($k ==129) ||($k==130) || ($k ==135) ||($k==136) ){ $intPrice = 127.50;}
if (($k ==133) ||($k==142)  ){ $intPrice = 147.50;}




//Retail
$intRetail = 2 * $intPrice;

if ($k <50){ $strCat = "JOHN VARVATOS";$strBrah = "";}
if ($k>49 && $k<75) { $strCat = "CONVERSE, Backstage"; $strBrah = "Converse Backstage";}
if ($k>74 && $k<95) { $strCat = "CONVERSE, Black Canvas"; $strBrah = "Converse Black Canvas";}
if ($k>94 && $k<101) { $strCat = "CONVERSE, Star Chevron";  $strBrah= "Converse Star Chevron";}
if ($k>100 && $k<125) { $strCat = "LUCKY BRAND";$strBrah = "Lucky Brand";}
if ($k>124 && $k<143) { $strCat = "TUMI";$strBrah = "Tumi";}



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
    //array_push($arr1, $li->plaintext);
    } //end foreach li
} //end foreach ul#ulModels


//print_r($arr);

$arrName = array();
foreach ($dom->find("#MainContent_ucFrameViewer_lblStyleName") as $sn){
    array_push($arrName, $sn->plaintext);
    } //end foreach sn

//print_r($arrName);


$arrBrand = array();
$arrBrand2 = array();
if ($k>49){
foreach ($dom->find("#MainContent_ucFrameViewer_imgLogo span") as $bn){
    array_push($arrBrand, $bn->plaintext);
    } //end foreach sn
$arrBrand = str_replace("-", "", $arrBrand);

}//end if $k>8

$count = 0;
if ($k<50){
    foreach ($dom->find("head meta") as $hm){
        $count++;
        if($count == 2){
            array_push($arrBrand, $hm->outertext);
            //echo $hm->outertext;
        }
    }//end foreach
$arrBrand= explode("content=\"", $arrBrand[0]);
$arrBrand= explode(" v", $arrBrand[1]);
    
}//end if $k<50

//$arrBrand= explode("v9", $arrBrand[1]);

//print_r($arrBrand);


$arrDescStr = "<p>" . $arrDesc[0] . "</p><p>" . $arrDesc[1] . "</p><p>" .  $arrDesc[2] . "</p><p>" .  $arrDesc[3] . "</p><p>" .  $arrDesc[4] . "</p><p>".  $arrDesc[5] . "</p><p>".  $arrDesc[6] . "</p><p>".  $arrDesc[7] . "</p><p>".  $arrDesc[9] . "</p><p>".  $arrDesc[10] . "</p><p>";


//print_r($arr);
//print_r($arr1[0]);
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
     //array_push($arrofarr, $temparr2);
     $temparr2[3] = str_replace(" ", "", $temparr2[3]);
     $temparr2[1] = str_replace(" ", "", $temparr2[1]);
     $temparr2[0]= str_replace(" ", "", $temparr2[0]);
     
    if ($k>49){
     $tempstr = $temparr2[1] . ";1;" . $arrName[0] . ";" . $strCat . ";" . $intRetail . ";30;" . $intPrice . ";;;;;;" . $temparr2[1] . ";" . $temparr2[1] . ";rem;" . ";;;;0.25;999;" . $strBrah . " " . $arrName[0] . " (" . $temparr2[3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";;;1;;1;..//img/sun/" . $temparr2[1] . ".jpg;;;;";}
     
     if ($k<50){
     $tempstr = $temparr2[1] . ";1;" . $arrName[0] . ";" . $strCat . ";" . $intRetail . ";30;" . $intPrice . ";;;;;;" . $temparr2[1] . ";" . $temparr2[1] . ";rem;" . ";;;;0.25;999;" . $strBrah . $arrBrand[0] . " " . $arrName[0] . " (" . $temparr2[3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";;;1;;1;..//img/sun/" . $temparr2[1] . ".jpg;;;;";}
    



     
     /* $tempstr = $temparr2[$i][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $temparr2[$i][1] . "; " . $temparr2[$i][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $temparr2[$i][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $temparr2[$i][0] . ";" . ";;;";  */

    //Saving data for Products.csv
   //  $strVarName = $arrBrand[0] . " " . $arrName[0] . $temparr2[3];
   // scraperwiki::save_var($strVarName, $tempstr);
//print_r($i);
//print_r($strVarName);


//print_r($strVarName);
   // print_r($temparr2);
   //Saving images
  $image_url = "http://www.remeyewear.com/showimage.aspx?img=" . $temparr2[0] . ".jpg&sku=" . $temparr2[1] . "&w=667";
  $image_local = $temparr2[1] . ".jpg,";
  scraperwiki::save_var($image_local, $image_url);
//copy( $image_url, '/tmp/' . $image_local );
   
} //end for count($arr)

//print_r($arrofarr);
//print_r($arrofarr[2][2]);
//print_r($temparr2);


/*

$str = $arrofarr[0][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[0][1] . "; " . $arrofarr[0][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[0][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[0][0] . ";" . ";;;";

echo $str ;
echo "****************************" ;


$str1 = $arrofarr[1][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[1][1] . "; " . $arrofarr[1][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[1][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[1][0] . ";" . ";;;";

echo $str1;
echo "****************************" ;

$str2 = $arrofarr[2][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[2][1] . "; " . $arrofarr[2][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[2][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[2][0] . ";" . ";;;";

echo $str2;
//print_r($arr);
//print_r($arr);
scraperwiki::save_var('fomt', $str2);
*/
}
?><?php

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


$arrPages = array();

//JohnVarvatos
$arrPages[0]= "v740.html";
$arrPages[1]= "v748.html";
$arrPages[2]= "v749.html";
$arrPages[3]= "v750.html";
$arrPages[4]= "v751.html";
$arrPages[5]= "v752-af.html";
$arrPages[6]= "v752.html";
$arrPages[7]= "v753-af.html";
$arrPages[8]= "v753.html";
$arrPages[9]= "v754.html";
$arrPages[10]= "v755.html";
$arrPages[11]= "v756-af.html";
$arrPages[12]= "v756.html";
$arrPages[13]= "v757.html";
$arrPages[14]= "v758.html";
$arrPages[15]= "v759.html";
$arrPages[16]= "v760.html";
$arrPages[17]= "v761.html";
$arrPages[18]= "v762.html";
$arrPages[19]= "v763.html";
$arrPages[20]= "v764.html";
$arrPages[21]= "v765-af.html";
$arrPages[22]= "v765.html";
$arrPages[23]= "v766-af.html";
$arrPages[24]= "v766.html";
$arrPages[25]= "v767-af.html";
$arrPages[26]= "v767.html";
$arrPages[27]= "v768-af.html";
$arrPages[28]= "v768.html";
$arrPages[29]= "v769-af.html";
$arrPages[30]= "v769.html";
$arrPages[31]= "v770-af.html";
$arrPages[32]= "v770.html";
$arrPages[33]= "v771.html";
$arrPages[34]= "v772.html";
$arrPages[35]= "v773-af.html";
$arrPages[36]= "v773.html";
$arrPages[37]= "v774-af.html";
$arrPages[38]= "v774.html";
$arrPages[39]= "v775.html";
$arrPages[40]= "v776.html";
$arrPages[41]= "v777-af.html";
$arrPages[42]= "v777.html";
$arrPages[43]= "v779-af.html";
$arrPages[44]= "v779.html";
$arrPages[45]= "v780-af.html";
$arrPages[46]= "v780.html";
$arrPages[47]= "v905.html";
$arrPages[48]= "v906.html";
$arrPages[49]= "v907.html";

//Converse Backstage
$arrPages[50]= "chart-topper.html";
$arrPages[51]= "chorus.html";
$arrPages[52]= "front-man.html";
$arrPages[53]= "half-stack.html";
$arrPages[54]= "in-studio.html";
$arrPages[55]= "lineup.html";
$arrPages[56]= "merch.html";
$arrPages[57]= "on-tour.html";
$arrPages[58]= "opening-band.html";
$arrPages[59]= "plugged-in.html";
$arrPages[60]= "record-deal.html";
$arrPages[61]= "reel.html";
$arrPages[62]= "roadie.html";
$arrPages[63]= "set-list.html";
$arrPages[64]= "the-close-talker.html";
$arrPages[65]= "the-entertainer.html";
$arrPages[66]= "the-showstopper.html";
$arrPages[67]= "the-sure-thing.html";
$arrPages[68]= "the-tall-tale-teller.html";
$arrPages[69]= "the-traveler.html";
$arrPages[70]= "ticket-holder.html";
$arrPages[71]= "venue.html";
$arrPages[72]= "wavelength.html";
$arrPages[73]= "will-call.html";
$arrPages[74]= "with-the-band.html";

//Converse Black Canvas Sun
$arrPages[75]= "american-dream.html";
$arrPages[76]= "birdie.html";
$arrPages[77]= "breakdown-lane.html";
$arrPages[78]= "converseations.html";
$arrPages[79]= "daring.html";
$arrPages[80]= "endorser.html";
$arrPages[81]= "forum.html";
$arrPages[82]= "foxing.html";
$arrPages[83]= "hall-of-fame.html";
$arrPages[84]= "independence.html";
$arrPages[85]= "maximum-traction.html";
$arrPages[86]= "play-on.html";
$arrPages[87]= "reinvented.html";
$arrPages[88]= "tournament.html";
$arrPages[89]= "triple-treads.html";
$arrPages[90]= "truer-bounce.html";
$arrPages[91]= "well-played.html";
$arrPages[92]= "what-s-new.html";
$arrPages[93]= "who-knows.html";
$arrPages[94]= "world-champion.html";

//Converse Star Chevron
$arrPages[95]= "buzzer-beater.html";
$arrPages[96]= "in-the-mix.html";
$arrPages[97]= "offense.html";
$arrPages[98]= "on-deck.html";
$arrPages[99]= "overtime.html";
$arrPages[100]= "turnover.html";

//Luck Brand
$arrPages[101]= "aurora.html";
$arrPages[102]= "beach-bum.html";
$arrPages[103]= "bootcut.html";
$arrPages[104]= "boyfriend.html";
$arrPages[105]= "capitola.html";
$arrPages[106]= "day-break.html";
$arrPages[107]= "flare.html";
$arrPages[108]= "highlander.html";
$arrPages[109]= "hyannis.html";
$arrPages[110]= "indigo.html";
$arrPages[111]= "interlude.html";
$arrPages[112]= "kennedy.html";
$arrPages[113]= "local.html";
$arrPages[114]= "midnight.html";
$arrPages[115]= "moon-beam.html";
$arrPages[116]= "night.html";
$arrPages[117]= "nocturnal.html";
$arrPages[118]= "oceana.html";
$arrPages[119]= "recruiter.html";
$arrPages[120]= "refrain.html";
$arrPages[121]= "resort.html";
$arrPages[122]= "sun-kiss.html";
$arrPages[123]= "super-skinny.html";
$arrPages[124]= "sync.html";

//Tumi Sun
$arrPages[125]= "bixby-af.html";
$arrPages[126]= "bixby.html";
$arrPages[127]= "brooklyn.html";
$arrPages[128]= "capilano.html";
$arrPages[129]= "coronado-af.html";
$arrPages[130]= "coronado.html";
$arrPages[131]= "kawazu.html";
$arrPages[132]= "malone-af.html";
$arrPages[133]= "malone.html";
$arrPages[134]= "newport.html";
$arrPages[135]= "severn-af.html";
$arrPages[136]= "severn.html";
$arrPages[137]= "stari-af.html";
$arrPages[138]= "stari.html";
$arrPages[139]= "tacoma-af.html";
$arrPages[140]= "tacoma.html";
$arrPages[141]= "tobin.html";
$arrPages[142]= "vasco.html";





$intPrice = 0.00;
$strCat = "";
$intTaxRule = 30;
$intRetail = 0.00;
$strBrah = "";


//for ($k=0; $k<143; $k++){


for ($k=99; $k<143; $k++){
$strPage = "http://cpxip.com/" . $arrPages[$k];
$html = scraperwiki::scrape($strPage);
//$html = scraperwiki::scrape("http://cpxip.com/coronado.html");
$dom = new simple_html_dom();
$dom->load($html);
$arr = array();
$arr1 = array();
$arrDesc = array();


//John Varvatos Book
if (($k ==0) ||($k==49)){ $intPrice = 160;}
if ($k == 1){ $intPrice = 115;}
if (($k >= 2 && $k<=19) || ($k==22) || ($k==39) || ($k==40)){$intPrice = 100;}
if (($k==20) || ($k==23) || ($k==24) || ($k >= 27 && $k<=30)|| ($k==35) || ($k==36) || ($k==43) || ($k==44)){$intPrice = 110;}
if (($k==25) || ($k==26) || ($k >= 31 && $k<=34)|| ($k==37) || ($k==38) || ($k==41) || ($k==42)){$intPrice = 120;}
if (($k ==45) ||($k==46)){ $intPrice = 130;}
if (($k ==47) ||($k==48)){ $intPrice = 180;}

//Converse Backstage
if ($k >49 && $k<75){$intPrice = 29;}


//Converse Black Canvas
if ($k>74 && $k<95){$intPrice = 64;}

//Converse Star Chevron
if ($k>94 && $k<101){$intPrice = 34.50;}

//Lucky Brand
if ($k>100 && $k<125){$intPrice = 34.50;}
if (($k ==102) ||($k==105) || ($k ==113) ||($k==118) || ($k ==121) ||($k==122)){ $intPrice = 24.50;}

//Tumi

if (($k ==125) ||($k==126) || ($k ==134) ||($k==139) || ($k ==140) ){ $intPrice = 132.50;}
if (($k ==127) ||($k==131) || ($k ==137) ||($k==138) ){ $intPrice = 137.50;}
if (($k ==128) ||($k==141)  ){ $intPrice = 112.50;}
if (($k ==129) ||($k==130) || ($k ==135) ||($k==136) ){ $intPrice = 127.50;}
if (($k ==133) ||($k==142)  ){ $intPrice = 147.50;}




//Retail
$intRetail = 2 * $intPrice;

if ($k <50){ $strCat = "JOHN VARVATOS";$strBrah = "";}
if ($k>49 && $k<75) { $strCat = "CONVERSE, Backstage"; $strBrah = "Converse Backstage";}
if ($k>74 && $k<95) { $strCat = "CONVERSE, Black Canvas"; $strBrah = "Converse Black Canvas";}
if ($k>94 && $k<101) { $strCat = "CONVERSE, Star Chevron";  $strBrah= "Converse Star Chevron";}
if ($k>100 && $k<125) { $strCat = "LUCKY BRAND";$strBrah = "Lucky Brand";}
if ($k>124 && $k<143) { $strCat = "TUMI";$strBrah = "Tumi";}



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
    //array_push($arr1, $li->plaintext);
    } //end foreach li
} //end foreach ul#ulModels


//print_r($arr);

$arrName = array();
foreach ($dom->find("#MainContent_ucFrameViewer_lblStyleName") as $sn){
    array_push($arrName, $sn->plaintext);
    } //end foreach sn

//print_r($arrName);


$arrBrand = array();
$arrBrand2 = array();
if ($k>49){
foreach ($dom->find("#MainContent_ucFrameViewer_imgLogo span") as $bn){
    array_push($arrBrand, $bn->plaintext);
    } //end foreach sn
$arrBrand = str_replace("-", "", $arrBrand);

}//end if $k>8

$count = 0;
if ($k<50){
    foreach ($dom->find("head meta") as $hm){
        $count++;
        if($count == 2){
            array_push($arrBrand, $hm->outertext);
            //echo $hm->outertext;
        }
    }//end foreach
$arrBrand= explode("content=\"", $arrBrand[0]);
$arrBrand= explode(" v", $arrBrand[1]);
    
}//end if $k<50

//$arrBrand= explode("v9", $arrBrand[1]);

//print_r($arrBrand);


$arrDescStr = "<p>" . $arrDesc[0] . "</p><p>" . $arrDesc[1] . "</p><p>" .  $arrDesc[2] . "</p><p>" .  $arrDesc[3] . "</p><p>" .  $arrDesc[4] . "</p><p>".  $arrDesc[5] . "</p><p>".  $arrDesc[6] . "</p><p>".  $arrDesc[7] . "</p><p>".  $arrDesc[9] . "</p><p>".  $arrDesc[10] . "</p><p>";


//print_r($arr);
//print_r($arr1[0]);
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
     //array_push($arrofarr, $temparr2);
     $temparr2[3] = str_replace(" ", "", $temparr2[3]);
     $temparr2[1] = str_replace(" ", "", $temparr2[1]);
     $temparr2[0]= str_replace(" ", "", $temparr2[0]);
     
    if ($k>49){
     $tempstr = $temparr2[1] . ";1;" . $arrName[0] . ";" . $strCat . ";" . $intRetail . ";30;" . $intPrice . ";;;;;;" . $temparr2[1] . ";" . $temparr2[1] . ";rem;" . ";;;;0.25;999;" . $strBrah . " " . $arrName[0] . " (" . $temparr2[3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";;;1;;1;..//img/sun/" . $temparr2[1] . ".jpg;;;;";}
     
     if ($k<50){
     $tempstr = $temparr2[1] . ";1;" . $arrName[0] . ";" . $strCat . ";" . $intRetail . ";30;" . $intPrice . ";;;;;;" . $temparr2[1] . ";" . $temparr2[1] . ";rem;" . ";;;;0.25;999;" . $strBrah . $arrBrand[0] . " " . $arrName[0] . " (" . $temparr2[3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";;;1;;1;..//img/sun/" . $temparr2[1] . ".jpg;;;;";}
    



     
     /* $tempstr = $temparr2[$i][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $temparr2[$i][1] . "; " . $temparr2[$i][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $temparr2[$i][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $temparr2[$i][0] . ";" . ";;;";  */

    //Saving data for Products.csv
   //  $strVarName = $arrBrand[0] . " " . $arrName[0] . $temparr2[3];
   // scraperwiki::save_var($strVarName, $tempstr);
//print_r($i);
//print_r($strVarName);


//print_r($strVarName);
   // print_r($temparr2);
   //Saving images
  $image_url = "http://www.remeyewear.com/showimage.aspx?img=" . $temparr2[0] . ".jpg&sku=" . $temparr2[1] . "&w=667";
  $image_local = $temparr2[1] . ".jpg,";
  scraperwiki::save_var($image_local, $image_url);
//copy( $image_url, '/tmp/' . $image_local );
   
} //end for count($arr)

//print_r($arrofarr);
//print_r($arrofarr[2][2]);
//print_r($temparr2);


/*

$str = $arrofarr[0][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[0][1] . "; " . $arrofarr[0][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[0][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[0][0] . ";" . ";;;";

echo $str ;
echo "****************************" ;


$str1 = $arrofarr[1][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[1][1] . "; " . $arrofarr[1][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[1][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[1][0] . ";" . ";;;";

echo $str1;
echo "****************************" ;

$str2 = $arrofarr[2][1] . "; 1;" . $arrName[0] . ";;;;;;;;;;" . $arrofarr[2][1] . "; " . $arrofarr[2][1] . "; " . "rem; " . ";;;;" . "0.25; 999;" . $arrBrand[0] . " " . $arrName[0] . " (" . $arrofarr[2][3] . ");" . $arrDescStr . ";" . ";;;;" . $arrName[0] . ";" . ";;1;;1;..//img/" . $arrofarr[2][0] . ";" . ";;;";

echo $str2;
//print_r($arr);
//print_r($arr);
scraperwiki::save_var('fomt', $str2);
*/
}
?>