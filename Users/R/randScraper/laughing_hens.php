<?php
require 'scraperwiki/simple_html_dom.php'; 
function textbetweenarray($s1,$s2,$s){
  $myarray=array();
  $s1=strtolower($s1);
  $s2=strtolower($s2);
  $L1=strlen($s1);
  $L2=strlen($s2);
  $scheck=strtolower($s);

  do{
  $pos1 = strpos($scheck,$s1);
  if($pos1!==false){
    $pos2 = strpos(substr($scheck,$pos1+$L1),$s2);
    if($pos2!==false){
      $myarray[]=substr($s,$pos1+$L1,$pos2);
      $s=substr($s,$pos1+$L1+$pos2+$L2);
      $scheck=strtolower($s);
      }
        }
  } while (($pos1!==false)and($pos2!==false));
return $myarray;
}


$url = 'http://www.laughinghens.com/sitemap.asp';
$content = file_get_contents($url);

$trs = textbetweenarray("<li><a href=\"knitting-wool-yarn.asp?yarnid=2446\">Araucania Botany Lace</a></li>", "</ul>", $content);

foreach($trs as $tr) {
$tr = str_replace("<ul>", "", $tr);
$tr = str_replace("<li><a href=\"", "http://www.laughinghens.com/", $tr);
$tr = preg_replace("/\">.*/", "EOL", $tr);
$urlArray =explode("EOL", $tr);

for($i=0; $i<(count($urlArray)-1); $i++)
{
$content2 = file_get_contents(trim($urlArray[$i]));
$title = textbetweenarray("<h1>", "</h1>", $content2);
$price = textbetweenarray("Price: &pound;", "</span>", $content2);
if (isset($title[0]) && isset($price[0])){
$record = array(
'product' => $title[0],
//'price' => "£".$price[0]);
'price' => $price[0]);
scraperwiki::save(array('product','price'), $record); 
}
}
}






?>
<?php
require 'scraperwiki/simple_html_dom.php'; 
function textbetweenarray($s1,$s2,$s){
  $myarray=array();
  $s1=strtolower($s1);
  $s2=strtolower($s2);
  $L1=strlen($s1);
  $L2=strlen($s2);
  $scheck=strtolower($s);

  do{
  $pos1 = strpos($scheck,$s1);
  if($pos1!==false){
    $pos2 = strpos(substr($scheck,$pos1+$L1),$s2);
    if($pos2!==false){
      $myarray[]=substr($s,$pos1+$L1,$pos2);
      $s=substr($s,$pos1+$L1+$pos2+$L2);
      $scheck=strtolower($s);
      }
        }
  } while (($pos1!==false)and($pos2!==false));
return $myarray;
}


$url = 'http://www.laughinghens.com/sitemap.asp';
$content = file_get_contents($url);

$trs = textbetweenarray("<li><a href=\"knitting-wool-yarn.asp?yarnid=2446\">Araucania Botany Lace</a></li>", "</ul>", $content);

foreach($trs as $tr) {
$tr = str_replace("<ul>", "", $tr);
$tr = str_replace("<li><a href=\"", "http://www.laughinghens.com/", $tr);
$tr = preg_replace("/\">.*/", "EOL", $tr);
$urlArray =explode("EOL", $tr);

for($i=0; $i<(count($urlArray)-1); $i++)
{
$content2 = file_get_contents(trim($urlArray[$i]));
$title = textbetweenarray("<h1>", "</h1>", $content2);
$price = textbetweenarray("Price: &pound;", "</span>", $content2);
if (isset($title[0]) && isset($price[0])){
$record = array(
'product' => $title[0],
//'price' => "£".$price[0]);
'price' => $price[0]);
scraperwiki::save(array('product','price'), $record); 
}
}
}






?>
