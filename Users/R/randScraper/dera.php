<?php
require 'scraperwiki/simple_html_dom.php';  
for($i=1;$i<20;$i++){
$content=file_get_contents('http://www.deramores.com/knitting-yarn?price=1%2C50&p='.$i);
preg_match_all("/\">.*<\/a><\/h4>/", $content, $titles);
preg_match_all("/<span class=\"price\">.*<\/span>                <\/span>/", $content, $prices);

$allTitles = array();
$allPrices = array();
foreach ($titles[0] as $title)
{
   $title =  str_replace("\">", "", $title); 
   $title =  str_replace("</a></h4>", "", $title);
   $allTitles[]=$title;
}
foreach ($prices[0] as $price){
    $price =  str_replace("<span class=\"price\">", "", $price); 
    $price =  str_replace("</span>", "", $price); 
    $price =  str_replace("£", "", $price); 
    $allPrices[]=$price;
}

for($j=0;$j<(count($allTitles)-1);$j++)
{
$record = array(
'product' => $allTitles[$j],
'price' => $allPrices[$j]);
scraperwiki::save(array('product','price'), $record);
//$allTitles[$j].", ".$allPrices[$j]."\n");
}
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';  
for($i=1;$i<20;$i++){
$content=file_get_contents('http://www.deramores.com/knitting-yarn?price=1%2C50&p='.$i);
preg_match_all("/\">.*<\/a><\/h4>/", $content, $titles);
preg_match_all("/<span class=\"price\">.*<\/span>                <\/span>/", $content, $prices);

$allTitles = array();
$allPrices = array();
foreach ($titles[0] as $title)
{
   $title =  str_replace("\">", "", $title); 
   $title =  str_replace("</a></h4>", "", $title);
   $allTitles[]=$title;
}
foreach ($prices[0] as $price){
    $price =  str_replace("<span class=\"price\">", "", $price); 
    $price =  str_replace("</span>", "", $price); 
    $price =  str_replace("£", "", $price); 
    $allPrices[]=$price;
}

for($j=0;$j<(count($allTitles)-1);$j++)
{
$record = array(
'product' => $allTitles[$j],
'price' => $allPrices[$j]);
scraperwiki::save(array('product','price'), $record);
//$allTitles[$j].", ".$allPrices[$j]."\n");
}
}
?>
