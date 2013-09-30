<?php
require 'scraperwiki/simple_html_dom.php';  
for($i=1;$i<20;$i++){
$content=file_get_contents('http://www.deramores.com/knitting-yarn?price=1%2C50&p='.$i);
preg_match_all("/\">.*<\/a><\/h4>/", $content, $titles);
preg_match_all("/<span class=\"price\">.*<\/span>                <\/span>/", $content, $prices);
preg_match_all("/class=\"button\"><span><span>.*<\/span><\/span>/", $content, $shades);

$allTitles = array();
$allPrices = array();
$allShades = array();
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

foreach ($shades[0] as $shade)
{
   $shade =  str_replace("class=\"button\"><span><span>View All ", "", $shade); 
   $shade =  str_replace(" Shades</span></span>", "", $shade);
   $shade =  str_replace("class=\"button\"><span><span>More Info</span></span>", "Yarn Pack", $shade); 
   $allShades[]=$shade;
}

for($j=0;$j<(count($allTitles));$j++)
{
$record = array(
'product' => $allTitles[$j],
'price' => $allPrices[$j],
'shades' => $allShades[$j]);
scraperwiki::save(array('product','price','shades'), $record);
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
preg_match_all("/class=\"button\"><span><span>.*<\/span><\/span>/", $content, $shades);

$allTitles = array();
$allPrices = array();
$allShades = array();
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

foreach ($shades[0] as $shade)
{
   $shade =  str_replace("class=\"button\"><span><span>View All ", "", $shade); 
   $shade =  str_replace(" Shades</span></span>", "", $shade);
   $shade =  str_replace("class=\"button\"><span><span>More Info</span></span>", "Yarn Pack", $shade); 
   $allShades[]=$shade;
}

for($j=0;$j<(count($allTitles));$j++)
{
$record = array(
'product' => $allTitles[$j],
'price' => $allPrices[$j],
'shades' => $allShades[$j]);
scraperwiki::save(array('product','price','shades'), $record);
//$allTitles[$j].", ".$allPrices[$j]."\n");
}
}
?>
